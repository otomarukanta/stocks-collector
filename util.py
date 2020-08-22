from typing import Any, Iterable, NamedTuple

def generate_avro_schema(records: Iterable[NamedTuple]):
    def to_avro_type(t: Any):
        if t is int:
            return 'int'
        elif t is float:
            return 'double'
        else:
            raise Exception(f"{t} is not supported to convert avro type.")
    cls = next(iter(records))
    fields = cls.__annotations__
    name = cls.__class__.__name__
    avro_fields = [{'name': k, 'type': to_avro_type(v)} for k, v in fields.items()]
    return {
        'name': name,
        'type': 'record',
        'fields': avro_fields
    }