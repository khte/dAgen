#!/usr/bin/env python3
#/****************************************************************************
# dAgen
# Copyright (c) 2022, Kristian Husum Laursen <kristian.h.laursen@gmail.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#****************************************************************************/

#!/usr/bin/env python3
import sys, os
import importlib

def get_args(gen_args):
    # split generator arguments into an args list and a kwargs dictionary
    args = []
    kwargs = {}
    for gen_arg in gen_args:
        if '=' in gen_arg:
            k, v = gen_arg.split('=', 1)
            kwargs[k] = v
        else:
            args.append(gen_arg)
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
    print('usage 1: %s <input.gen>' % sys.argv[0])
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
