#!/usr/bin/env python3
#/****************************************************************************
# Functional architecture module
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
    Function for creating the functional specification file. Must be called before
    other functions. Input: filename
    """
    global fname
    fname = filename + ".funcspec"
    file = open(fname, "w")
    file.write("/* Auto-generated function decomposition file made using droneDSL */ \n")
    file.write("function decomposition 1.1 " + filename + "\n\n")
    file.write("/* Default Deviation Hierarchy */ \n")
    file.write("deviation not_available  \"Failure (Function and output not available)\" \n\n")
    file.write("/* Function hierarchy */ \n")
    file.write("function aviate \"Aviate\" system {\n")
    file.write("}\n\n")
    file.write("function navigate \"Navigate\" system {\n")
    file.write("}\n\n")
    file.write("function communicate \"Communicate\" system {\n")
    file.write("}")
    file.close()

def add_functions(*args, **kwargs):
    """
    Function for defining the drone functions.
    If standard layout is wanted, input only std (requires the std functions found in the docstring for drone_components and gcs_components).
    If custom functions are wanted those are input instead. Valid input examples are:
        aviate=Aviate
        navigate=Navigate
        communicate=Communicate
    """

    with open(fname, "r") as f:
        contents = f.readlines()

        if(args[0] == 'std'):
             # 999 to ensure placement last in file.
            contents.insert(999,"function aviate \"Aviate\" system { \n" + \
                                "    function est_alt \"Estimate altitude\" safety \n" + \
                                "    function est_pos \"Estimate position (lat, lon)\" safety \n" + \
                                "    function ctrl_alt \"Control altitude\" safety { \n" + \
                                "        deviations [not_available] \n" + \
                                "        allocations [hd_phy.uas.uav.mr] \n" + \
                                "        function ctrl_mr_thrust \"Control MR thrust\" system \n" + \
                                "    } \n" + \
                                "    function ctrl_lat \"Control lateral position\" safety { \n" + \
                                "        deviations [not_available] \n" + \
                                "        allocations [hd_phy.uas.uav.mr] \n" + \
                                "        function ctrl_mr_att \"Control MR attitude\" system \n" + \
                                "    } \n" + \
                                "} \n\n" + \
                                "function navigate \"Navigate\" system { \n" + \
                                "    function follow_route \"Follow route\" safety \n" + \
                                "} \n\n" + \
                                "function communicate \"Communicate\" system { \n" + \
                                "    function c2 \"C2 link communication\" safety { \n" + \
                                "        eviations [not_available] \n" + \
                                "        llocations [hd_phy.uas.uav.uav_c2, hd_phy.uas.gcs.gcs_c2] \n" + \
                                "    } \n" + \
                                "    function hmi \"Provide HMI for operator\" safety { \n" + \
                                "        deviations [not_available] \n" + \
                                "        allocations [hd_phy.uas.gcs.gcs_hmi] \n" + \
                                "    } \n" + \
                                "function pilot \"Remote pilot control by TX\" safety { \n" + \
                                "    deviations [not_available] \n" + \
                                "    allocations [hd_phy.uas.tx] \n" + \
                                "    } \n" + \
                                "} \n\n" + \
                                "function daa \"Detect And Avoid\" safety { \n" + \
                                "    deviations [not_available] \n" + \
                                "    allocations [hd_phy.uas.uav.daa] \n" + \
                                "    function detect_gaa \"Detect third party general aviation\" safety \n" + \
                                "}")

        else:
            for k in kwargs:
                # insert functions.
                contents.insert(index,  "function " + k + " \"" + kwargs[k] + "\"" + " system {\n" + \
                                        "    deviations [not_available] \n" + \
                                        "} \n\n")

    with open(fname, "w") as f:
        contents = "".join(contents)
        f.write(contents)

def aviate_functions(**kwargs):
    """
    Function for defining the avaiate functions.
    Valid input examples (add all with space in between): \n
        est_alt=Estimate_altitude
        est_pos=Estimate_position
    """
    insert_function("Aviate", **kwargs)

def navigate_functions(**kwargs):
    """
    Function for defining the avaiate functions.
    Valid input examples (add all with space in between): \n
        follow_route=Follow_route
    """
    insert_function("Navigate", **kwargs)

def communicate_functions(**kwargs):
    """
    Function for defining the avaiate functions.
    Valid input examples (add all with space in between): \n
        c2=C2_link_communication
        hmi=Human_machince_interface
    """
    insert_function("Communicate", **kwargs)

def allocate(**kwargs):
    """
    """
    with open(fname, "r") as f:
        contents = f.readlines()

        for k in kwargs:
            i = 0
            index = 0
            for line in contents:
                i = i + 1
                if k in line:
                    index = i
                    break
            contents.insert(index, "        allocations [" + kwargs[k] + "]\n")

    write_to_file(contents)

def insert_function(hej, **kwargs):
    start_keyword = hej
    i = 0
    index = 0

    with open(fname, "r") as f:
        contents = f.readlines()

        # find the keyword to insert module after it.
        for line in contents:
            i = i + 1
            if start_keyword in line:
                index = i
                break

        for k in kwargs:
            # insert uav components.
            contents.insert(index,  "    function " + k + " \"" + kwargs[k] + "\"" + " system {\n" + \
                                    "        deviations [not_available]\n" + \
                                    "    }\n")

    write_to_file(contents)

def write_to_file(contents):
    with open(fname, "w") as f:
        contents = "".join(contents)
        f.write(contents)
