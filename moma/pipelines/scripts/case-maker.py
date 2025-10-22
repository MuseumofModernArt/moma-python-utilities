# change this out depending on which tables have been added
TABLES = [
    'events',
    'price_lists',
    'ticket_types',
    'ticket_types_products',
    'event_time_slots',
    'event_tickets',
    'price_lists_ticket_types',
    'ticket_type_categories',
    'events_ticket_type_categories',
    'event_time_slots_products'
]

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def fill_case_statement(table_name: str) -> str:
    unspaced_table_name = table_name.replace('_', '')
    return f'''case "{table_name}":
    sync{unspaced_table_name} = importlib.import_module('moma.pipelines.sync{unspaced_table_name}')
    make_runner(sync{unspaced_table_name}.{to_camel_case(table_name)})()'''

if __name__ == '__main__':
    for t in TABLES:
        print(fill_case_statement(t))