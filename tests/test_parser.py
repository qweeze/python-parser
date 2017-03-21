import pytest
from python_parser.parser import Lexer, Token, Node
from python_parser import *


def test_lexer():
    patterns = (
        ('\d+', 'NUM'),
        ('\w+', 'STR')
    )
    lexer = Lexer(patterns)

    assert list(lexer.lex( '123 abc ')) == (
        [Token('NUM', '123'), Token('STR', 'abc'), Token('EOF', None)]
    )
    assert list(lexer.lex('')) == [Token('EOF', None)]

    with pytest.raises(SyntaxError):
        list(lexer.lex('123 abc ?'))


def test_parser():
    patterns = (
        ('\(', 'L_PAR'),
        ('\)', 'R_PAR'),
        ('\,', 'SEP'),
        ('\d+', 'NUM'),
        ('"\w+"', 'STR')
    )
    grammar = {
        'EXPR': a(
            skip('L_PAR'),
            'VALUE', maybe(someof(skip('SEP'), 'VALUE')),
            skip('R_PAR')
        ),
        'VALUE': anyof('STR', 'NUM', 'EXPR')
    }
    parser = Parser(patterns, grammar)
    ast = parser.parse('EXPR', '(1, 2, ("test", (3, 4)))')

    result = Node('EXPR', items=[
        Node('VALUE', [Token('NUM', '1')]),
        Node('VALUE', [Token('NUM', '2')]),
        Node('VALUE', [Node('EXPR', items=[
            Node('VALUE', [Token('STR', '"test"')]),
            Node('VALUE', items=[
                Node('EXPR', items=[
                    Node('VALUE', [Token('NUM', '3')]),
                    Node('VALUE', [Token('NUM', '4')])
                ])
            ])
        ])])
    ])
    assert ast == result

    with pytest.raises(SyntaxError):
        parser.parse('EXPR', '((1, 2, ("test", (3, 4)))')