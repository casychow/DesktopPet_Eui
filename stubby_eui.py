import RPi.GPIO as GPIO
from time import sleep

def info():
	'''Prints a basic library description'''
	print("Software library for Eui.")

def setupSound():
	print("in setupSound")
	PIN = 12
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN, GPIO.OUT)
	return PIN

## lights ##

def turnOnLED():
	print("LEDs turn on")

def turnOffLED():
	print("LEDs turn off")

def changeLEDColor():
	print("LEDs change color")

def sendByte():
	print("send byte to shift register")

## sound ##

def makeSound(PIN):
	print("piezo make a sound")
	pwm = GPIO.PWM(PIN, 276)
	pwm.start(1)
	sleep(1)
	pwm.stop()

def makeMelody():
	print("piezo plays a tone")

## movements ##

def motorTest():
	print("power motors on")

def rightTurn():
	print("make right turn")

def leftTurn():
	print("make left turn")

## sensors ##

def readDist():
	print("distance read by sensor")

def registerTap():
	print("gets a signal from linear softpot")

def buttonPressed():
	print("button is pressed")

## display ##

def displayOn():
	print("display turns on")

def displayOff():
	print("display turns off")

def displayImage():
	print("displays an image")

def displayText():
	print("displays text")
