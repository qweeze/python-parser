from python_parser import Parser, a, anyof, maybe, skip, someof

tokens = (
    ('[+-]?(\\d+(\\.\\d*)?|\\.\\d+)', 'NUM'),
    ('"\w+"', 'STR'),
    (':', 'COL'),
    ('\[', 'L_BR'),
    ('\]', 'R_BR'),
    ('{', 'L_PAR'),
    ('}', 'R_PAR'),
    ('\,', 'SEP'),
    ('true', 'TRUE'),
    ('false', 'FALSE'),
    ('null', 'NULL')
)
grammar = {
    'ROOT': anyof('ARR', 'OBJ'),
    'VAL': anyof('STR', 'NUM', 'ARR', 'OBJ', 'TRUE', 'FALSE', 'NULL'),
    'ARR': a(
        skip('L_BR'),
        maybe('VAL', maybe(someof(skip('SEP'), 'VAL'))),
        skip('R_BR')
    ),
    'OBJ': a(
        skip('L_PAR'),
        maybe('PAIR', maybe(someof(skip('SEP'), 'PAIR'))),
        skip('R_PAR')
    ),
    'PAIR': a('STR', skip('COL'), 'VAL')
}

parser = Parser(tokens, grammar)


def load(text):

    def arr(node):
        return list(map(val, node.items))

    def obj(node):
        return dict(map(pair, node.items))

    def val(node):
        node = node.items[0]
        return {
            'STR': lambda t: t.value[1: -1],
            'NUM': lambda t: float(t.value),
            'TRUE': lambda _: True,
            'FALSE': lambda _: False,
            'NULL': lambda _: None,
            'ARR': arr,
            'OBJ': obj
        }[node.name](node)

    def pair(node):
        key, value = node.items
        return val(node), val(value)

    ast = parser.parse('ROOT', text)
    root = ast.items[0]
    return locals()[root.name.lower()](root)
