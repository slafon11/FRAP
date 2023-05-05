import serial
from termcolor import colored, cprint
import time


def lire(obj,message):
	obj.write(message)
	out=b''
	time.sleep(0.2)
	while obj.inWaiting() >0:
		out+=obj.read(1)
	return out

def close(port,baudrate):
	obj=serial.Serial(port,baudrate)
	try:
		obj.close()
	except:
		0


def test_boitier(port,baudrate):
	try:
		obj=serial.Serial(port,baudrate)
		rep=lire(port, baudrate,b't')
		if rep==b'T':
			cprint('Boitier opened and tested.','white','on_green')
		else:
			cprint('Erreur 1 de lecture du boitier','white','on_magenta')
			close(port,baudrate)
	except:
		cprint('Erreur 2 de lecture du boitier','white','on_magenta')

def test_roue(port,baudrate):
	try:
		obj=serial.Serial(port,baudrate)
		cprint('Roue opened','white','on_green')
	except:
		cprint('Could not open wheel','white','on_magenta')


def set_tps_bleach(port,baudrate,temps):
	obj=serial.Serial(port,baudrate)
	obj.lire()
