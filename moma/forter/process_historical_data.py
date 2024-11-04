import datetime
import json
import os
import pprint
import random
import re
import sys
import yaml

ignored_sources = [
    'TicketOrderRefundHerokuTransactionJob',
    'SpecialEventLineitemGuestsHerokuTransactionJob'
]

def load_objects(filename, key_field, destination):
    with open(filename, encoding='utf-8') as f:
        line_number = 0
        for line in f:
            line_number += 1
            try:
                json_object = json.loads(line)
                if json_object[key_field] is None:
                    continue

                if json_object.get('source__c') in ignored_sources:
                    continue

                if 'amount' in json_object and json_object.get('amount') in [0, None]:
                    continue

                if not json_object[key_field] in destination:
                    destination[json_object[key_field]] = []
                elif not json_object.get('sfid') is None:
                    skip = False
                    for jo in destination[json_object[key_field]]:
                        if json_object.get('sfid') == jo.get('sfid'):
                            skip = True
                    if skip:
                        continue

                destination[json_object[key_field]].append(json_object)

            except json.JSONDecodeError:
                print(f'Error decoding JSON {filename}:{line_number} - {line}')
        return destination

def duplicate_count(hd, label):
    i = 0
    count = 0
    max_count = 0
    for k in hd:
        i+=1
        if len(hd[k]) > 1:
            count += 1
            if len(hd[k]) > max_count:
                max_count = len(hd[k])
            pprint.pp((i, label, k, len(hd[k]), hd[k]))
            print('\n')
    return (count, max_count)

now = datetime.datetime.now(datetime.timezone.utc).timestamp()
def format_order_validation(payment, cart, user, line_items, heroku_transaction, ticketing_order, ticketing_tickets, tiers, events):
    event_datetime = timestamp(payment['updated_at'])
    recipient = format_primary_recipient(line_items[0])
    order_validation_data = {
        # 'authorizationStep': 'POST_AUTHORIZATION',
        'cartItems': format_cart_items(cart, line_items, ticketing_order, ticketing_tickets, tiers),
        'checkoutTime': int(event_datetime * 1000),
        'orderId': cart['uuid'],
        'orderType': 'WEB',
        'payment': format_payment_information(payment),
        'primaryDeliveryDetails': format_primary_delivery_details(),
        'primaryRecipient': recipient,
        'timeSentToForter': int(now * 1000),
        'totalAmount': { 'amountUSD': format_amount(payment['amount_in_cents'] / 100.0) },
        'accountOwner': format_account_owner(user, recipient),
        'historicalData': format_historical_data(payment, events),
    }
    ip_address = dig(payment, ['properties', 'ip_address'])
    if not ip_address is None:
        order_validation_data['connectionInformation'] = {
            'customerIP': ip_address,
        }
    return order_validation_data

def format_cart_items(cart, line_items, ticketing_order, ticketing_tickets, tiers):
    cart_items = []
    for line_item in line_items:
        if line_item['type'] in membership_types:
            cart_items.append(membership_cart_item(line_item, tiers))
        elif line_item['type'] in ticket_types:
            cart_items.extend(ticket_order_cart_items(line_item, ticketing_order, ticketing_tickets))
        elif line_item['type'] == 'LineItems::SpecialEventContribution':
            cart_items.append(special_event_contribution_cart_item(line_item))
        elif line_item['type'] == 'LineItems::SpecialEventDonation':
            cart_items.append(special_event_donation_cart_item(line_item))
        elif line_item['type'] in donation_types:
            cart_items.append(donation_cart_item(line_item))
        else:
            raise ProcessingException(f'Not implemented for {line_item}')

    return cart_items

def membership_cart_item(line_item, tiers):
    return {
        'basicItemData': {
            'name': membership_product_name(line_item, tiers),
            'price': {
                'amountUSD': format_amount(line_item['amount_in_cents'] / 100.0)
            },
            'quantity': 1,
            'type': 'NON_TANGIBLE'
        }
    }

def membership_product_name(line_item, tiers):
    tier = tiers[line_item['properties']['tier_id']][0]
    preface = 'New' if line_item['properties']['joiner'] else 'Renewal'
    name_parts = [preface, tier['name']]
    if line_item['type'] == 'LineItems::GiftMembership':
        name_parts.append('Gift')
    name_parts.append('Membership')
    return ' '.join(name_parts)

def ticket_order_cart_items(line_item, ticketing_orders, ticketing_tickets):
    order = ticketing_orders[line_item['properties']['order_id']]
    tickets = ticketing_tickets[order['id']]

    cart_items = []
    for detail in line_item['properties']['order_details']:
        if int(detail['quantity']) < 1:
            continue

        ticket = None
        for t in tickets:
            if detail['external_id'] == t['external_id'] and detail['ticket_type_id'] == t['ticket_type_id']:
                ticket = t
                break

        if ticket is None:
            raise ProcessingException(f'Missing ticket {line_item}')

        cart_items.append({
            'basicItemData': {
                'name': ticket_product_name(line_item, ticket),
                'price': {
                    'amountUSD': format_amount(ticket['price'] / 100.0),
                },
                'quantity': int(detail['quantity']),
                'type': 'NON_TANGIBLE'
            }
        })

    return cart_items

def ticket_product_name(line_item, ticket):
    class_name = line_item['type'].split('::')[-1]
    return ' '.join([class_name, ticket['name']])

def donation_cart_item(line_item):
    return {
        'name': 'Donation',
        'price': {
            'amountUSD': format_amount(line_item['amount_in_cents'] / 100.0)
        },
        'quantity': 1,
        'type': 'NON_TANGIBLE'
    }

def special_event_contribution_cart_item(line_item):
    return {
        'name': f'{line_item['properties']['special_event_title']} Contribution',
        'price': {
            'amountUSD': format_amount(line_item['amount_in_cents'] / 100.0)
        },
        'quantity': 1,
        'type': 'NON_TANGIBLE'
    }

def special_event_donation_cart_item(line_item):
    return {
        'name': f'{line_item['properties']['special_event_title']} Donation',
        'price': {
            'amountUSD': format_amount(line_item['amount_in_cents'] / 100.0)
        },
        'quantity': 1,
        'type': 'NON_TANGIBLE'
    }

def format_payment_information(payment):
    return [{
        'amount': {
            'amountUSD': format_amount(payment['amount_in_cents'] / 100.0)
        },
        'creditCard': format_credit_card(payment),
        # 'billingDetails': format_billing_details(payment)
    }]

def format_credit_card(payment):
    credit_card = {}
    additional_data = dig(payment, ['properties', 'additional_data'])
    raw_payment_data = dig(payment, ['properties', 'raw_payment_data'])

    if additional_data is None or raw_payment_data is None:
        raise ProcessingException('missing payment data')

    add_el(credit_card, additional_data, 'cardBin', 'bin')
    add_el(credit_card, payment, 'last_digits', 'lastFourDigits')
    add_el(credit_card, payment, 'card_brand', 'cardBrand')

    expiry_parts = additional_data['expiryDate'].split('/')
    credit_card['expirationMonth'] = expiry_parts[0]
    credit_card['expirationYear'] = expiry_parts[1]

    credit_card['cardType'] = 'UNKNOWN'

    add_el(credit_card, additional_data, 'countryOfIssuance', 'issuerCountry')

    credit_card['fullResponsePayload'] = raw_payment_data

    credit_card['paymentProcessorData'] = {
        'processorName': 'Adyen',
        'processorTransactionId': payment['properties']['psp_reference']
    }

    credit_card['verificationResults'] = format_verification_results(payment)

    return credit_card

def format_billing_details(payment):
    personal_details = {}
    add_el(personal_details, payment['properties'], 'email', 'email')
    add_el(personal_details, payment['properties'], 'first_name', 'firstName')
    add_el(personal_details, payment['properties'], 'last_name', 'lastName')

    if not 'email' in personal_details:
        shopper_reference = dig(payment, ['properties', 'additional_data', 'recurring.shopperReference'])
        if not shopper_reference is None:
            personal_details['email'] = shopper_reference.rsplit('_', 1)[0]

    return {
        'personalDetails': personal_details
    }

def dig(source, keys=[]):
    rval = source
    for key in keys:
        if key in rval:
            rval = rval[key]
        else:
            return None
    return rval

def format_verification_results(payment):
    additional_data = dig(payment, ['properties', 'additional_data'])
    raw_payment_data = dig(payment, ['properties', 'raw_payment_data'])

    response_text = raw_payment_data['resultCode'] if payment['status'] == 'collected' else raw_payment_data['refusalReason']

    verification_data = {
        'processorResponseText': response_text
    }

    add_el(verification_data, additional_data, 'cvcResultRaw', 'cvvResult')
    add_el(verification_data, additional_data, 'avsResultRaw', 'avsFullResult')
    add_el(verification_data, additional_data, 'authCode', 'authorizationCode')
    add_el(verification_data, additional_data, 'refusalReasonCode', 'processorResponseCode')

    return verification_data

def format_primary_delivery_details():
    return {
        'deliveryMethod': 'email',
        'deliveryType': 'DIGITAL'
    }

membership_types = ['LineItems::Membership', 'LineItems::GiftMembership']
ticket_types = ['LineItems::OnlineTicketOrder', 'LineItems::FilmTicketOrder']
special_event_types = ['LineItems::SpecialEventContribution', 'LineItems::SpecialEventDonation']
donation_types = ['LineItems::Donation']

def format_primary_recipient(line_item):
    # get the order attributes based on the line item type
    order_attributes = {}
    if line_item['type'] in membership_types:
        order_attributes = line_item['properties']['primary_member_attributes']
    elif line_item['type'] in ticket_types:
        order_attributes = line_item['properties']['user_attributes']
    elif line_item['type'] in special_event_types:
        order_attributes = line_item['properties']['order_attributes']
    elif line_item['type'] in donation_types:
        order_attributes = line_item['properties']['donor_info']
    else:
        raise ProcessingException(f'Not implemented for {line_item}')

    personal_details = {}
    add_el(personal_details, order_attributes, 'email', 'email')
    add_el(personal_details, order_attributes, 'first_name', 'firstName')
    add_el(personal_details, order_attributes, 'last_name', 'lastName')

    primary_recipient = {
        'personalDetails': personal_details
    }

    if 'phone_number' in order_attributes:
        primary_recipient['phone'] = [{ 'phone': order_attributes['phone_number'] }]

    return primary_recipient

def format_account_owner(user, recipient):
    if user is None:
        personal_details = recipient['personalDetails']
        account_owner = {}
        add_el(account_owner, personal_details, 'email', 'email')
        add_el(account_owner, personal_details, 'firstName', 'firstName')
        add_el(account_owner, personal_details, 'lastName', 'lastName')
        return account_owner

    created_at = timestamp(user['created_at'])
    account_owner = {
        'created': int(created_at),
    }
    add_el(account_owner, user, 'email', 'email')
    add_el(account_owner, user, 'uuid', 'id')
    add_el(account_owner, user, 'first_name', 'firstName')
    add_el(account_owner, user, 'last_name', 'lastName')
    return account_owner

def add_el(dest, source, key, dest_key):
    if key in source:
        dest[dest_key] = source[key]

def format_amount(amount):
    return '%0.2f' % amount

def timestamp(ts):
    return datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f').timestamp()

def sanitize_keys(objs):
    sanitized_objs = []
    for obj in objs:
        sanitized_obj = {}
        for key in obj:
            sanitized_obj[key.replace(':', '')] = obj[key]
        sanitized_objs.append(sanitized_obj)
    return sanitized_objs

def format_historical_data(payment, events):
    if len(events) == 0:
        if payment['status'] == 'collected':
            return {
                'status': 'COMPLETED',
                'fraud': 'NONE'
            }
        elif payment['status'] == 'failed':
            refusal_reason = dig(payment, ['properties', 'refusal_reason'])
            if refusal_reason is None or re.search(r'fraud', refusal_reason, re.I):
                return {
                    'status': 'PAYMENT_NOT_AUTHORIZED',
                    'fraud': 'DECLINED_FOR_FRAUD'
                }
            else:
                return {
                    'status': 'PAYMENT_NOT_AUTHORIZED',
                    'fraud': 'NONE'
                }
        else:
            pprint.pprint(payment)
            return {}

    last_event = events[-1]

    fraud = 'NONE'
    if last_event['eventCode'] == 'AUTHORISATION' and last_event['success']:
        status = 'COMPLETED'

    elif last_event['eventCode'] == 'AUTHORISATION' and not last_event['success']:
        status = 'PAYMENT_NOT_AUTHORIZED'
        if re.search(r'fraud', last_event['reason'], re.I):
            fraud = 'DECLINED_FOR_FRAUD'

    elif last_event['eventCode'] == 'CAPTURE_FAILED':
        status = 'CANCELED_BY_MERCHANT'

    elif last_event['eventCode'] == 'CAPTURE':
        status = 'COMPLETED'

    else:
        status = 'COMPLETED'
        fraud = last_event['eventCode']

    return {
        'status': status,
        'fraud': fraud
    }

class ProcessingException(Exception):
    """Processing Error"""

if __name__ == '__main__':
    hts = load_objects('/home/jhalderm/Documents/online_transaction_hts.json', 'reference_id__c', {})
    users_by_contact_id = load_objects('/home/jhalderm/Documents/users.json', 'contact_id', {})
    users_by_fallback_contact_id = load_objects('/home/jhalderm/Documents/users.json', 'fallback_contact_id', {})
    carts = load_objects('/home/jhalderm/Documents/carts.json', 'id', {})
    line_items = load_objects('/home/jhalderm/Documents/line_items.json', 'cart_id', {})
    ticket_orders = load_objects('/home/jhalderm/Documents/ticketing_orders.json', 'id', {})
    tickets = load_objects('/home/jhalderm/Documents/ticketing_tickets.json', 'order_id', {})
    tiers = load_objects('/home/jhalderm/Documents/tiers.json', 'id', {})
    webhook_events = load_objects('/home/jhalderm/Documents/adyen-webhook-data-for-membership-ecom.json', 'merchantReference', {})

    # ht_count, max_ht_count = duplicate_count(hts, 'heroku transactions')
    # u_by_cid_count, max_u_by_cid_count = duplicate_count(users_by_contact_id, 'users by contact id')
    # u_by_fb_cid_count, max_u_by_fb_cid_count = duplicate_count(users_by_fallback_contact_id, 'users by fallback contact id')
    # carts_count, max_carts_count = duplicate_count(carts, 'carts')
    # li_count, max_li_count = duplicate_count(line_items, 'line_items')

    # print(f'heroku transactions {len(hts)} - {ht_count} - {max_ht_count}')
    # print(f'users by contact id {len(users_by_contact_id)} - {u_by_cid_count} - {max_u_by_cid_count}')
    # print(f'user by fallback contact id {len(users_by_fallback_contact_id)} - {u_by_fb_cid_count} - {max_u_by_fb_cid_count}')
    # print(f'carts {len(carts)} - {carts_count} - {max_carts_count}')
    # print(f'line_items {len(line_items)} - {li_count} - {max_li_count}')


    # event code AUTHORISATION: 214915
    # event code DISPUTE_DEFENSE_PERIOD_ENDED: 1974
    # event code REFUND: 2779
    # event code REPORT_AVAILABLE: 328
    # event code NOTIFICATION_OF_FRAUD: 2331
    # event code ISSUER_COMMENTS: 107
    # event code CHARGEBACK: 2336
    # event code NOTIFICATION_OF_CHARGEBACK: 2363
    # event code INFORMATION_SUPPLIED: 10
    # event code CAPTURE_FAILED: 32
    # event code ISSUER_RESPONSE_TIMEFRAME_EXPIRED: 7
    # event code CAPTURE: 32
    # event code CHARGEBACK_REVERSED: 12
    # event code SECOND_CHARGEBACK: 4
    # event code REQUEST_FOR_INFORMATION: 2

    last_webhook_event_counts = { None: 0 }
    event_counts = {}
    error_counts = {
        'KeyError': 0,
        'JSONDecodeError': 0,
        'ProcessingException': 0
    }
    authorisation_reasons = {}

    webhook_events_by_event_code = load_objects('/home/jhalderm/Documents/adyen-webhook-data-for-membership-ecom.json', 'eventCode', {})
    for event_code in webhook_events_by_event_code:
        last_webhook_event_counts[event_code] = 0

    # for event in webhook_events_by_event_code['AUTHORISATION']:
    #     if not event['success']:
    #         reason = event['reason']
    #         if not reason in authorisation_reasons:
    #             authorisation_reasons[reason] = 0
    #         authorisation_reasons[reason] += 1

    print('\n')

    # get the seed
    SEED=int(os.getenv('SEED', random.randint(1, 100000)))
    print(f'SEED={SEED}')
    sys.stdout.flush()
    random.seed(SEED)

    VERBOSE = os.getenv('VERBOSE', False) == 'true'

    SAMPLE_SIZE=int(os.getenv('SAMPLE_SIZE', 100))

    file_name = '/home/jhalderm/Documents/payment_details.json'
    output_file_name = '/home/jhalderm/Documents/order_validation_sample.json'

    with open(output_file_name, '+w', encoding='utf-8') as of:
        with open(file_name, encoding='utf-8') as f:
            line_number = 0
            for line in f:
                line_number += 1
                cart = None
                heroku_transaction = None
                user = None
                cart_line_items = None
                cart_ticket_orders = None
                cart_tickets = None

                if random.randint(1, 100) > SAMPLE_SIZE:
                    continue

                try:
                    payment = json.loads(line)

                    cart = carts[payment['cart_id']][0]

                    if cart['fallback_contact_id'] in users_by_fallback_contact_id:
                        user = users_by_fallback_contact_id[cart['fallback_contact_id']][-1]
                    if cart['contact_id'] in users_by_contact_id:
                        user = users_by_contact_id[cart['contact_id']][-1]

                    # if not cart['uuid'] in hts:
                    #     print(f'missing heroku transaction {file_name}:{line_number} - {line} - cart uuid: {cart['uuid']}')
                    #     print('\n')
                    #     continue

                    heroku_transaction = hts.get(cart['uuid'], [None])[0]
                    cart_line_items = line_items[cart['id']]

                    cart_ticket_orders = {}
                    cart_tickets = {}
                    for line_item in cart_line_items:
                        if 'order_id' in line_item['properties']:
                            order = ticket_orders[line_item['properties']['order_id']][0]

                            cart_ticket_orders[order['id']] = order

                            if not order['requested_items'] is None:
                                cart_tickets[order['id']] = sanitize_keys(yaml.safe_load(order['requested_items'].replace('\\n', '\n')))
                            else:
                                cart_tickets[order['id']] = tickets.get(order['id'], [])

                    events = webhook_events.get(cart['uuid'], [])
                    event = None
                    if len(events) > 0:
                        event = events[-1]['eventCode']

                    last_webhook_event_counts[event] += 1

                    if not len(events) in event_counts:
                        event_counts[len(events)] = 0

                    event_counts[len(events)] += 1

                    if not event is None and event == 'AUTHORISATION':
                        last_event = events[-1]
                        if not last_event['success']:
                            reason = last_event['reason']
                            if not reason in authorisation_reasons:
                                authorisation_reasons[reason] = 0
                            authorisation_reasons[reason] += 1

                    # pprint.pp(cart)
                    # pprint.pp(user)
                    # pprint.pp(ht)
                    # pprint.pp(li)

                    # pprint.pp(format_order_validation(payment, cart, user, cart_line_items, heroku_transaction, cart_ticket_orders, cart_tickets, tiers))
                    # print('\n')

                    order_validation_obj = format_order_validation(payment, cart, user, cart_line_items, heroku_transaction, cart_ticket_orders, cart_tickets, tiers, events)
                    json.dump(order_validation_obj, of)

                    of.write('\n')
                except KeyError as key_error:
                    error_counts['KeyError'] += 1
                    if VERBOSE:
                        print(f'Key Error: {key_error}')
                        pprint.pp(('payment: ', payment))
                        pprint.pp(('cart: ', cart))
                        pprint.pp(('cart_line_items: ', cart_line_items))
                        pprint.pp(('heroku_transaction: ', heroku_transaction))
                        pprint.pp(('user: ', user))
                        pprint.pp(('cart_ticket_orders: ', cart_ticket_orders))
                        pprint.pp(('cart_tickets: ', cart_tickets))
                        print('\n')
                        sys.stdout.flush()
                except ProcessingException as processing_error:
                    error_counts['ProcessingException'] += 1
                    if VERBOSE:
                        print(f'Error processing order {file_name}:{line_number} - {line}')
                        print(processing_error)
                        print('\n')
                        sys.stdout.flush()
                except json.JSONDecodeError:
                    error_counts['JSONDecodeError'] += 1
                    if VERBOSE:
                        print(f'Error decoding JSON {file_name}:{line_number} - {line}')
                        print('\n')
                        sys.stdout.flush()

        # format data according to forter requirements
        # write output to file

        # SEED=82994
        # SEED=86739
        # SEED=5924

        print('\nwebhook event counts')
        for event_code in webhook_events_by_event_code:
            print(f'event code {event_code}: {len(webhook_events_by_event_code[event_code])}')

        print('\nlast webhook event counts')
        for event_code in last_webhook_event_counts:
            print(f'event code {event_code}: {last_webhook_event_counts[event_code]}')

        print('\nevent count frequencies')
        for event_count in event_counts:
            print(f'count {event_count}: {event_counts[event_count]}')

        print('\nerror counts')
        for error_code in error_counts:
            print(f'count {error_code}: {error_counts[error_code]}')

        print('\nauthorisation reaons')
        for reason in authorisation_reasons:
            print(f'reason \'{reason}\': {authorisation_reasons[reason]}')