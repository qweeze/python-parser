import pytest
from examples.calc import parser, interpreter, InterpreterError


def test_calc():

    interpreter.visit(parser.parse('PROGRAM', 'a = 11'))
    interpreter.visit(parser.parse('PROGRAM', 'b = -13'))
    a, b = 11, -13

    samples = (
        '2+2',
        '(((23 + -3.2)) / 34+(2*((3)) *(3.0 - .1)))',
        '0.000',
        'a * b - 123'
    )

    for i in samples:
        assert interpreter.visit(parser.parse('PROGRAM', i)) == eval(i)

    with pytest.raises(ZeroDivisionError):
        interpreter.visit(parser.parse('PROGRAM', '1 / 0'))

    with pytest.raises(InterpreterError):
        interpreter.visit(parser.parse('PROGRAM', '1 + undefined'))
