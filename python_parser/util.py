import uuid
from .parser import Token, Node


def to_dot(ast):
    result = [
        'strict digraph "AST" {',
        'size="16,14"; ratio = fill;'
    ]
    _escape = lambda s: s.replace('"', r'\"')
    
    def format_node(node, uid):
        if isinstance(node, Token):
            label = '{} [{}]'.format(*map(_escape, (node.name, node.value)))
        elif isinstance(node, Node):
            label = '{}'.format(*map(_escape, (node.name,)))
        else:
            raise ValueError("Can't format node {}".format(node))
        return '"{}" [label="{}"];'.format(uid, label)

    def walk(node, uid):
        result.append(format_node(node, uid))
        if isinstance(node, Node):
            for i in node.items:
                child_uid = uuid.uuid4().hex
                walk(i, child_uid)
                result.append('"{}" -> "{}";'.format(uid, child_uid))

    uid = uuid.uuid4().hex
    walk(ast, uid)
    result.append('}')
    return '\n'.join(result)
