# tapFX - tapStuhl
# Tobias Disch - September 2024 - theater am puls Schwetzingen
# Produktion Biedermann und die Brandstifter
# -------------------------------------------------------------------
# Wenn auf den Fahrstuhlknopf gedrückt wird, soll das Licht am Knopf
# an gehen.
# Wenn die Fahrstuhltür auf geht, soll ein BING und anschließend die 
# Fahrstuhlmusik in Dauerschleife abgespeilt werden. Das Licht 
# am Knopf soll dann aus gehen.
# Wird die Fahrstuhltür geschlossen, soll die Musik aus gehen.
# Ist die Fahrstuhltür offen, soll das Licht am Knopf nicht an gehen,
# egal ob gedrückt wird. 
# -------------------------------------------------------------------
# Hardware
# Raspberry Pico, Adafruit MAX98357A, 3W Lautsprecher,
# Roll Schalter, beleuchteter Drucktaster
# -------------------------------------------------------------------

import audiocore
import board
import audiobusio
import digitalio
import time

# Init I2S Audio Verstaerker mit GP0 = CLK, GP1 = LineClock, GP2=Data
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

# Define GP13 als Schalter fuer die Schiebetuer, 
# Tuer Offen = 1, Tuer Zu = 0
doorswtich = digitalio.DigitalInOut(board.GP13)
doorswtich.switch_to_input(pull=digitalio.Pull.UP)

# Define GP12 als Drucktaster fuer die Fahrstuhltuer, 
# Schalter Reagiert auf zustandsaenderung ueber doorbuttonLastValue
doorbutton = digitalio.DigitalInOut(board.GP12)
doorbutton.switch_to_input(pull=digitalio.Pull.UP)
doorbuttonLastValue = 1

# Define GP11 als LED im Drucktaster
buttonLED = digitalio.DigitalInOut(board.GP11)
buttonLED.switch_to_output()

# Define GP11 als 27 als gruene Debug LED am Kaestchen
# zur Zeit implentiert als Power LED
LED1 = digitalio.DigitalInOut(board.GP27)
LED1.switch_to_output()

# Set Gain des Audio Amps, 
gain=9

#Logik zum setzten des Gais nach Datenblatt. 
gain100k = digitalio.DigitalInOut(board.GP20)
gainvdd = digitalio.DigitalInOut(board.GP19)
if gain==12 or gain ==9 or gain==6:
    gain100k.switch_to_input()    
if gain== 15:
    gain100k.switch_to_output()
    gain100k.value = 0
if gain==3:
    gain100k.switch_to_output()
    gain100k.value = 1

if gain==15 or gain ==9 or gain==3:
    gainvdd.switch_to_input()    
if gain== 12:
    gainvdd.switch_to_output()
    gainvdd.value = 0
if gain==6:
    gainvdd.switch_to_output()
    gainvdd.value = 1

# Oeffne Musik
music_file = open("elevator-ziff-loop.wav", "rb")
music = audiocore.WaveFile(music_file)

bell_file = open("bell.wav", "rb")
bell = audiocore.WaveFile(bell_file)

# Power LED AN
LED1.value = 1
print("Moin ")

# Programm Loop
while 1:
    if audio.playing:
        if doorswtich.value == 0:
            audio.stop()
    else:
        if doorswtich.value == 1: 
            buttonLED.value = 0
            audio.play(bell)
            time.sleep(0.5)
            audio.play(music, loop=True)

        if doorbutton.value != doorbuttonLastValue:
            buttonLED.value = 1

    doorbuttonLastValue = doorbutton.value

    time.sleep(0.1)
