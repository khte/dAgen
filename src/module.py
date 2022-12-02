def add_str(*args, **kwargs):
    """Function for adding strings. Input: strings separated by a space"""
    kwargs_list = ['%s=%s' % (k, kwargs[k]) for k in kwargs]
    print(''.join(args), ','.join(kwargs_list))

def add_num(*args, **kwargs):
    """Function for adding numbers. Input: numbers separated by a space. End with type=int/float"""
    t = globals()['__builtins__'][kwargs['type']]
    print(sum(map(t, args)))
