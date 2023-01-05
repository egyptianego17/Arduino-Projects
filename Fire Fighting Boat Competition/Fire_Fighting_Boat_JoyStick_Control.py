# import necessary modules
import pygame
import serial
import time
import threading

# Set up the serial connection to the Arduino
Shoting = False

# define function to control robot movement
def Motion(Up, Down, Left, Right):
    global M_Up, M_Down, M_Right, M_Left
    global M_UL, M_UR, M_DL, M_DR

    # if joystick is tilted up and left, move robot up and left
    if (Up and Left):
        M_UL = True
        # send command to Arduino to move robot up and left
        ship.write(b"W")
        ship.write(b"\n")
        return 0

    # if joystick is tilted up and right, move robot up and right
    elif (Up and Right) :
        M_UR = True
        # send command to Arduino to move robot up and right
        ship.write(b"Q")
        ship.write(b"\n")
        return 0

    # if joystick is tilted down and left, move robot down and left
    elif (Down and Left):
        M_DL = True
        # send command to Arduino to move robot down and left
        ship.write(b"Z")
        ship.write(b"\n")
        return 0

    # if joystick is tilted down and right, move robot down and right
    elif (Down and Right):
        M_DR = True
        # send command to Arduino to move robot down and right
        ship.write(b"X")
        ship.write(b"\n")
        return 0

    # if joystick is tilted up, move robot up
    elif Up :
        M_Up = True
        # send command to Arduino to move robot up
        ship.write(b"U")
        ship.write(b"\n")
        return 0

    # if joystick is tilted down, move robot down
    elif Down :
        M_Down = True
        # send command to Arduino to move robot down
        ship.write(b"D")
        ship.write(b"\n")
        return 0

    # if joystick is tilted left, turn 2 motors opposite directions to move robot left
    elif Left :
        M_Left = True
        # send command to Arduino to turn 2 motors opposite directions to move robot left
        ship.write(b"L")
        ship.write(b"\n")
        return 0

    # if joystick is tilted right, turn 2 motors opposite directions to move robot right
    elif Right:
        M_Right = True
        # send command to Arduino to turn 2 motors opposite directions to move robot right
        ship.write(b"R")
        ship.write(b"\n")
        return 0
    # if joystick is not tilted in any direction, stop the robot
    else:
        # send command to Arduino to stop the robot
        ship.write(b"S")
        ship.write(b"\n")

# define function to control camera direction
def CameraDirection(Up, Down, Left, Right):
    # if F button is pressed, move camera up
    if Up:
        # send command to Arduino to move camera up
        ship.write(b"i")
        ship.write(b"\n")

    # if trigger button is pressed, move camera down
    if Down:
        # send command to Arduino to move camera down
        ship.write(b"k")
        ship.write(b"\n")

    # if A button is pressed, move camera right
    if Right:
        # send command to Arduino to move camera right
        ship.write(b"l")
        ship.write(b"\n")

    # if B button is pressed, move camera left
    if Left:
        # send command to Arduino to move camera left
        ship.write(b"j")
        ship.write(b"\n")

# define function to control firing of water gun
def FireWater(fire):
    global Shoting
    # if X button is pressed and water gun is not already firing, start firing
    if fire and not(Shoting):
        Shoting = True
        # send command to Arduino to start firing water gun
        ship.write(b"F")
        ship.write(b"\n")
    # if X button is not pressed and water gun is
# if water gun is not firing and X button is not pressed, start firing
    if not(fire) and Shoting:
        Shoting = False
        # send command to Arduino to stop firing water gun
        ship.write(b"f")
        ship.write(b"\n")

# define function to control speed of robot and water gun
def changespeed(up ,down, Fup, Fdwn):
    # if left bumper button is pressed, increase speed of robot
    if up ==1:
        # send command to Arduino to increase speed of robot
        ship.write(b"I")
        ship.write(b"\n")

    # if left trigger button is pressed, decrease speed of robot
    elif down ==1:
        # send command to Arduino to decrease speed of robot
        ship.write(b"J")
        ship.write(b"\n")
    # if right bumper button is pressed, increase speed of water gun
    if Fup ==1:
        # send command to Arduino to increase speed of water gun
        ship.write(b"P")
        ship.write(b"\n")
    # if right trigger button is pressed, decrease speed of water gun
    elif Fdwn ==1:
        # send command to Arduino to decrease speed of water gun
        ship.write(b"O")
        ship.write(b"\n")


def check_connection(n):
    # function to check serial connection
    global ship
    data = ship.readline().decode("utf-8")
    if len(data) > 0:
        n = 0;
        print(data)
    elif n >3:
        ship.close()
        try:
            ship = serial.Serial('COM15', 9600)
            ship.write(b"f")
            ship.write(b"\n")
            ship.write(b"S")
            ship.write(b"\n")
        except serial.serialutil.SerialException:
            print("Failed to connect to Arduino. Trying again in 3 seconds...")
            time.sleep(0.5)
    else:
        n+=1
    threading.Timer(1/4, check_connection, args = (n)).start()
    
    
# try to establish serial connection with Arduino
while True:
    try:
        # try to open serial connection to Arduino on COM15 at 9600 baud rate
        ship = serial.Serial('COM15', 9600)
        # send command to Arduino to stop firing water gun
        ship.write(b"f")
        ship.write(b"\n")
        # send command to Arduino to stop the robot
        ship.write(b"S")
        ship.write(b"\n")
        break
    except serial.serialutil.SerialException:
        # if serial connection fails, print message and try again in 3 seconds
        print("Failed to connect to Arduino. Trying again in 3 seconds...")
        time.sleep(3)
    else:
        # if serial connection fails after multiple attempts, print message
        print("Failed to connect to Arduino.")
        
# initialize pygame
pygame.init()

# set up joystick
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

n = 0
threading.Timer(1/4, check_connection, args = (n)).start()

# set up clock
clock = pygame.time.Clock()


while True:
    # Read the controller inputs
    pygame.event.get()

    # set the LEFT variable to 1 if the joystick's x-axis is less than -0.5, else set it to 0
    LEFT = 1 if joystick.get_axis(0) < -0.5 else 0
    #print("LEFT")
    
    # set the RIGHT variable to 1 if the joystick's x-axis is greater than 0.5, else set it to 0
    RIGHT = 1 if joystick.get_axis(0) > 0.5 else 0
    #print("RIGHT")
    
    # set the UP variable to 1 if the joystick's y-axis is less than -0.5, else set it to 0
    UP = 1 if joystick.get_axis(1) < -0.5 else 0
    #print("UP")
    
    # set the DOWN variable to 1 if the joystick's y-axis is greater than 0.5, else set it to 0
    DOWN = 1 if joystick.get_axis(1) > 0.5 else 0
    #print("DOWN")

    # set the H_LEFT variable to 1 if the joystick's z-axis (rotation about x-axis) is less than -0.5, else set it to 0
    H_LEFT = 1 if joystick.get_axis(2) < -0.5 else 0
    #print("H_LEFT")
    
    # set the H_RIGHT variable to 1 if the joystick's z-axis (rotation about x-axis) is greater than 0.5, else set it to 0
    H_RIGHT = 1 if joystick.get_axis(2) > 0.5 else 0
    #print("H_RIGHT")

    # set the H_UP variable to 1 if the joystick's r-axis (rotation about y-axis) is less than -0.5, else set it to 0
    H_UP = 1 if joystick.get_axis(3) < -0.5 else 0
    #print("H_UP")
    
    # set the H_DOWN variable to 1 if the joystick's r-axis (rotation about y-axis) is greater than 0.5, else set it to 0
    H_DOWN = 1 if joystick.get_axis(3) > 0.5 else 0
    #print("H_DOWN")

    # set the fire variable to the value of the first button on the joystick (True if pressed, False if not pressed)
    fire = joystick.get_button(0)


    # set the factorup variable to the value of the 10's button on the joystick (True if pressed, False if not pressed)
    factorup = joystick.get_button(10)
    
    
    # set the factordown variable to the value of the 5th button on the joystick (True if pressed, False if not pressed)
    factordown = 1 if joystick.get_axis(5) > 0.5 else 0
    
    # set the speedup variable to the value of the 9th button on the joystick (True if pressed, False if not pressed)
    speedup = joystick.get_button(9)
    
    # set the speeddown variable to the value of the 9th button on the joystick (True if pressed, False if not pressed)
    speeddwn = 1 if joystick.get_axis(4) > 0.5 else 0


    # try to execute the Motion, CameraDirection, FireWater, and changespeed functions
    try:
        Motion(UP, DOWN, LEFT, RIGHT)
        CameraDirection(H_UP, H_DOWN, H_LEFT, H_RIGHT)
        FireWater(fire)
        changespeed(speedup ,speeddwn, factorup, factordown)
    # if the serial connection is lost, catch the exception and try to reconnect
    except serial.serialutil.SerialException:
         # If the serial connection is lost, try to reconnect'
        n=0
        while n<=3:
            try:
                ship = serial.Serial('COM15', 9600)
                break
            except serial.serialutil.SerialException:
                # if the serial connection fails, print message and try again in 1 seconds
                print("Failed to reconnect to Arduino. Trying again in 1 seconds...")
                time.sleep(1)
                n+=1
        else:
            # if the serial connection fails after multiple attempts, print message and exit
            print("Failed to reconnect to Arduino. Exiting.")
            exit()

    # Determine the commands to send to the Arduino based on the controller inputs
    clock.tick(30)
