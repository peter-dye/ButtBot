import math

CAM_HEIGHT = 100        #Camera height off of ground in cm
CAM_ANGLE_D = 15        #Angle of Camera pitch servo, Servo[2] in degrees
CAM_OFFSET = 10         #Distance between straight below camera to center of collection arm nozzle in cm

CAM_ANGLE_R = (CAM_ANGLE_D * math.pi)/180                                        #Angle of Camera pitch servo, Servo[2] in radians
relative_dist  = round(((CAM_HEIGHT * math.tan(CAM_ANGLE_R)) - CAM_OFFSET) , 2)  #Linear distance between center of nozzle to detected butt in cm
