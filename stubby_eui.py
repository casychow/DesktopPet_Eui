import RPi.GPIO as GPIO
import time

def info():
	'''Prints a basic library description'''
	print("Software library for Eui.")

## timers ##

def workTime(testing=False):
	print("Start work time!")

	if (testing):			# for testing purposes just wait 0.5s
		time.sleep(0.5)
	else:
		time.sleep(25*60)	# 25min of focused work time

	print("Time for a break!")

def breakTime(testing=False):
	print("It's break time!")

	if (testing):			# for testing purposes just wait 0.5s
		time.sleep(0.5)
	else:
		time.sleep(5*60)	# 5 min of break

	print("Break is over")

def setupBtnForTimer():
        print("in setupBtnForTimer")
        PIN = 17
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN)
        return PIN

def waitForBtnPress(PIN, duration):
	timerRunning = False    # timer is initially not running

	try:
		print("Waiting for button press to start timer...")
		print("NOTE: ^C to stop testing waitForBtnPress")
		while True:
			btnPressed = GPIO.input(PIN) # 0 is false & 1 is true
			time.sleep(0.5)

                	# button pressed to end timer
			if (btnPressed and timerRunning):
				print("Timer forced to end")
				timerRunning = False
				print("Waiting for button press to start timer...")
				continue

                	# button pressed to start timer
			if (btnPressed and not timerRunning):
				print("Timer starts")
				start = time.time()
				timerRunning = True

		 	# timer is running
			if (timerRunning):
				if (time.time()-start >= duration):
					print("Time ended")
					timerRunning = False
					print("Waiting for button press to start timer...")

	except KeyboardInterrupt:
		print("waitForBtnEnd forced to end")
		GPIO.cleanup()
		time.sleep(1)

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

def setupSound():
	print("in setupSound")
	PIN = 12
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN, GPIO.OUT)
	return PIN

def makeSound(PIN):
	print("piezo make a sound")
	pwm = GPIO.PWM(PIN, 276)
	pwm.start(1)
	time.sleep(1)
	pwm.stop()

def playMelody(song, beat, tempo, PIN):
	print("piezo plays a song")

	pwm = GPIO.PWM(PIN, 100)
	pwm.start(50)

	for i in range(0, len(song)):
		pwm.ChangeFrequency(song[i])
		time.sleep(beat[i]*tempo)

	pwm.ChangeDutyCycle(0)
	pwm.stop()

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
