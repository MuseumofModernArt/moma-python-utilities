import re
from typing import List, Dict

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

TYPE_CONVERSION = {
    'STRING': 'str',
    'INT64': 'int',
    'BOOL':	'bool',
    'TIMESTAMP': 'datetime.datetime',
    'JSON':	'dict'
}

schema_re = re.compile(r'TABLE `moma-membership.moma_import.[a-z_]+`[ \n]\(\n(.+?)\n\)\nPART', flags=re.DOTALL)
record_re = re.compile(r'([a-z_]+) ([A-Z0-9]+)')

def get_schema_file(table_name: str) -> str:
    with open(f'./moma/pipelines/bq-schemas/{table_name}.sql') as f:
        sql_text = f.read()
        m = re.search(schema_re, sql_text) 
        try:
            return [el.strip() for el in m[1].split(',\n')]
        except TypeError:
            print(f'Problem in {table_name}')
            return ''
        
def build_record_schema_row(el: str) -> str:
    a = re.search(record_re, el)
    return (f'{a[1]}: {TYPE_CONVERSION[a[2]]}')
    
def make_record_schema(create_schema: List[str]) -> str:
    return [build_record_schema_row(el) for el in create_schema]

def build_bq_schema_row(el: str) -> Dict[str, str]:
    a = re.search(record_re, el)
    return {'name': a[1], 'type': a[2], 'mode': 'REQUIRED' if 'NOT NULL' in el else 'NULLABLE'}

def make_bq_schema(create_schema: List[str]) -> List[Dict[str, str]]:
    return [build_bq_schema_row(el) for el in create_schema]

if __name__ == '__main__':
    key = 'events' # change out this string for the file name in bq-schemas
    schema = get_schema_file(key)
    print('Record Schema:')
    print(make_record_schema(schema))
    print('Transfer Schema:')
    print(make_bq_schema(schema))