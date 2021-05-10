from stubby_eui import *
from time import sleep

# for testing playMelody() -- London Bridge

c = [32, 65, 131, 262, 523]
db = [34, 69, 139, 277, 554]
d = [36, 73, 147, 294, 587]
eb = [37, 78, 156, 311, 622]
e = [41, 82, 165, 330, 659]
f = [43, 87, 175, 349, 698]
gb = [46, 92, 185, 370, 740]
g = [49, 98, 196, 392, 784]
ab = [52, 104, 208, 415, 831]
a = [55, 110, 220, 440, 880]
bb = [58, 117, 223, 466, 932]
b = [61, 123, 246, 492, 984]

''' BEATS:
        0.5 = eigth note
        1 = quarter note
        2 = half note
        3 = dotted half note
        4 = whole note
'''

londonBridge = [g[2], a[2], g[2], f[2], e[2], f[2], g[2], d[2],
                e[2], f[2], e[2], f[2], g[2], g[2], a[2], g[2],
                f[2], e[2], f[2], g[2], d[2], g[2], e[2], c[2]]
LBbeats = [2, 0.5, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0.5, 1,
                1, 1, 1, 2, 2, 2, 1, 1]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
SOUNDPIN = 12
TIMERPIN = 17

#LIGHTS
DATA = 21
STOR = 13
SHIFT = 18
NSHIFT = 16

#MOTORS
IN1 = 27 #2
IN2 = 22 #3
EN1 = 4
IN3 = 1
IN4 = 0
EN2 = 5

#DISPLAY
RST = 26 #24
text = "cassandra was here - bleep, blap, bloop :P"


info()

workTime(True)
breakTime(True)

setupBtnForTimer(TIMERPIN)
waitForBtnPress(TIMERPIN, 10)

setupLED(DATA, STOR, SHIFT, NSHIFT)
sendByte()
turnOffLED()
sleep(1)
turnOnLED()
sleep(1)
turnOffLED()
sleep(1)
LEDwave()

setupSound(SOUNDPIN)
makeSound(SOUNDPIN)
sleep(2)
playMelody(londonBridge, LBbeats, 0.3, SOUNDPIN)

motorTest(IN1, IN2, EN1, IN3, IN4, EN2)
sleep(2)
rightTurn(IN1, IN2, EN1, IN3, IN4, EN2)
sleep(2)
leftTurn(IN1, IN2, EN1, IN3, IN4, EN2)
sleep(2)
stopMotors(IN1, IN2, EN1, IN3, IN4, EN2)

readDist(0)
#registerTap()
#probably won't get to this - used to answer questions on the OLED display

#buttonPressed()
#probably won't get to this - mute sounds

disp = setupDisplay(RST)
displayOn(disp)
sleep(2)
displayImage(disp)
sleep(1)
displayText(disp, text)
displayOff(disp)

GPIO.cleanup()
