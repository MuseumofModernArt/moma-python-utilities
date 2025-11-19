import sys

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def fill_case_statement(table_name: str) -> str:
    unspaced_table_name = table_name.replace('_', '')
    return f'''case "{table_name}":
    sync{unspaced_table_name} = importlib.import_module('moma.pipelines.sync{unspaced_table_name}')
    make_runner(sync{unspaced_table_name}.{to_camel_case(table_name)[:-1]})()'''

if __name__ == '__main__':
    print(fill_case_statement(sys.argv[1]))