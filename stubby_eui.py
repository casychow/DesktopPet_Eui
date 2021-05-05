import RPi.GPIO as GPIO
import time
import spidev
import Adafruit_SSD1306
from PIL import Image

def info():
	'''Prints a basic library description'''
	print("Software library for Eui.")

## timers ##

def workTime(testing=False, wDuration=25):
	print("Start work time!")

	if (testing):			# for testing purposes just wait 0.5s
		time.sleep(0.5)
	else:
		time.sleep(wDuration*60)	# 25min of focused work time

	print("Time for a break!")

def breakTime(testing=False, bDuration=5):
	print("It's break time!")

	if (testing):			# for testing purposes just wait 0.5s
		time.sleep(0.5)
	else:
		time.sleep(bDuration*60)	# 5 min of break

	print("Break is over")

def setupBtnForTimer(timerPin): #originally without any params
	print("in setupBtnForTimer")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(timerPin, GPIO.IN)

def waitForBtnPress(timerPin, duration):
	timerRunning = False    # timer is initially not running

	try:
		print("Waiting for button press to start timer...")
		print("NOTE: ^C to stop testing waitForBtnPress")
		while True:
			btnPressed = GPIO.input(timerPin) # 0 is false & 1 is true
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

def setupLED(DATA, STOR, SHIFT, NSHIFT):
	#GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DATA, GPIO.OUT)
	GPIO.setup(STOR, GPIO.OUT)
	GPIO.setup(SHIFT, GPIO.OUT)
	GPIO.setup(NSHIFT, GPIO.OUT)
	GPIO.output(NSHIFT, GPIO.LOW) #clear shift register
	GPIO.output(NSHIFT, GPIO.HIGH) #don't clear shift register yet

def turnOnLED():
	print("LEDs turn on")

def turnOffLED():
	print("LEDs turn off")

def LEDwave(DATA, STOR, SHIFT):
	try:
		print("performing LED wave now. Press ^C to stop")
		while True:
			x=0x01
			for i in range(0,8):
				GPIO.output(DATA, GPIO.HIGH)
				time.sleep(0.1)
				GPIO.output(SHIFT, GPIO.HIGH)
				time.sleep(0.1)
				GPIO.output(SHIFT, GPIO.LOW)
				GPIO.output(DATA, GPIO.LOW)
				GPIO.output(STOR, GPIO.HIGH)
				time.sleep(0.1)
				GPIO.output(STOR, GPIO.LOW)
			for i in range(0,8):
				GPIO.output(DATA, GPIO.LOW)
				time.sleep(0.1)
				GPIO.output(SHIFT, GPIO.HIGH)
				time.sleep(0.1)
				GPIO.output(SHIFT, GPIO.LOW)
				GPIO.output(DATA, GPIO.LOW)
				GPIO.output(STOR, GPIO.HIGH)
				time.sleep(0.1)
				GPIO.output(STOR, GPIO.LOW)
	except KeyboardInterrupt:
		GPIO.cleanup()

def changeLEDColor():
	print("LEDs change color")

def sendByte():
	print("send byte to shift register")

## sound ##

def setupSound(soundPin):
	print("in setupSound")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(soundPin, GPIO.OUT)

def makeSound(soundPin):
	print("piezo make a sound")
	pwm = GPIO.PWM(soundPin, 276)
	pwm.start(1)
	time.sleep(1)
	pwm.stop()

def playMelody(song, beat, tempo, soundPin):
	print("piezo plays a song")

	pwm = GPIO.PWM(soundPin, 100)
	pwm.start(50)

	for i in range(0, len(song)):
		pwm.ChangeFrequency(song[i])
		time.sleep(beat[i]*tempo)

	pwm.ChangeDutyCycle(0)
	pwm.stop()

## movements ##

def motorTest(IN1, IN2, EN1, IN3, IN4, EN2):
	print("power motors on")
	#GPIO.setmode(GPIO.BCM)
	#GPIO.setwarnings(False)

	#in1 = 2
	#in2 = 3
	#en1 = 4    # Enable Pin for wheel 1
	#in3 = 1    # Input Pin
	#in4 = 0    # Input Pin
	#en2 = 5    # Enable Pin for wheel 2

	GPIO.setup(IN1, GPIO.OUT)
	GPIO.setup(IN2, GPIO.OUT)
	GPIO.setup(EN1, GPIO.OUT)
	GPIO.setup(IN3, GPIO.OUT)
	GPIO.setup(IN4, GPIO.OUT)
	GPIO.setup(EN2, GPIO.OUT)

	print("\tFORWARD MOTION")
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(EN1, GPIO.HIGH)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)
	GPIO.output(EN2, GPIO.HIGH)

	time.sleep(3)

	print("\tBACKWARD MOTION")
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.HIGH)
	GPIO.output(EN1, GPIO.HIGH)
	GPIO.output(IN3, GPIO.LOW)
	GPIO.output(IN4, GPIO.HIGH)
	GPIO.output(EN2, GPIO.HIGH)

	time.sleep(3)

	print("\tSTOP")
	GPIO.output(EN1, GPIO.LOW)
	GPIO.output(EN2, GPIO.LOW)

	GPIO.cleanup()

def rightTurn():
	print("make right turn")

def leftTurn():
	print("make left turn")

## sensors ##

def readADC(spi, channel=0):
	if ((channel > 3) or (channel < 0)):
		return -1
	reply = spi.xfer2([1, (8 + channel) << 4, 0])
	adc = ((reply[1] & 3) << 8) + reply[2]
	v = (3.3 * adc) / 1024 #3.3 is Vref
	print("\tvoltage =", v)
	dist = 16.2537 * v**4 - 129.893 * v**3 + 382.268 * v**2 - 512.611 * v + 306.439
	#still need to figure out correct formula
	cm = int(round(dist))
	return cm

def readDist(spiChannel):
	print("distance read by sensor")
	#GPIO.setwarnings(False)
	#GPIO.setmode(GPIO.BCM)
	spi = spidev.SpiDev()
	spi.open(0, spiChannel) # SPI Port 0, Chip Select 0
	spi.max_speed_hz = 7629

	try:
		while True:
			print("\tNOTE: ^C to stop testing readDist")
			print("\tdistance in cm:", readADC(spi))
			print()
			time.sleep(1)
	except KeyboardInterrupt:
		spi.close()
		GPIO.cleanup()

def registerTap():
	print("gets a signal from linear softpot")

def buttonPressed():
	print("button is pressed")

## display ##

def displayOn():
	print("currently displaying happycat image")
	RST = 24
	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
	disp.begin()
	disp.clear()
	disp.display()
	# Load image based on OLED display height.  Note that image is converted to 1 bit color.
	if disp.height == 64:
		image = Image.open('/home/pi/DesktopPet_Eui/Adafruit_Python_SSD1306/examples/happycat_oled_64.ppm').convert('1')
	else:
		image = Image.open('/home/pi/DesktopPet_Eui/Adafruit_Python_SSD1306/examples/happycat_oled_32.ppm').convert('1')

	# Display image.
	disp.image(image)
	disp.display()

def displayOff():
	print("display will turn off in one second")
	RST = 24
	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
	time.sleep(1)
	disp.clear()
	disp.display()
	print("display has turned off")

def displayImage():
	print("displaying other image")
	RST = 24
	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
	disp.clear()
	disp.display()
	'''
	if disp.height == 64:
		image = Image.open('/home/pi/DesktopPet_Eui/Adafruit_Python_SSD1306/examples/happycat_oled_64.ppm').convert('1')
	else:
		image = Image.open('/home/pi/DesktopPet_Eui/Adafruit_Python_SSD1306/examples/happycat_oled_32.ppm').convert('1')

	# Display image.
	#disp.image(image)
	'''
	disp.display()

def displayText():
	print("displays text - still need to configure")
