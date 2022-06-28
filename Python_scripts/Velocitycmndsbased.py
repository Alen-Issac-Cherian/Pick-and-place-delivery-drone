from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import socket
import exceptions


# Set up option parsing to get connection string
import argparse

#Function to connect script to copter
def connectMyCopter() :
	parser = argparse.ArgumentParser(description='Commands')
	parser.add_argument('--connect')
	args = parser.parse_args()

	connection_string = args.connect
	vehicle = connect(connection_string, wait_ready=True)

return vehicle


#Definition to arm the drone and takeoff


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    while vehicle.mode! = VehicleMode("GUIDED"):
	print("Waiting for vehicle to enter guided mode")
	time.sleep(1)
	
    # Arming after confirming guided mode
    vehicle.armed = True
    vehicle.channels.overrides['3']= 1500
    # Confirm vehicle armed before attempting to take off
    while vehicle.armed==False:
        print(" Waiting for arming...")
        time.sleep(1)
    
    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
def set_velocity_body(Vx,Vy,Vz) :
	
	msg = vehicle.message_factory.net_position_target_local_ned_encode(
		0,
		0,0
		mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
		0b0000111111000111, #bitmask
		0,0,0, #position
		Vx,Vy,Vz, #velocity
		0,0,0, #accelaration
		0,0)
	vehicle.send_mavlink(msg)
	vehicle.flush()

####################################

vehicle=connectMyCopter()
print("About to takeoff...")

arm_and_takeoff(2)

c=0
 
while c<2:
	set_velocity_body(1,0,0)
	print("Heads 1 unit north")
	time.sleep(1)
	c=c+1

time.sleep(2)

c=0

while c<2
	set_velocity_body(-1,0,0)
	print("Heads 1 unit south")
	time.sleep(1)
	c=c+1
time.sleep(2)

vehicle.mode=VehicleMode("RTL")


print("End of function")


while True:
	time.sleep(2)
vehicle.close()
