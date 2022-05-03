from dronekit import connect,VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time 
import socket
import exceptions
import argparse

####Function definitions for mission

####Function to connect this script to pixhawk firmware
def connectMyCopter():
    parser = argparse.ArgumentParser(description = 'commands')
    parser.add_argument('--connect')
    args = parser.parse_args()
    connection_string = args.connect
    vehicle = connect(connection_string, wait_ready = True)
    return vehicle

####Function to arm the drone and takeoff
def arm_and_takeoff(aTargetAtlitude):
    while not vehicle.is_armable:
        print("waiting for vehicle to be armable")
        time.sleep(1)

    #switch vehicle to GUIDED mode and wait for change
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode != "GUIDED":
	    print("Waiting for vehicle to enter GUIDED mode")
            time.sleep(1)

    #arm vehicle once GUIDED mode is confirmed
    vehicle.armed = True
    while vehicle.armed == False:
        print("Waiting for vehicle to become armed")
        time.sleep(1)
    
    vehicle.simple_takeoff(aTargetAtlitude)
    
    prev_altitude = None
    while True:
        curr_altitude = vehicle.location.global_relative_frame.alt
        print("Current Altitude : %d" %curr_altitude) #target altitude comparison
        if curr_altitude >= aTargetAtlitude* 0.95 :
            break
        if curr_altitude == prev_altitude :
            break
        else : prev_altitude = curr_altitude
        time.sleep(1)
    print("Target altitude reached")
    return None

####Mission

vehicle = connectMyCopter()
print("About to takeoff...")

vehicle.mode=VehicleMode("GUIDED")
arm_and_takeoff(2) #Tell drone to fly 2 meters in the sky
vehicle.mode = VehicleMode("LAND") # Once drone reaches altitude, tell it to land

time.sleep(2)

print("End of function")
print("Arducopter version :%s" %vehicle.version)

while True :
	time.sleep(2)

vehicle.close()
