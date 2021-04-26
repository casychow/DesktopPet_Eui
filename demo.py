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
DATA = 11
STOR = 13
SHIFT = 15
NSHIFT = 16

info()

workTime(True)
breakTime(True)

#btnPIN = setupBtnForTimer()
#waitForBtnPress(btnPIN, 10)	# 10 sec
setupBtnForTimer(TIMERPIN)
waitForBtnPress(TIMERPIN, 10)

setupLED(DATA, STOR, SHIFT, NSHIFT)
turnOnLED()
turnOffLED()
LEDwave(DATA, STOR, SHIFT)
changeLEDColor()
sendByte()

#buzzPIN = setupSound()
#makeSound(buzzPIN)
setupSound(SOUNDPIN)
makeSound(SOUNDPIN)
sleep(2)
#playMelody(londonBridge, LBbeats, 0.3, buzzPIN)
playMelody(londonBridge, LBbeats, 0.3, SOUNDPIN)

motorTest()
rightTurn()
leftTurn()

#readDist(0) #0 = channel #need to make sure placing init value is fine
readDist()
registerTap()
buttonPressed()

displayOn()
displayOff()
displayImage()
displayText()
