from dronekit import connect,VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time 
import socket
import exceptions
import argparse

###Function definitions for mission

###Function to connect this script to pixhawk firmware
def connectMyCopter():
    parser = argparse.ArgumentParser(description = 'commands')
    parser.add_argument('--connect')
    args = parser.parse_args()
    connection_string = args.connect
    vehicle = connect(connection_string, wait_ready = True)
    return vehicle

###Function to arm the drone and takeoff
def arm_and_takeoff(aTargetAlitude):
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
    
    vehicle.simple_takeoff(aTargetAltitude)
   
    while True:
        print("Current Altitude : %d" %vehicle.location.global_relative_frame.alt) #target altitude comparison
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude* 0.95 :
         break
        time.sleep(1)
    print("Target altitude reached")
    return None



def goto(dNorth, dEast, gotoFunction=vehicle.simple_goto):
	# Moves the vehicle to a position dNorth metres North and dEast metres East of the current position.

    currentLocation = vehicle.location.global_relative_frame
    targetLocation = get_location_metres(currentLocation, dNorth, dEast)
    targetDistance = get_distance_metres(currentLocation, targetLocation)
    gotoFunction(targetLocation)
    while vehicle.mode.name=="GUIDED":
   	remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        print("Distance to target: ", remainingDistance)
        if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
            print("Reached target")
            break;
        time.sleep(2)
    time.sleep(1)




###Mission

vehicle = connectMyCopter()
print("About to takeoff...")

vehicle.mode=VehicleMode("GUIDED")
arm_and_takeoff(2) #Tell drone to fly 2 meters in the sky
goto(3,0) #for moving 3m north




vehicle.mode = VehicleMode("LAND") # Once drone reaches altitude, tell it to land

time.sleep(2)

print("End of function")
print("Arducopter version :%s" %vehicle.version)

while True :
	time.sleep(2)

vehicle.close()


