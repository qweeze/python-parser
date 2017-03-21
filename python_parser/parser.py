import re
from collections import namedtuple


Token = namedtuple('Token', ('name', 'value'))
Node = namedtuple('Node', ('name', 'items'))


class Lexer(object):
    """
    A tokenizer that takes a string and produces a sequence of
    `Token` instances. If no match found a SyntaxError is raised.
    """
    def __init__(self, patterns):
        """
        :param patterns: A sequence of (regex_pattern, token_name) tuples.
         Patterns are order dependent: first match wins
        """
        self.patterns = [
            (re.compile(bytes(p, 'utf8')), name) for p, name in patterns]

    def lex(self, raw, ignore_spaces=True):
        """
        :param raw: an input string
        :param ignore_spaces: if True, all whitespace characters are skipped
        :return: generator of tokens
        """
        self.raw = bytearray(raw, 'utf8')
        self.pos = 0
        endpos = len(self.raw)

        while self.pos != endpos:
            if ignore_spaces and self.raw[self.pos: self.pos + 1].isspace():
                self.pos += 1
                continue
            for p, name in self.patterns:
                m = p.match(self.raw[self.pos:])
                if m is not None:
                    val, offset = m.group(), m.end()
                    yield Token(name, str(val, 'utf8'))
                    self.pos += offset
                    break
            else:
                self.error('Illegal character')
        yield Token('EOF', None)

    def error(self, message):
        raise SyntaxError(message, self.get_debug_info())

    def get_debug_info(self, f_name=None):
        pos = self.pos + 1
        raw = self.raw
        line_no = raw[:pos].count(b'\n')
        line_start = max(raw.rfind(b'\n'), 0)
        line_end = max(raw.find(b'\n'), len(raw))
        line = str(raw[line_start:line_end], 'utf-8')
        offset = pos - line_start
        return (f_name, line_no, offset, line)


class Parser(object):
    def __init__(self, tokens, grammar):
        self.lexer = Lexer(tokens)
        self.grammar = grammar
        self.count = 0

    def step(self):
        self.cur_token = next(self.token_generator, None)
        if self.cur_token is not None:
            self.count += 1

    def error(self):
        if self.cur_token.value is not None:
            message = 'Unexpected token {}'.format(self.cur_token.value)
        else:
            message = 'Unexpected EOF'
        self.lexer.error(message)

    def eat(self, token_name):
        if self.cur_token is not None and self.cur_token.name == token_name:
            token = self.cur_token
            self.step()
            return token

    def parse_rule(self, rule):
        return Node(name=rule, items=self.grammar[rule](self))

    def parse(self, rule, text, ignore_spaces=True, check_eof=True):
        self.token_generator = self.lexer.lex(text, ignore_spaces)
        self.cur_token = None
        self.step()
        try:
            result = self.parse_rule(rule)
            if check_eof:
                a('EOF')(self)
        except ParserError:
            self.error()
        else:
            return result


class ParserError(Exception):
    pass


def unify(*args):
    args = (arg if callable(arg) else a(arg) for arg in args)
    return a(*args)


def just(token_name):
    def inner(parser):
        token = parser.eat(token_name)
        if token is None:
            raise ParserError
        return token
    return inner


def maybe(*args):
    def inner(parser):
        cnt = parser.count
        try:
            return unify(*args)(parser)
        except ParserError:
            if parser.count != cnt:
                raise ParserError
    return inner


def skip(*args):
    def inner(parser):
        unify(*args)(parser)
    return inner


def anyof(*args):
    def inner(parser):
        for arg in args:
            result = maybe(arg)(parser)
            if result:
                return result
        raise ParserError
    return inner


def someof(*args):
    def inner(parser):
        result = unify(*args)(parser)
        while True:
            part = maybe(unify(*args))(parser)
            if part:
                result.extend(part)
            else:
                break
        return result
    return inner


def a(*args):
    def inner(parser):
        result = []
        for arg in args:
            if arg in parser.grammar:
                arg = parser.parse_rule(arg)
            if isinstance(arg, str):
                arg = just(arg)
            if callable(arg):
                arg = arg(parser)
            if arg is not None:
                if not isinstance(arg, list):
                    result.append(arg)
                else:
                    result.extend(arg)
        return result
    return inner
