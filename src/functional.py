#!/usr/bin/env python3
#/****************************************************************************
# Functional specification module
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

fname = ""

def create_funcspec(filename):
    """
    Function for creating the functional decomposition file. Must be called before
    other functions. If a file with the same name exists it is overwritten.
    Input: filename without extension.
    """
    global fname
    fname = filename + ".funcspec"
    f = open(fname, "w")
    f.write("/* Auto-generated functional specification file made using dAgen */ \n")
    f.write("function decomposition 1.1 " + filename + "\n\n")
    f.write("/* Default Deviation Hierarchy */ \n")
    f.write("deviation not_available  \"Failure (Function and output not available)\" \n\n")
    f.write("/* Function hierarchy */ \n")
    f.close()

def load_funcspec(filename):
    """
    Function for loading the functional specification file. Must be called before
    other functions, if create_funcspec is not used.
    Input: filename without extension.
    """
    global fname
    fname = filename + ".funcspec"
    try:
        f = open(fname, "r")
        f.close()

    except Exception as e:
        print(e)

def add_function(*args, **kwargs):
    if(len(args) > 2):
        print("[Error] More than one root function and descriptor defined: " + str(args))
    elif(len(args) < 2):
        print("[Error] No root function with descriptor defined")
    else:
        try:
            f = open(fname, "r")
            contents = f.readlines()
        except:
            print("[Error] Could not add function. File does not exist")

        # iterator and check
        i = 0
        root_not_found = 1

        # tabs for proper indentation
        tab = "    "
        tabs = 1

        # container for already existing keys
        existing_keys = []

        # look through file for root component
        for line in contents:
            i = i + 1
            # if(root_not_found):
            if args[0] in line:
                # compute indents based on root component indentation
                indents = line.index(args[0]) - 6
                tabs = int(indents / 4)
                # find end of component to know when to stop looking for subcomponents
                indents = tab * (tabs - 1)
                end_of_function = indents + "}"
                # set flag and index
                root_not_found = 0
                break

        # if root component was found, find end of component line
        if not(root_not_found):
            j = 0
            for line in contents:
                j = j + 1
                if j > i and line.startswith(end_of_function):
                    break

            # check if input keys already exist in the root component
            x = 0
            for line in contents:
                x = x + 1
                # only check in the specific component, allowing for identical across components
                if(x > i and x < j):
                    for k in kwargs:
                        check = "function " + k
                        if check in line:
                            existing_keys.append(k)

        # if the root component does not exist, add end bracket for it
        if(root_not_found):
            contents.insert(i, "}\n\n")

        # insert uav components.
        for k in kwargs:
            # if key already exists, don't insert, obviously
            if k not in existing_keys:
                contents.insert(i, tab*tabs + "function " + k + " \"" + kwargs[k] + "\"" + " system {\n" + \
                                        tab*(tabs + 1) + "deviations [not_available] \n" + \
                                        tab*tabs + "}\n")

        # if the root component does not exist, create it.
        if(root_not_found):
            contents.insert(i, "function " + args[0] + " \"" + args[1] + "\" system {" + "\n")

        write_to_file(contents)

def allocate(**kwargs):
    """
    Function for allocating functions to physcial components from the physical architecture.
    Valid input:
    [function]=[allocation]
    """

    tab = "    "

    with open(fname, "r") as f:
        contents = f.readlines()

        for k in kwargs:
            i = 0
            index = 0
            for line in contents:
                i = i + 1
                if k in line:
                    indents = line.index(k) - 5
                    tabs = int(indents / 4)
                    index = i
                    break
            contents.insert(index, tab*tabs + "allocations [" + kwargs[k] + "]\n")

    write_to_file(contents)

def write_to_file(contents):
    with open(fname, "w") as f:
        contents = "".join(contents)
        f.write(contents)
