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

def fill_case_statement(table_name: str) -> str:
    return f'''case "{table_name}":
    synccontributionlevels = importlib.import_module('moma.pipelines.sync{table_name.replace('_', '')}')
    make_runner(synccontributionlevels.ContributionLevel)()'''

for t in TABLES:
    print(fill_case_statement(t))