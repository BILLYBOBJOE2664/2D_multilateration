#!/usr/bin/python

import math
import numpy as np

# This script uses the equations described here:
# https://en.wikipedia.org/wiki/Multilateration#math_4
# https://stackoverflow.com/a/2188606

# Get Receival times at the 3 mics A, B, C
mic_a = input("Enter Receival time at A: ")
mic_b = input("Enter Receival time at B: ")
mic_c = input("Enter Receival time at C: ")

# Get Positions of the 3 mics at A, B, C
# TODO: These values must be set as constants
# pos_a = [x1, y1]
# pos_b = [x2, y2]
# pos_c = [x3, y3]
vector_a = [0, 0, mic_a]
vector_b = [30, 30, mic_b]
vector_c = [-30, 30, mic_c]

#-------------------------Constants---------------------------------------------
# Speed of sound
# TODO: Have a separate function to calculate this. It should consider the
# temperature and the humidity of air
# value in metres per second (m/s)
SOUND_VELOCITY = 340.0

# value in metres (m)
ONE_DEG_LAT_EQUATOR = 110540

# value in metres (m)
ONE_DEG_LONG_EQUATOR = 111320

# LAT/ LONG of Kirigalpotta trailhead - Horton Plains NP
origin_lat_long_arr = [6.801746, 80.806442]

#-------------------------Function Definitions----------------------------------

# These functions find the coefficients of the Simlutaneous equations that must
# be solved to find sound source (x, y)

def calculate_COF_A(node_arr, origin_arr):
    A = (2*node_arr[0]/SOUND_VELOCITY*node_arr[2]) - (2*origin_arr[0]/SOUND_VELOCITY*origin_arr[2])
    return A

def calculate_COF_B(node_arr, origin_arr):
    B = (2*node_arr[1]/SOUND_VELOCITY*node_arr[2]) - (2*origin_arr[1]/SOUND_VELOCITY*origin_arr[2])
    return B

# NOTE: Kept only for consistency. This is the function that calculate the Z axis values. Since this is a
# 2D Multilateration, Z axis is ignored; hence returns 0. In case of 3D Multilateration
# use the same equation as calculate_CONST_B() chaging the array Indices
# to match the Z values
def calculate_COF_C(node_arr, origin_arr):
    return 0

def calculate_COF_D(node_arr, origin_arr):
    D = (SOUND_VELOCITY*node_arr[2] - SOUND_VELOCITY*origin_arr[2]) - ((node_arr[0]**2 + node_arr[1]**2 + 0)/SOUND_VELOCITY*node_arr[2]) + ((origin_arr[0]**2 + origin_arr[1]**2 + 0)/SOUND_VELOCITY*origin_arr[2])
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
cof_a1 = calculate_COF_A(vector_b, vector_a)
cof_b1 = calculate_COF_B(vector_b, vector_a)
cof_c1 = calculate_COF_C(vector_b, vector_a)
cof_d1 = calculate_COF_D(vector_b, vector_a)

# Coefficients of Simlutaneous equation 2
cof_a2 = calculate_COF_A(vector_c, vector_a)
cof_b2 = calculate_COF_B(vector_c, vector_a)
cof_c2 = calculate_COF_C(vector_c, vector_a)
cof_d2 = calculate_COF_D(vector_c, vector_a)

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

print "x_src: ", x_src
print "y_src: ", y_src

print "altans: ", altans

print "Angle to X axis: ", angle_to_x_axis
print str(sound_src_pos).strip('[]')
