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
    'VAL': anyof('STR', 'NUM', 'ARR', 'OBJ', 'TRUE', 'FALSE', 'NULL'),
    'ARR': a(skip('L_BR'), 'VAL', maybe(someof(skip('SEP'), 'VAL')), skip('R_BR')),
    'OBJ': a(skip('L_PAR'), 'PAIR', maybe(someof(skip('SEP'), 'PAIR')), skip('R_PAR')),
    'PAIR': a(anyof('STR', 'NUM'), skip('COL'), 'VAL')
}

parser = Parser(tokens, grammar)
