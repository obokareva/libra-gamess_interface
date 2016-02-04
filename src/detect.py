#*********************************************************************************
#* Copyright (C) 2016 Kosuke Sato, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/


# **************************************************************
# This program read the output from Semi-Emipirical Calculation
# where single point calculation is done 
# and GRADIENTS are output.
# **************************************************************

import os
import sys
import math


def detect_columns(l_gam,params):
    #this program detects the columns showing the prameters like
    # coordinates of atoms, gradients acting on atoms,
    # atomic orbitals, eigenenergies and eigenvectors.
    i = -1
    for line in l_gam:
        i += 1
        spline = line.split()

        #if len(spline) == 6 and spline[0] == "TOTAL" and spline[3] == "ATOMS":
            #params["lNatoms"] = i
            #params["Natoms"] = int(spline[5])

        # nGTO
        #if len(spline) == 14 and spline[1] == "GTO" and spline[12] == "STO":
        #    params["lGTO"] = i
        #    params["nGTO"] = int(spline[7])

        # the number of cartesian gaussian basis functions
        if len(spline) == 8 and spline[5] == "FUNCTIONS":
            params["lgbf"] = i
            params["Ngbf"] = int(spline[7])
            #print params["Ngbf"]
            
        # the atomic basis sets
        if len(spline) == 3 and spline[1] == "BASIS" and spline[2] == "SET":
            params["ab_start"] = i + 7
        if len(spline) == 8 and spline[5] == "SHELLS":
            params["ab_end"] = i - 2

        # eigenvectors ( molecular orbitals)
        if len(spline) > 0 and spline[0] == "EIGENVECTORS":
            params["mo_start"] = i + 3
            
            params["mo_end"] = i + 1 + (params["Ngbf"] + 4) * int(math.ceil(params["Ngbf"]/5.0))

        # the coordinates of the atoms (in Bohr)

        if len(spline) == 4 and spline[2] == "COORDINATES" and spline[3] == "(BOHR)":
            params["coor_start"] = i + 2
        if len(spline) == 3 and spline[0] == "INTERNUCLEAR" and spline[1] == "DISTANCES":
            params["coor_end"] = i -2 
            params["Natoms"] = params["coor_end"] - params["coor_start"] + 1

        # the gradients(in Hartree/Bohr)

        if len(spline) == 4 and spline[0] == "GRADIENT" and spline[3] == "ENERGY":
            params["grad_start"] = i + 4
            params["grad_end"] = params["grad_start"] + params["Natoms"] -1

def show_outputs(l_gam,params):
    #print "******************************************"
    #print "according to the",params["lGTO"]+1,"th column,"
    #print l_gam[params["lGTO"]]
    #print "nGTO = ",params["nGTO"]
    #print "*******************************************"
    #print
    print "******************************************"
    print "according to the",params["lgbf"]+1,"th column,"
    print l_gam[params["lgbf"]]
    print "Ngbf = ",params["Ngbf"]
    print "*******************************************"
    print
    print "******************************************"
    print "ATOMIC BASIS SET is within",params["ab_start"]+1,"-",params["ab_end"]+1,"th lines."
    for l in range(params["ab_start"],params["ab_end"]+1):
        print l_gam[l]
    print "******************************************"
    print
    print "******************************************"
    print "MOLECULAR ORBITALS is within",params["mo_start"]+1,"-",params["mo_end"]+1,"th lines"
    for l in range(params["mo_start"],params["mo_end"]+1):
        print l_gam[l]
    print "******************************************"
    print
    print "******************************************"
    print "COORDINATES OF ATOMS (in Bohr) is within",params["coor_start"]+1,"-",params["coor_end"]+1,"th lines"
    for l in range(params["coor_start"],params["coor_end"]+1):
        print l_gam[l]
    print "And the number of atoms is ",params["Natoms"]
    print "******************************************"
    print
    print "******************************************"
    print "GRADIENT (in Hartree/Bohr) is within",params["grad_start"]+1,"-",params["grad_end"]+1,"th lines"
    for l in range(params["grad_start"],params["grad_end"]+1):
        print l_gam[l]
    print "******************************************"
    print

    return

def detect(l_gam,params):
    
    detect_columns(l_gam,params)

    show_outputs(l_gam,params)

    print "*********************************************"
    print "detect program ends"
    print "*********************************************"
    print 