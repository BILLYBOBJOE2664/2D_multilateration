#!/usr/bin/python
import time
import math
import numpy as np
import sys
from TDOA.echo_delay import tdoa

print ("Start time: "+ time.strftime("%H:%M:%S"))

# This script uses the equations described here:
# https://en.wikipedia.org/wiki/Multilateration#math_4
# https://stackoverflow.com/a/2188606
# https://msi.nga.mil/MSISiteContent/StaticFiles/Calculators/degree.html

#-------------------------Notes-------------------------------------------------
# NOTE: Mention all bugs and future work needed here

# BUG: Float div by zero error comes when all time inputs are equal (OPEN)
# BUG: Longitude of the calculated coordinates is only accurate upto 1st decimal.
#      It should be accurate upto 3 decimals at least.
#      Suspected Reason: The constants are measured at the equator. The given
#      Origin is at a point above the equator. Hence calculate suitable constants
#      for the position and see. (OPEN)


#-------------------------Constants---------------------------------------------
# Speed of sound
SOUND_VELOCITY = 340.0 # TODO: Have a separate function to calculate this.

# value in metres (m)
ONE_DEG_LAT_EQUATOR = 110574 # prev: 110540

# value in metres (m)
ONE_DEG_LONG_EQUATOR = 111320

# LAT/ LONG of Kirigalpotta trailhead - Horton Plains NP
# TODO: Set this to the origin's coordinates in the actual site
origin_lat_long_arr = [6.801746, 80.806442]

#-------------------------Inputs------------------------------------------------

# Uncomment only one method as needed for testing

# MANUAL_TESTING_BY_TIME-----------------------------------------------------
# Get Receival times at the 3 mics A, B, C
# mic_a = input("Enter Receival time at A: ")
# mic_b = input("Enter Receival time at B: ")
# mic_c = input("Enter Receival time at C: ")
# mic_d = input("Enter Receival time at D: ")

# MANUAL_TESTING_BY_PROVIDING_UNKNOWN_COORDINATE-----------------------------
# sound_src_x = input("Enter Sound Source X: ")
# sound_src_y = input("Enter Sound Source Y: ")
#
# mic_a = round(math.hypot((sound_src_x - 0), (sound_src_y - 0))/ SOUND_VELOCITY, 4)
# mic_b = round(math.hypot((sound_src_x - 100), (sound_src_y - 0))/ SOUND_VELOCITY, 4)
# mic_c = round(math.hypot((sound_src_x - 0), (sound_src_y - 100))/ SOUND_VELOCITY, 4)
# mic_d = round(math.hypot((sound_src_x - 100), (sound_src_y - 100))/ SOUND_VELOCITY, 4)

# Get Positions of the 3 mics at A, B, C
# TODO: These values must be set as constants
# pos_a = [x1, y1]
# pos_b = [x2, y2]
# pos_c = [x3, y3]

mic_a = sys.argv[1]
mic_b = sys.argv[2]
mic_c = sys.argv[3]
mic_d = sys.argv[4]

vector_a = [0, 0, mic_a]
vector_b = [100, 0, mic_b]
vector_c = [0, 100, mic_c]
vector_d = [100, 100, mic_d]

#-------------------------Function Definitions----------------------------------

# These functions find the coefficients of the Simlutaneous equations that must
# be solved to find sound source (x, y)

# DONE: Integrated TDOA calculation
def calculate_v_tau(node_time, origin_time):
    # return (SOUND_VELOCITY*node_time - SOUND_VELOCITY*origin_time)
    return (SOUND_VELOCITY * tdoa(node_time, origin_time))

def calculate_COF_A(node_arr, origin_arr, node_1_arr):
    A = (2*node_arr[0]/calculate_v_tau(node_arr[2], origin_arr[2])) - (2*node_1_arr[0]/calculate_v_tau(node_1_arr[2], origin_arr[2]))
    return A

def calculate_COF_B(node_arr, origin_arr, node_1_arr):
    B = (2*node_arr[1]/calculate_v_tau(node_arr[2], origin_arr[2])) - (2*origin_arr[1]/calculate_v_tau(node_1_arr[2], origin_arr[2]))
    return B

# NOTE: Kept only for consistency. This is the function that calculate the Z axis values. Since this is a
# 2D Multilateration, Z axis is ignored; hence returns 0. In case of 3D Multilateration
# use the same equation as calculate_CONST_B() chaging the array Indices
# to match the Z values
def calculate_COF_C(node_arr, origin_arr, node_1_arr):
    return 0

def calculate_COF_D(node_arr, origin_arr, node_1_arr):
    D = calculate_v_tau(node_arr[2], origin_arr[2]) - calculate_v_tau(node_1_arr[2], origin_arr[2]) - ((node_arr[0]**2 + node_arr[1]**2 + 0)/calculate_v_tau(node_arr[2], origin_arr[2])) + ((node_1_arr[0]**2 + node_1_arr[1]**2 + 0)/calculate_v_tau(node_1_arr[2], origin_arr[2]))
    return D

def find_sound_lat_long(origin_lat_long_arr, x_sound_src, y_sound_src):
    delta_lat = y_sound_src/ONE_DEG_LAT_EQUATOR
    delta_long = x_sound_src/(ONE_DEG_LONG_EQUATOR * math.cos(math.radians(origin_lat_long_arr[1])))

    src_lat  = origin_lat_long_arr[0] + delta_lat
    src_long = origin_lat_long_arr[1] + delta_long

    sound_src_pos_lat_long = [src_lat, src_long]
    return sound_src_pos_lat_long

#-------------------------Main Program------------------------------------------

# Two Simlutaneous equations of the form xAi + yBi + zCi(==0) + Di = 0 is obtained
# Solving these would give the sound source (x, y) relative to the considered
# origin node, which in this program is always Node a (represented by vector_a)

# Coefficients of Simlutaneous equation 1
cof_a1 = calculate_COF_A(vector_c, vector_a, vector_b)
cof_b1 = calculate_COF_B(vector_c, vector_a, vector_b)
cof_c1 = calculate_COF_C(vector_c, vector_a, vector_b)
cof_d1 = calculate_COF_D(vector_c, vector_a, vector_b)

# Coefficients of Simlutaneous equation 2
cof_a2 = calculate_COF_A(vector_d, vector_a, vector_b)
cof_b2 = calculate_COF_B(vector_d, vector_a, vector_b)
cof_c2 = calculate_COF_C(vector_d, vector_a, vector_b)
cof_d2 = calculate_COF_D(vector_d, vector_a, vector_b)

# print cof_a1
# print cof_b1
# print cof_c1
# print cof_d1
#
# print cof_a2
# print cof_b2
# print cof_c2
# print cof_d2

# By simplifying the equations xA1 + yB1 + D1 = 0 & xA2 + yB2 + D2 = 0
# It can be found that,
# x_src = ((cof_b1/cof_b2)*cof_d2 - cof_d1)/(cof_a1 - ((cof_b1*cof_a2)/cof_b2))
# and
# y_src = -1*(cof_a2*x_src + cof_d2)/cof_b2

# where x_src and y_src are the cartesian coordinates of the sound source relative
# relative to the origin node, which in this program is
# always Node a (represented by vector_a)

x_src = ((cof_b1/cof_b2)*cof_d2 - cof_d1)/(cof_a1 - ((cof_b1*cof_a2)/cof_b2))

y_src = -1*(cof_a2*x_src + cof_d2)/cof_b2

angle_to_x_axis = math.degrees(math.atan(y_src/x_src))

sound_src_pos = find_sound_lat_long(origin_lat_long_arr, x_src, y_src)

# alt1 = np.array([[cof_a1,cof_b1],[cof_a2,cof_b2]])
# alt2 = np.array([-cof_d1, -cof_d2])
# altans = np.linalg.solve(alt1,alt2)
# print "altans: ", altans

print "x_src: ", round(x_src, 4)
print "y_src: ", round(y_src, 4)
print str(sound_src_pos).strip('[]')

print ("End time: "+ time.strftime("%H:%M:%S"))

# ----------Uncomment for testing only------------------
# print "Accuracy X: ", round((x_src/sound_src_x)*100, 4)
# print "Accuracy Y: ", round((y_src/sound_src_y)*100, 4)
# print "Difference percentage in X: ", round(round((x_src/sound_src_x)*100, 4) - 100, 4)
# print "Difference percentage in Y: ", round(round((y_src/sound_src_y)*100, 4) - 100, 4)
# print "Angle to X axis: ", angle_to_x_axis
# print str(sound_src_pos).strip('[]')
