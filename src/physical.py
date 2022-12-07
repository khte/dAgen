#!/usr/bin/env python3
#/****************************************************************************
# Physical architecture module
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

debug = False

fname = "" # the file name, global to be accessible by all funtions. Future work: classes!

def create_physarch(filename):
    """
    Function for creating the physical architecture file. Must be called before
    other functions. If a file with the same name exists it is overwritten.
    Input: filename without extension.
    """
    global fname
    fname = filename + ".physarch"
    f = open(fname, "w")
    # write start text plus outer wrapper component uas to empty file
    f.write("/* Auto-generated physical architecture file  made using dAgen */ \n\n")
    f.write("physical decomposition 1.1 " + filename + "\n\n")
    f.write("component uas \"Unmanned_aerial_system\" system {\n")
    f.write("}")
    f.close()

def load_physarch(filename):
    global fname
    fname = filename + ".physarch"
    try:
        f = open(fname, "r")
        f.close()

    except Exception as e:
        print(e)

def add_component(*args, **kwargs):
    """
    Function for adding component. If the root component does not exist, it is created.
    Input: [root component key] [root component descriptor] [component=descriptor component=descriptor (add as many as desired)]
    If no components except the root component is defined, and it does not already exist, an empty root component is created.
    """
    if(len(args) > 2):
        print("[Error] More than one root component and descriptor defined: " + str(args))
    elif(len(args) < 2):
        print("[Error] No root component with descriptor defined")
    else:
        try:
            f = open(fname, "r")
            contents = f.readlines()
        except:
            print("[Error] Could not add functions. File does not exist")

        # iterator and check
        i = 0
        root_not_found = 1

        # tabs for proper indentation
        tab = "    "
        tabs = 2

        # container for already existing keys
        existing_keys = []

        # look through file for root component
        for line in contents:
            i = i + 1
            # if(root_not_found):
            if args[0] in line:
                if(debug):
                    print("Root component found on line: " + str(i))
                # compute indents based on root component indentation
                indents = line.index(args[0]) - 6
                tabs = int(indents / 4)
                # find end of component to know when to stop looking for subcomponents
                indents = tab * (tabs - 1)
                end_of_component = indents + "}"
                # set flag and index
                root_not_found = 0
                break

        # if root component was found, find end of component line
        if not(root_not_found):
            j = 0
            for line in contents:
                j = j + 1
                if j > i and line.startswith(end_of_component):
                    break

            # check if input keys already exist in the root component
            x = 0
            for line in contents:
                x = x + 1
                # only check in the specific component, allowing for identical across components
                if(x > i and x < j):
                    for k in kwargs:
                        check = "component " + k
                        if check in line:
                            existing_keys.append(k)

        # if the root component does not exist, add end bracket for it
        if(root_not_found):
            contents.insert(i - root_not_found, tab + "}\n")

        # insert uav components.
        for k in kwargs:
            # if key already exists, don't insert, obviously
            if k not in existing_keys:
                contents.insert(i - root_not_found, tab*tabs + "component " + k + " \"" + kwargs[k] + "\"" + " system {\n" + \
                                        tab*(tabs + 1) + "failure modes [" + k + "_fail " + "\"" + kwargs[k] + " failure\"]\n" + \
                                        tab*tabs + "}\n")

        # if the root component does not exist, create it.
        if(root_not_found):
            contents.insert(i - root_not_found, tab + "component " + args[0] + " \"" + args[1] + "\" system {" + "\n")

        write_to_file(contents)

def write_to_file(contents):
    with open(fname, "w") as f:
        contents = "".join(contents)
        f.write(contents)
        f.close()
