from Classes.Marker_class import Marker
from Classes.Object_class import Object

# Constants
SAFETY_MOVE_HEIGHT = 200
MEASUREMENT_ERR = 10

zero_ids = [0, 1, 2]
electronic_self_ids = [3, 4]
# Markers
# zero markers
Zero_marker0 = Marker(0, None, 25, name="zero_0")
Zero_marker1 = Marker(1, None, 25, name="zero_X")
Zero_marker2 = Marker(2, None, 25, name="zero_Y")

# markers
Wheel1_marker0 = Marker(10, None, 40, name="Left_front")
Wheel1_marker1 = Marker(11, None, 40, name="Left_front")
Wheel2_marker0 = Marker(12, None, 40, name="Right_front")
Wheel2_marker1 = Marker(13, None, 40, name="Right_front")
Wheel3_marker0 = Marker(14, None, 40, name="Left_back")
Wheel3_marker1 = Marker(15, None, 40, name="Left_back")
Wheel4_marker0 = Marker(16, None, 40, name="Right_back")
Wheel4_marker1 = Marker(17, None, 40, name="Right_back")

Electronic_marker0 = Marker(18, None, 40, name="Electronic_front")
Electronic_marker1 = Marker(19, None, 40, name="Electronic_back")

Electronic_self_marker0 = Marker(3, None, 40, name="Self_electronic_front")
Electronic_self_marker1 = Marker(4, None, 40, name="Self_electronic_back")

Main_base_marker1 = Marker(20, None, 40, name="Main_base_front")
Main_base_marker2 = Marker(21, None, 40, name="Main_base_back")

Car_cap_marker1 = Marker(22, None, 40, name="Car_cap_front")
Car_cap_marker2 = Marker(23, None, 40, name="Car_cap_back")


# OBJECTS
# Platform
Car_cap = Object(Car_cap_marker1, Car_cap_marker2, 131.5, None)
Electronic_module = Object(Electronic_marker0, Electronic_marker1, 75, None)

Wheel_front_left = Object(Wheel1_marker0, Wheel1_marker1, 89, None)
Wheel_front_right = Object(Wheel2_marker0, Wheel2_marker1, 89, None)
Wheel_back_left = Object(Wheel3_marker0, Wheel3_marker1, 89, None)
Wheel_back_right = Object(Wheel4_marker0, Wheel4_marker1, 89, None)

'''
       car front
           |
           v
           
     ___       ___
    |L_F|     |R_F|
      
      
      
     ___       ___
    |L_B|     |R_B|
'''
# ---------------------------------------------------------------------------------------------------#