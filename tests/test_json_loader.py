import json

from python_parser.examples.json_parser import load as json_loads


def test_json_loader():
    samples = (
        {
            'first': [1, 2, 3, {'5': 6}, True],
            'key': 'value',
            '1': 2,
        },
        [
            {'test': 'test'},
            None,
            {'test': False},
            -321.123
        ],
        {},
        []
    )
    for sample in samples:
        assert json_loads(json.dumps(sample)) == sample
