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

# PINOUT:
# GP0     rot,    BCLK AMP    VBUS  
# GP1     blau,   LRC AMP     VSYS 
# GNG                         GND, 2xSchwarz, microSD, AMP
# GP2     weiß,   DIN AMP     3V3_EN
# GP3                         3V3(OUT), 2xROT, microSD, AMP
# GP4                         ADC-VREF
# GP5                         GP28 StatusLED Anode 50 Ohm
# GND                         GND  StatusLED Kathode
# GP6                         GP27
# GP7                         GP26
# GP8     weiß,   SO micorSD  RUN
# GP9     blau,   CS microSD  GP22 
# GND                         GND schwarz PIN1 TÜR 
# GP10    blau,   CLK microSD GP21 
# GP11    weiß,   SI microSD  GP20 
# GP12    blank,  GAIN AMP    GP19 
# GP13    100k,   GAIN AMP    GP18 blau, PIN2 TÜR 
# GND                         GND  schwarz, PIN1 PIN4 BUTTON-CON
# GP14                        GP17 weiß, PIN3 BUTTON-CON LED
# GP15                        GP16 blau, PIN2 BUTTON-CON Button

import audiocore
import board
import audiobusio
import digitalio
import time

#PIN Definitonen
DOORTSWITCH_PIN = board.GP18

DOORBUTTON_PIN = board.GP16
BUTTONLED_PIN  = board.GP17

STATUSLED_PIN  = board.GP28

GAIN100K_PIN   = board.GP13
GAINVCC_PIN    = board.GP12

# Set Gain des Audio Amps, 3, 6, 9, 12 dB
gain=9


# Init I2S Audio Verstaerker mit GP0 = BCLK rot, GP1 = LineClock blau, GP2=Data weiss
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

# Define GP13 als Schalter fuer die Schiebetuer, 
# Tuer Offen = 1, Tuer Zu = 0
doorswtich = digitalio.DigitalInOut(DOORTSWITCH_PIN)
doorswtich.switch_to_input(pull=digitalio.Pull.DOWN)

# Define GP12 als Drucktaster fuer die Fahrstuhltuer, 
# Schalter Reagiert auf zustandsaenderung ueber doorbuttonLastValue
doorbutton = digitalio.DigitalInOut(DOORBUTTON_PIN)
doorbutton.switch_to_input(pull=digitalio.Pull.UP)
doorbuttonLastValue = 1

# Define GP11 als LED im Drucktaster
buttonLED = digitalio.DigitalInOut(BUTTONLED_PIN)
buttonLED.switch_to_output()

# Define GP11 als 27 als gruene Debug LED am Kaestchen
# zur Zeit implentiert als Power LED
LED1 = digitalio.DigitalInOut(STATUSLED_PIN)
LED1.switch_to_output()

#Logik zum setzten des Gais nach Datenblatt. 
gain100k = digitalio.DigitalInOut(GAIN100K_PIN)
gainvdd = digitalio.DigitalInOut(GAINVCC_PIN)
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
