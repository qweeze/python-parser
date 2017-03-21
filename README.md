# python-parser
A recursive descent parser generator

[![Build Status](https://travis-ci.org/qweeze/python-parser.svg?branch=master)](https://travis-ci.org/qweeze/python-parser)

### Usage
To create a parser you should provide a sequence of tokens and a BNF-like grammar. Here's a simple example of parsing an expressions with nested parentheses:
```python
from python_parser import Parser, a, anyof, someof, maybe, skip, to_dot

tokens = (
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
string_to_parse = '(1, 2, ("test", ((3), 4)))'

parser = Parser(tokens, grammar)
ast = parser.parse('EXPR', string_to_parse)

with open('ast.dot', 'w') as f:
    f.write(to_dot(ast))

```
After running this code `ast.dot` should contain the following graph:
<p align="center">
  <img src="https://github.com/qweeze/python-parser/raw/master/python_parser/examples/output.png?raw=true" alt="Ast graph"/>
