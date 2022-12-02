#!/usr/bin/env python3
import sys, os
import importlib

def get_args(dsl_args):
    # split DSL arguments into an args list and a kwargs dictionary
    args = []
    kwargs = {}
    for dsl_arg in dsl_args:
        if '=' in dsl_arg:
            k, v = dsl_arg.split('=', 1)
            kwargs[k] = v
        else:
            args.append(dsl_arg)
    return args, kwargs

def get_help(module_name):
    mod = importlib.import_module(module_name)
    print(mod.__doc__ or '')
    for name in dir(mod):
        if not name.startswith('_'):
            attr = getattr(mod, name)
            print(attr.__name__)
            print(attr.__doc__ or '', '\n')

# input file is added as argument to the script
if len(sys.argv) != 2:
    print('usage 1: %s <input.dsl>' % sys.argv[0])
    print('usage 2: %s help=<module_name>' % sys.argv[0])
    sys.exit(1)

# path to root folder of this file (where modules are also stored)
sys.path.append(os.getcwd())

# parse input file or help request
if sys.argv[1].startswith('help='):
    get_help(sys.argv[1][5:])
else:
    with open(sys.argv[1], 'r') as input:
        for line in input:
            line = line.strip()
            # ignore comments
            if not line or line[0] == '#':
                continue
            elements = line.split()
            # print(elements)

            # import module(s) at runtime
            mod = importlib.import_module(elements[0])
            # print(mod)
            args, kwargs = get_args(elements[2:])
            getattr(mod, elements[1])(*args, **kwargs)
