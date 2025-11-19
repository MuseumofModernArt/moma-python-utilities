# Running these scripts

## Schema Maker
`schema-maker.py` takes as an argument the name of the table it is being called for. For example, to run it for the `purchased_tickets` table, one would run the following code:
```
python moma/pipelines/scripts/schema-maker.py purchased_tickets
```

This will print two schemas to the console. The first, labelled "Record Schema" can be used as a base for filling in the lines under `class Record(typing.NamedTuple):`.

"Transfer Schema" should be slotted into the `fields` key under `bq_table_schema`.
```
bq_table_schema={
            'fields': ...
        }
```

## Case Maker
`case-maker.py` takes the same argument as `schema-maker.py`. For example:
```
python moma/pipelines/scripts/case-maker.py purchased_tickets
```

This will print some Python code to the console. It can be appended to `pipelines/__init__.py`. **NB: Double check the `make_runner` line to ensure the argument matches the object name in the sync file.** 