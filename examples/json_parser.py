from python_parser import Parser, a, anyof, maybe, skip, someof, to_dot

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
    'ROOT': anyof('OBJ', 'ARR'),
    'VAL': anyof('STR', 'NUM', 'ARR', 'OBJ', 'TRUE', 'FALSE', 'NULL'),
    'ARR': a(skip('L_BR'), 'VAL', maybe(someof(skip('SEP'), 'VAL')), skip('R_BR')),
    'OBJ': a(skip('L_PAR'), 'PAIR', maybe(someof(skip('SEP'), 'PAIR')), skip('R_PAR')),
    'PAIR': a(anyof('STR', 'NUM'), skip('COL'), 'VAL')
}

parser = Parser(tokens, grammar)


class Interpreter(object):

    def arr(self, node):
        return list(map(self.val, node.items))

    def obj(self, node):
        return dict(map(self.pair, node.items))

    def val(self, node):
        node = node.items[0]
        return {
            'STR': lambda t: t.value,
            'NUM': lambda t: float(t.value),
            'TRUE': lambda _: True,
            'FALSE': lambda _: False,
            'NULL': lambda _: None,
            'ARR': self.arr,
            'OBJ': self.obj
        }[node.name](node)

    def pair(self, node):
        key, value = node.items
        return self.val(node), self.val(value)

    def visit(self, node):
        node = node.items[0]
        return getattr(self, node.name.lower())(node)
