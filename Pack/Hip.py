from math import *

height = float(input('Enter Height'))
hypot1 = float(input('Enter Hypothnuese One'))

pitch1 = asin(height/hypot1)    #soh

adj1 = cos(asin(height/hypot1)) * hypot1    #cah

print ("Pitch for part one is " , (pitch1  * 180) / pi ,"deg")
print ("Adj for part one is " , adj1)

hypot2 = float(input('Enter Hypot for area 2'))

pitch2 = (asin(height/hypot2) * 180) / pi

print ("Pitch for part two is " , pitch2 ,"deg")

hip_angle = int(input("Enter Hip angle on plan"))

hyp_hip = adj1 / sin(radians(hip_angle))  #soh

pitch_hip = atan(height/hyp_hip)

print ("/n Pitch of Hip is " , degrees(pitch_hip))

print ("Length of hip is ", sqrt(height*height + hyp_hip*hyp_hip))

#soh cah toa