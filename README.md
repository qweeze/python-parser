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

### More examples
[Calculator](python_parser/examples/calc.py)
<pre>
> (((23 + -3.2)) / 34+(2*((3)) *(3.0 - .1)))
  <b>17.98235294117647</b>
> 1/0
  <b>float division by zero</b>
> a = 11
> b = -6
> a * b
  <b><red>-66.0</red></b>
> 
</pre>
[JSON parser](python_parser/examples/json_parser.py)
```python
>>> from python_parser.examples.json_parser import load as json_loads
>>> json_string = '{"first": [1, 2, 3, {"5": 6}, true], "key": "value", "1": 2}'
>>> result = json_loads(json_string)
>>> type(result)
builtins.dict
>>> result['first'][3]['5']
6
```
