import RPi.GPIO as GPIO
import time
import spidev
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#PWM = -1

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
<<<<<<< HEAD
                # button pressed to end timer
>>>>>>> b2a9456abe1a5d637841e816ac850b8b5b306e2b
			if (btnPressed and timerRunning):
				print("Timer forced to end")
				timerRunning = False
				print("Waiting for button press to start timer...")
				continue

<<<<<<< HEAD
                # button pressed to start timer
>>>>>>> b2a9456abe1a5d637841e816ac850b8b5b306e2b
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
	#print("in setupLED")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DATA, GPIO.OUT)
	GPIO.setup(STOR, GPIO.OUT)
	GPIO.setup(SHIFT, GPIO.OUT)
	GPIO.setup(NSHIFT, GPIO.OUT)
	GPIO.output(NSHIFT, GPIO.LOW) #clear shift register
	GPIO.output(NSHIFT, GPIO.HIGH) #don't clear shift register yet

def turnOnLED(DATA=21, STOR=13, SHIFT=18):
	print("LEDs turn on")
	#sendByte(0xFF)
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

def turnOffLED(DATA=21, STOR=13, SHIFT=18):
	print("LEDs turn off")
	#sendByte(0x00)
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

def LEDwave(DATA=21, STOR=13, SHIFT=18):
	try:
		print("performing LED wave now. Press ^C to stop")
		while True:
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
			#for i in range(0,8):
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

def sendByte(val=0b10000001, DATA=21, STOR=13, SHIFT=18):
	print("send byte to shift register")
	'''
	for ind, bit in enumerate(bin(val)):
		if (ind<2):
			continue
		elif (bit==1):
			GPIO.output(DATA, GPIO.HIGH)
			print("yes equal")
		else:
			GPIO.output(DATA, GPIO.LOW)
		time.sleep(0.1)
		GPIO.output(SHIFT, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(SHIFT, GPIO.LOW)
		GPIO.output(DATA, GPIO.LOW)
		GPIO.output(STOR, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(STOR, GPIO.LOW)
	'''

## sound ##

def setupSound(soundPin):
	print("in setupSound")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(soundPin, GPIO.OUT)

#def stopSound():
#	PWM.stop()

def makeSound(soundPin):
	print("piezo make a sound")
	PWM = GPIO.PWM(soundPin, 276)
	PWM.start(1)
	time.sleep(1)
	#stopSound()
	PWM.stop()

def playMelody(song, beat, tempo, soundPin):
	print("piezo plays a song")

	PWM = GPIO.PWM(soundPin, 100)
	PWM.start(50)

	for i in range(0, len(song)):
		PWM.ChangeFrequency(song[i])
		time.sleep(beat[i]*tempo)

	PWM.ChangeDutyCycle(0)
	PWM.stop()
	#stopSound()

## movements ##

def setupMotors(IN1, IN2, EN1, IN3, IN4, EN2):
	GPIO.setup(IN1, GPIO.OUT)
	GPIO.setup(IN2, GPIO.OUT)
	GPIO.setup(EN1, GPIO.OUT)
	GPIO.setup(IN3, GPIO.OUT)
	GPIO.setup(IN4, GPIO.OUT)
	GPIO.setup(EN2, GPIO.OUT)

def forward(IN1, IN2, EN1, IN3, IN4, EN2):
	print("\tFORWARD MOTION")
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(EN1, GPIO.HIGH)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)
	GPIO.output(EN2, GPIO.HIGH)

def backward(IN1, IN2, EN1, IN3, IN4, EN2):
	print("\tBACKWARD MOTION")
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.HIGH)
	GPIO.output(EN1, GPIO.HIGH)
	GPIO.output(IN3, GPIO.LOW)
	GPIO.output(IN4, GPIO.HIGH)
	GPIO.output(EN2, GPIO.HIGH)

def stopMotors(IN1, IN2, EN1, IN3, IN4, EN2):
	print("\tSTOP")
	GPIO.output(EN1, GPIO.LOW)
	GPIO.output(EN2, GPIO.LOW)

def motorTest(IN1, IN2, EN1, IN3, IN4, EN2):
	print("power motors on")

	GPIO.setup(IN1, GPIO.OUT)
	GPIO.setup(IN2, GPIO.OUT)
	GPIO.setup(EN1, GPIO.OUT)
	GPIO.setup(IN3, GPIO.OUT)
	GPIO.setup(IN4, GPIO.OUT)
	GPIO.setup(EN2, GPIO.OUT)

	#print("\tFORWARD MOTION")
	#GPIO.output(IN1, GPIO.HIGH)
	#GPIO.output(IN2, GPIO.LOW)
	#GPIO.output(EN1, GPIO.HIGH)
	#GPIO.output(IN3, GPIO.HIGH)
	#GPIO.output(IN4, GPIO.LOW)
	#GPIO.output(EN2, GPIO.HIGH)

	forward(IN1, IN2, EN1, IN3, IN4, EN2)
	time.sleep(2)

	#print("\tBACKWARD MOTION")
	#GPIO.output(IN1, GPIO.LOW)
	#GPIO.output(IN2, GPIO.HIGH)
	#GPIO.output(EN1, GPIO.HIGH)
	#GPIO.output(IN3, GPIO.LOW)
	#GPIO.output(IN4, GPIO.HIGH)
	#GPIO.output(EN2, GPIO.HIGH)
	backward(IN1, IN2, EN1, IN3, IN4, EN2)

	time.sleep(2)

	#print("\tSTOP")
	#GPIO.output(EN1, GPIO.LOW)
	#GPIO.output(EN2, GPIO.LOW)
	stopMotors(IN1, IN2, EN1, IN3, IN4, EN2)
	#GPIO.cleanup()

def rightTurn(IN1, IN2, EN1, IN3, IN4, EN2):
	print("make right turn")
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(EN1, GPIO.HIGH)
	GPIO.output(EN2, GPIO.LOW)

def leftTurn(IN1, IN2, EN1, IN3, IN4, EN2):
	print("make left turn")
	GPIO.output(EN1, GPIO.LOW)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)
	GPIO.output(EN2, GPIO.HIGH)

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
	spi = spidev.SpiDev()
	spi.open(0, spiChannel) # SPI Port 0, Chip Select 0
	spi.max_speed_hz = 7629

	try:
		while True:
			#print("\tNOTE: ^C to stop testing readDist")
			dist = readADC(spi)
			print("\tdistance in cm:", dist)
			if (dist > 37):
				print("\t\tSomething detected!")
			else:
				print("\t\tNothing...")
			time.sleep(1)
	except KeyboardInterrupt:
		spi.close()
		#GPIO.cleanup()

def registerTap():
	print("gets a signal from linear softpot")

def buttonPressed():
	print("button is pressed")

## display ##

def setupDisplay(pin):
	return Adafruit_SSD1306.SSD1306_128_64(rst=pin)

def displayOn(disp):
	print("currently displaying happycat image")
	#RST = 24
	#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
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

def displayOff(disp):
	print("display will turn off in one second")
	#RST = 24
	#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
	time.sleep(1)
	disp.clear()
	disp.display()
	print("display has turned off")

def displayImage(disp):
	print("displaying other image")
	#RST = 24
	#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
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

def editText(text):
	ret = ""
	last = ""

	#add \n and white space for strings that are not exactly multiples of 21 (the edge of the OLED screen)
	if ((len(text)%21)):
		#if not exactly multiple, need to know how much white space to add at the end
		last = ' ' * (21 - len(text)%21)
	text += last
	for ind in range(1, (len(text)//21)+1):
		ret += text[ind*21-21:ind*21] + '\n'
	return ret

def displayText(disp, text):
	print("displaying text on OLED:\n" + text)
	disp.begin()
	disp.clear()
	disp.display()
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	padding = -2
	line = padding
	bottom = height - padding
	x = 0
	font = ImageFont.load_default()
	text = editText(text)
	draw.multiline_text((x, line), text, font=font, fill=255)
	disp.image(image)
	disp.display()
	time.sleep(0.1)
