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

fname = ""
# keys = []

def create_physarch(filename):
    """
    Function for creating the physical architecture file. Must be called before
    other functions. Input: filename
    """
    global fname
    fname = filename + ".physarch"
    file = open(fname, "w")
    file.write("/* Auto-generated physical architecture file  made using droneDSL */ \n\n")
    file.write("physical decomposition 1.1 " + filename + "\n\n")
    file.write("component uas \"Unmanned Aerial System\" system {\n")
    file.write("}")
    file.close()

def drone_components(**kwargs):
    """
    Function for defining the drone components.
    Valid input examples (add all with space in between): \n
        mr=Multirotor
        fc=Flight_controller
        pwr=Power_system
        uav_c2=UAV_C2_link
        daa=DAA_system
    """

    # global keys
    start_bracket = "{"
    i = 0
    index = 0

    with open(fname, "r") as f:
        contents = f.readlines()

        # find the first start bracket to insert module after it.
        for line in contents:
            i = i + 1
            if start_bracket in line:
                index = i
                break

        for k in kwargs:
            # insert uav components.
            contents.insert(index,  "    component " + k + " \"" + kwargs[k] + "\"" + " system {\n" + \
                                    "      failure modes [" + k + "_fail " + "\"" + kwargs[k] + " failure\"]\n" +
                                    "    }\n")
        contents.insert(index, "  component uav \"Unmanned Aerial Vehicle\" system {\n")

    with open(fname, "w") as f:
        contents = "".join(contents)
        f.write(contents)

def gcs_components(**kwargs):
    """
    Function for defining the GCS components.
    Valid inputs consist of a keyword and a description, with a space in between
    each pair.

    Examples : \n
        hmi=Human_machince_interface
        gcs_c2=GCS_C2_link
        pwr=Power_supply
    """

    # global keys
    start_bracket = "{"
    i = 0
    index = 0

    with open(fname, "r") as f:
        contents = f.readlines()

        # find the first start bracket to insert module after it.
        for line in contents:
            i = i + 1
            if start_bracket in line:
                index = i
                break

        for k in kwargs:
            # insert gcs components.
            contents.insert(index,  "    component " + k + " \"" + kwargs[k] + "\"" + " system {\n" + \
                                    "      failure modes [" + k + "_fail " + "\"" + kwargs[k] + " failure\"]\n" +
                                    "    }\n")
        contents.insert(index, "  component gcs \"Ground Control System\" system {\n")

    with open(fname, "w") as f:
        contents = "".join(contents)
        f.write(contents)

def transmitter(bool):
    if bool:
        start_bracket = "{"

        i = 0
        index = 0

        with open(fname, "r") as f:
            contents = f.readlines()

            # find the first start bracket to insert module after it.
            for line in contents:
                i = i + 1
                if start_bracket in line:
                    index = i
                    break
            # insert transmitter component.
            contents.insert(index,  "  component tx \"Transmitter\" system {\n" + \
                                    "    failure modes [tx_loss \"TX_communication_loss\"]\n" + \
                                    "  }\n")
        with open(fname, "w") as f:
            contents = "".join(contents)
            f.write(contents)
