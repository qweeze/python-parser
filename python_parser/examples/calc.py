import traceback
import readline
import operator as op

from python_parser import Parser, a, anyof, maybe, someof


class InterpreterError(Exception):
    pass

class Interpreter(object):

    def __init__(self):
        self.un_ops = {
            '-': op.neg,
            '+': op.pos
        }
        self.bin_ops = {
            '*': op.mul,
            '/': op.truediv,
            '+': op.add,
            '-': op.sub
        }
        self.vars = {}

    def expr(self, items):
        result = self.visit(next(items))
        op = next(items, None)
        while op is not None:
            result = self.bin_ops[op.value](result, self.visit(next(items)))
            op = next(items, None)
        return result

    def term(self, items):
        return self.expr(items)

    def factor(self, items):
        item = next(items)
        if item.name == 'L_PAR':
            result = self.visit(next(items))
        elif item.name in ('ADD', 'SUB'):
            result = self.un_ops[item.value](self.visit(next(items)))
        elif item.name == 'NAME':
            if item.value not in self.vars:
                raise InterpreterError(
                    'Variable {} is not defined'.format(item.value))
            result = self.vars[item.value]
        else:
            result = float(item.value)
        next(items, None)
        return result

    def defn(self, items):
        name = next(items).value.split('=')[0].rstrip()
        self.vars[name] = self.visit(next(items))

    def skip(self, items):
        return self.visit(next(items))

    def visit(self, node):
        return getattr(self, node.name.lower(), self.skip)(iter(node.items))


tokens = (
    ('(\d*\.\d+)|(\d+\.\d*)', 'FLOAT'),
    ('\d+', 'INT'),
    ('\+', 'ADD'),
    ('-', 'SUB'),
    ('\*', 'MUL'),
    ('/', 'DIV'),
    ('\)', 'R_PAR'),
    ('\(', 'L_PAR'),
    ('\w+\s*=', 'SET'),
    ('\w+', 'NAME'),
    ('=', 'EQ')
)

grammar = {
    'FACTOR': anyof(
        'FLOAT', 'INT', 'NAME',
        a(anyof('ADD', 'SUB'), 'FACTOR'),
        a('L_PAR', 'EXPR', 'R_PAR')),
    'TERM': a('FACTOR', maybe(someof(anyof('DIV', 'MUL'), 'FACTOR'))),
    'DEFN': a('SET', 'EXPR'),
    'EXPR': a('TERM', maybe(someof(anyof('ADD', 'SUB'), 'TERM'))),
    'PROGRAM': anyof('EXPR', 'DEFN')
}

parser = Parser(tokens, grammar)
interpreter = Interpreter()

def calc_eval(text):
    ast = parser.parse('PROGRAM', text)
    return interpreter.visit(ast)


_bold = '\033[;1m{}\033[0;0m'.format
_red = '\033[1;31m{}\033[0;0m'.format

if __name__ == '__main__':
    while True:
        try:
            text = input(_bold('> '))
            if not text:
                continue
            rv = calc_eval(text)
            if rv is not None:
                print(' ', _bold(rv))
        except (KeyboardInterrupt, EOFError):
            exit(0)
        except SyntaxError as exc:
            msg = traceback.format_exception_only(type(exc), exc)
            print(_red(''.join(msg[3:] + msg[1:3])), end='')
        except (ArithmeticError, InterpreterError) as exc:
            print(_red(exc))
