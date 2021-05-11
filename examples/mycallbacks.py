

def pass_through(*args):
	return args

def render_sum(x, op, y):
    if op == 'plus':
        return x + y
    elif op == 'minus':
        return x - y
    elif op == 'multiply':
        return x*y
    elif op == 'divide':
        return x/y