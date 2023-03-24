from stemi.data_collection import collect
collect("ID")


from stemi import display
from stemi.expansion_board import ExpansionBoard
from adafruit_ahtx0 import AHTx0
from stemi.barometer import Barometer

# Konstante

grupa = "ime_grupe"
optimalna_vlaga_tla = 0.6
min_svjetlost = 0.5
optimalna_temp_zrak = [24,25,26]
korekcija_temp_zrak = -5 # ocitanje temperature sa senzora za tlak i temperaturu + korekcija

granice_temp_zraka = [16, 29]

eb = ExpansionBoard(i2c)
aht = AHTx0(i2c)
bar = Barometer(i2c)

_vlaga_zemlja = 0
_svjetlost = 0
_temp_zrak = 0
_tlak = 0
_vlaga_zrak = 0
_temp_zemlja = 0

mode = 0

# Funkcije

def pocetna(): # D

    display.clear()
    display.write(grupa, 0)
    display.write("SW1: Status", 1) # A
    display.write("SW2: Zrak", 2) # B
    display.write("SW3: Zemlja", 3) # C

def status(vlaga_zemlje, svjetlost, temp_zraka): # A

    display.clear()
    display.write("Status:", 0)
    display.write("Zaliti: " + zaliti(vlaga_zemlje), 1)
    display.write("Svjetlost: " + svjetlo(svjetlost), 2)
    display.write("Zrak: " + str(temp_zraka) + " C " + opttemp_zrak(temp_zraka), 3)

def zrak(temp_zraka, svjetlost, tlak, vlaga_zraka): # B

    display.clear()
    display.write("Temp: " + str(temp_zraka) + " C", 0)
    display.write("Svjetlost: " + str(svjetlost*100) + "%", 1)
    display.write("Tlak: " + str(tlak) + " hPa", 2)
    display.write("Vlaga: " + str(vlaga_zraka) + "%")

def zemlja(temp_zemlje, vlaga_zemlje): # C

    display.clear()
    display.write("Zemlja:", 0)
    display.write("Vlaga: " + str(vlaga_zemlje*100) + "%", 1)
    display.write("Temp: " + str(temp_zemlje) + " C", 2)
    display.write("Zaliti: " + zaliti(vlaga_zemlje), 3)

def zaliti(vlaga_zemlje):

    if (vlaga_zemlje < optimalna_vlaga_tla):
        return "Da"
    else:
        return "Ne"

def svjetlo(svjetlost):

    if (svjetlost < min_svjetlost):
        return "Tamno"
    else:
        return "OK" 

def opttemp_zrak(temp_zrak):

    if (int(temp_zrak) in optimalna_temp_zrak):
        return "OPT"
    elif (int(temp_zrak) <= granice_temp_zraka[0] or int(temp_zrak) >= granice_temp_zraka[1]):
        return "!!"
    else:
        return "OK"

pocetna()

while True:

    if (buttons.A.read_int() == 1): 

        _vlaga_zemlja = 0
        _svjetlost = 0
        _temp_zrak = 0
        _tlak = 0
        _vlaga_zrak = 0
        _temp_zemlja = 0

        mode = 1

    elif (buttons.B.read_int() == 1):

        _vlaga_zemlja = 0
        _svjetlost = 0
        _temp_zrak = 0
        _tlak = 0
        _vlaga_zrak = 0
        _temp_zemlja = 0

        mode = 2

    elif (buttons.C.read_int() == 1):

        _vlaga_zemlja = 0
        _svjetlost = 0
        _temp_zrak = 0
        _tlak = 0
        _vlaga_zrak = 0
        _temp_zemlja = 0

        mode = 3

    elif (buttons.D.read_int() == 1):

        pocetna()
        _vlaga_zemlja = 0
        _svjetlost = 0
        _temp_zrak = 0
        _tlak = 0
        _vlaga_zrak = 0
        _temp_zemlja = 0

        mode = 0
    
    if (mode == 1):

        vlaga_zemlja = float(f"{eb.sensor1.humidity/1024:.2f}")
        svjetlost = float(f"{eb.sensor1.ldr/1024:.2f}")
        temp_zrak = float(f"{bar.temp+korekcija_temp_zrak:.1f}")

        if (temp_zrak != _temp_zrak or svjetlost != _svjetlost or vlaga_zemlja != _vlaga_zemlja):

            status(vlaga_zemlja, svjetlost, temp_zrak)
            _vlaga_zemlja = vlaga_zemlja
            _svjetlost = svjetlost
            _temp_zrak = temp_zrak

    elif (mode == 2):

        temp_zrak = float(f"{bar.temp+korekcija_temp_zrak:.1f}")
        svjetlost = float(f"{eb.sensor1.ldr/1024:.2f}")
        tlak = float(f"{bar.pressure:.1f}")
        vlaga_zrak = float(f"{aht.relative_humidity:.1f}")

        if (temp_zrak != _temp_zrak or svjetlost != _svjetlost or int(vlaga_zrak) not in [int(_vlaga_zrak)-1,int(_vlaga_zrak), int(_vlaga_zrak)+1]):

            zrak(temp_zrak, svjetlost, tlak, vlaga_zrak)
            _temp_zrak = temp_zrak
            _svjetlost = svjetlost
            _tlak = tlak
            _vlaga_zrak = vlaga_zrak

    elif (mode == 3):

        temp_zemlja = float(f"{eb.sensor1.temp:.1f}")
        vlaga_zemlja = float(f"{eb.sensor1.humidity/1024:.2f}")

        if (temp_zemlja != _temp_zemlja or vlaga_zemlja != _vlaga_zemlja):

            zemlja(temp_zemlja, vlaga_zemlja)
            _temp_zemlja = temp_zemlja
            _vlaga_zemlja = vlaga_zemlja
