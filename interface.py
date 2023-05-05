from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import numpy as np
import subprocess
from termcolor import colored, cprint
import time
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from commandes import *
from datetime import datetime

port_boitier='/dev/ttyUSB0'
port_roue='/dev/ttyUSB1'
baudrate_boitier=9600
baudrate_roue=115200


# paramètres affichage #
c1='#41B77F'
red='#FC0101'
black='#000000'
text_size=12
title_size = 18
button_text_size=10
small_size=7

# initialisation fenêtre #
root = Tk()
root.title("Command panel")
root.geometry("960x900")
root.minsize(480,360)
root.config(background=black)


frametop=Frame(root,bg=black)

def closeboitier():
	global boitier
	try:
		boitier.close()
		cprint('Boitier fermé','white','on_red')
	except:
		cprint('Erreur fermeture boitier','white','on_red')
def openboitier():
	global boitier
	try:
		boitier.close()
	except:
		pass
	try:
		boitier=serial.Serial(port_boitier,baudrate=baudrate_boitier,timeout=10)
		cprint('Boitier ouvert','white','on_green')
		rep=lire(boitier,b't')
		if rep==b'T':
			cprint('et testé','white','on_green')
		else:
			cprint('et ne répond pas','on_red')
	except:
		cprint('Erreur lecture boitier','white','on_magenta')


frametopleft=Frame(frametop,bg=black)
frametoptop=Frame(frametop,bg=black)
Label(frametoptop, text="Serial connexions", font=('Courrier',title_size),bg=black,fg='white').pack()

frameboitier=Frame(frametoptop,bg=black)
openboitier_button=Button(frameboitier,text='Open Boitier',command=openboitier)
openboitier_button.pack(padx=5,pady=10)
closeboitier_button=Button(frameboitier,text='Close Boitier',command=closeboitier)
closeboitier_button.pack(padx=5,pady=10)

def closeroue():
	global roue
	try:
		roue.close()
		cprint('Roue fermée','white','on_red')
	except:
		cprint('Erreur fermeture roue','white','on_red')
def openroue():
	global roue
	try:
		roue.close()
	except:
		pass
	try:
		roue=serial.Serial(port_roue,baudrate=baudrate_roue,timeout=10)
		cprint('Roue ouverte','white','on_green')
	except:
		cprint('Erreur lecture roue','white','on_magenta')


frameroue=Frame(frametoptop,bg=black)
openroue_button=Button(frameroue,text='Open Roue',command=openroue)
openroue_button.pack(padx=5,pady=10)
closeroue_button=Button(frameroue,text='Close Roue',command=closeroue)
closeroue_button.pack(padx=5,pady=10)

frametopright=Frame(frametop,bg=black)


#############
framedir=Frame(frametopleft,bg=black)
Label(framedir, text="Directory", font=('Courrier',title_size),bg=black,fg='white').pack()
create_var=StringVar()
def create_new_folder(): #ne fonctionne pas
	global initial_folder,create_entry
	initial_folder=filedialog.askdirectory()
	#initial_folder_path.set(initial_folder)
	newfolder_name=create_entry.get()
	#subprocess.call(str('bash cd '+str(initial_folder)),shell=True)
	newfolder_path=str(initial_folder+'/'+str(newfolder_name))
	print(str('bash mkdir ' + str(newfolder_path)))
	subprocess.call(str('bash mkdir ' + str(newfolder_path)),shell=True)
create_var.set(str('Newfolder'))
create_entry=Entry(framedir,textvariable=create_var)
create_entry.pack(padx=10)


create_button=Button(framedir,text='Create new folder',command=create_new_folder)
create_button.pack(ipadx=5,pady=15)

def select_parent_folder():
	global folder,folder_path
	folder=filedialog.askdirectory()
	folder_path.set(folder)
	Label(framedir, text=folder, font=('Courrier',small_size),bg='white',fg=black).pack()
button=Button(framedir, text="Select parent directory", command= select_parent_folder)
button.pack(ipadx=5, pady=15)


def select_photo_folder():
	global folder,folder_path,folder_photo
	folder_photo=filedialog.askdirectory(initialdir=folder)
	folder_photo_path.set(folder_photo)
	Label(framedir, text=folder_photo, font=('Courrier',small_size),bg='white',fg=black).pack()

button_photo=Button(framedir, text="Select photo directory", command= select_photo_folder)
button_photo.pack(ipadx=5, pady=15)

folder_path = StringVar()
folder_photo_path = StringVar()
folder_photo = StringVar()

##############
framefile=Frame(frametopright,bg=black)
def select_file():
	global file_posmot, file_path, folder, fileposmot
	fileposmot=filedialog.askopenfilename(initialdir=folder,filetypes=[('TXT','*.txt')])
	file_path.set(fileposmot)
	Label(framefile, text=fileposmot, font=('Courrier',small_size),bg='white',fg=black).pack()
Label(framefile, text="File posmot", font=('Courrier',title_size),bg=black,fg='white').pack()
button_file=Button(framefile, text="Select file", command= select_file)
button_file.pack(ipadx=5, pady=15)

def plot_posmot():
	global fileposmot
	fposmot=np.loadtxt(fileposmot,skiprows=2,unpack=True,delimiter=';')
	machine_t=np.array(fposmot[0][1:-1])
	machine_pos=np.array(fposmot[1][1:-1])
	real_t=machine_t-machine_t[0]
	real_pos=machine_pos/3.2/50
	real_v=(real_pos[-1]-real_pos[1])/(real_t[-1]-real_t[1])
	print('Veff = ',real_v,' µm/s')
	#fig1=plt.figure(figsize=(3,3),dpi=100)
	#bar1=FigureCanvasTkAgg(fig1,framefile)
	#bar1.get_tk_widget().pack(side=LEFT,fill=BOTH)
	#ax1=fig1.add_subplot(111)
	plt.scatter(real_t,real_pos,label='Data')
	plt.plot(real_t,real_pos[0]+real_t*real_v,color='r',label=f'Fit vmoy = {round(real_v,3)} µm/s')
	plt.xlabel('t (s)')
	plt.ylabel('d (µm)')
	plt.legend(loc='upper right')
	#fig1.set_tight_layout(True)
	plt.show()
button_plot=Button(framefile,text='Plot motor positions',command=plot_posmot)
button_plot.pack(ipadx=5,pady=15)

file_path=StringVar()
##############
frametopbottom=Frame(frametop,bg=black)
Label(frametopbottom, text="Metadata", font=('Courrier',title_size),bg=black,fg='white').pack()
text=["Name","Liquid","Bottom surface","Top surface"]
#var0=['SL','Liquid','Wafer','Si prism']
VAR=[StringVar(),StringVar(),StringVar(),StringVar()]
ENTRY=['','','','']
for i in range(len(text)):
	#label=Label(frametopbottom,text=text[i],font=("Courrier",text_size),bg=black,fg="white")
	#label.pack()
	VAR[i].set(text[i])
	ENTRY[i]=Entry(frametopbottom,textvariable=VAR[i])
	ENTRY[i].pack(padx=10)
def save_MD():
	global folder
	print(folder)
	timestr=time.strftime("%Y%m%d")
	path_file=str(folder+'/Setup_'+str(timestr)+'.txt')
	operator=ENTRY[0].get()
	liquid=ENTRY[1].get()
	bsurface=ENTRY[2].get()
	tsurface=ENTRY[3].get()
	MD=str('Operator = '+str(operator)+'\n'+'Liquid = '+str(liquid)+'\n'+'Bottom surface = '+str(bsurface)+'\n'+'Top surface = '+str(tsurface)+'\n')
	try:
		f=open(path_file,'a')
		print('MD file modified')
	except:
		f=open(path_file,'w')
		print('MD file created and modified')
	f.write(MD)
	f.close()
save_button=Button(frametopbottom,text='Save Metadata',font=('Courrier',button_text_size),bg='white',fg=black,command=save_MD)
save_button.pack(pady=10)



##############
framebottom=Frame(root,bg=c1)

frame0=Frame(framebottom,bg=black)
title_frame0=Label(frame0,text="LASER",font=('Courrier',title_size),bg=black,fg='white')
title_frame0.pack(fill='x')


# initialisation #

try:
	boitier=serial.Serial(port_boitier,baudrate_boitier,timeout=20)
	cprint('Boitier ouvert et testé','white','on_green')
except:
	cprint('Erreur lecture boitier','white','on_magenta')
try:
	roue=serial.Serial(port_roue,baudrate_roue)
	cprint('Roue ouverte et testée','white','on_green')
except:
	cprint('Erreur lecture roue','white','on_magenta')

etat_main,etat_att=False,False

#
# Controle #
def get_etat_shutters():
	global etat_main,etat_att
	rep=lire(boitier,b'c')
	if rep.find(b'a')!=-1:
		etat_att=False
	elif rep.find(b'A')!=-1:
		etat_att=True
	if rep.find(b's')!=-1:
		etat_main=False
	elif rep.find(b'S')!=-1:
		etat_main=True
	else:
		cprint('Erreur sur signal shutter','white','on_magenta')
	return [etat_main,etat_att]

temps=800
def set_tps_bleach(): #ne fonctionne pas
	global setbleach_entry
	tps_bleach=setbleach_entry.get()
	rep=lire(boitier,bytes(str(tps_bleach),'utf-8')+b'b')
	print('Bleach time set to',tps_bleach)
setbleach_label=Label(frame0,text="Bleach time",font=("Courrier",text_size),bg=black,fg="white")
setbleach_label.pack()
setbleach_variable=StringVar()
setbleach_variable.set("800")
setbleach_entry=Entry(frame0,textvariable=setbleach_variable)
setbleach_entry.pack(padx=10)
setbleach_button=Button(frame0,text='Set bleach time',font=('Courrier',button_text_size),bg=c1,fg=black,command=set_tps_bleach)
setbleach_button.pack(pady=10)

def bleach():
	global setbleach_entry
	tps_bleach=setbleach_entry.get()
	rep0=lire(boitier,bytes(str(tps_bleach),'utf-8')+b'b')
	lire(boitier,b'h')
bleach_button=Button(frame0,text='Bleach',font=('Courrier',button_text_size),bg=c1,fg=black,command=bleach)
bleach_button.pack(pady=10)

def att():
	global etat_main,etat_att
	get_etat_shutters()
	if etat_att:
		lire(boitier,b'a')
		#Label(frame0, text='Atténuateur fermé', font=button_text_size,bg='white',fg=c1).pack()
		cprint('Attenuator closed','grey','on_white')
	else:
		lire(boitier,b'A')
		#Label(frame0, text='Atténuateur ouvert', font=button_text_size,bg='white',fg=c1).pack()
		cprint('Attenuator opened','white','on_blue')
att_button=Button(frame0,text='Attenuator',font=('Courrier',button_text_size),bg=c1,fg=black,command=att)
att_button.pack(pady=10)

def main():
	global etat_main,etat_att
	get_etat_shutters()
	if etat_main:
		lire(boitier,b's')
		#Label(frame0, text='Main shutter closed', font=button_text_size,bg='white',fg=c1).pack()
		cprint('Main shutter closed','grey','on_white')
	else:
		lire(boitier,b'S')
		#Label(frame0, text='Main shutter opened', font=button_text_size,bg='white',fg=c1).pack()
		cprint('Main shutter opened','white','on_blue')
main_button=Button(frame0,text='Main shutter', font=('Courrier',button_text_size),bg=c1,fg=black,command=main)
main_button.pack(pady=10)

def shutters():
	global etat_main, etat_att
	[etat_main,etat_att]=get_etat_shutters()
	if etat_main:
		cprint('Main shutter opened','white','on_blue')
	else:
		cprint('Main shutter closed','grey','on_white')
	if etat_att:
		cprint('Attenuator opened','white','on_blue')
	else:
		cprint('Attenuator closed','grey','on_white')
shutters_button=Button(frame0,text='Etat shutters', font=('Courrier',button_text_size),bg=c1,fg=black,command=shutters)
shutters_button.pack(pady=10)


#sep01=ttk.Separator(frame0,orient='vertical')
#sep01.pack(fill='y')

frame1=Frame(framebottom,bg=black)
title_frame1=Label(frame1,text="Moteur",font=('Courrier',title_size),bg=black,fg='white')
title_frame1.pack()


def get_pos_moteur():
	global folder
	rep=str(lire(boitier,b'K'))
	rep2=rep.replace('\\r','').replace('\'','').split(' ')
	position=int(rep2[1])
	path_posmot=str(str(folder)+'/posmot.txt')
	try:
		f=open(path_posmot,'a')
		#f.write('prout')
		f.write(str(str(time.time())+';'+str(position)+'\n'))
		f.close()
	except:
		print('File posmot.txt not found')
	print(position)
	if position >= 216000:
		print('ATTENTION : limite vis micrométrique atteinte !')
	return position

def set_pos_moteur(sens,vitesse,pos_cible):
	if sens:
		message='J'
	else:
		message='I'
	message+=str(vitesse)+'V'+str(pos_cible)+'NW'
	lire(boitier,bytes(message, 'utf-8'))


getpos_button=Button(frame1,text='Get pos mot', font=('Courrier',button_text_size),bg='white',fg=black,command=get_pos_moteur)
getpos_button.pack(pady=10)
#Label(frame1, text=, font=button_text_size,bg='white',fg=c1).pack()


vitesse_query = Label(frame1,text="Vitesse (µm/s)",font=("Courrier",text_size),bg=black,fg="white")
vitesse_query.pack()
vitesse_var = StringVar()
vitesse_var.set("5")
vitesse_entry = Entry(frame1,textvariable=vitesse_var)
vitesse_entry.pack(pady=10)


tempscis_query = Label(frame1,text="Temps cisaillé (s)",font=("Courrier",text_size),bg=black,fg="white")
tempscis_query.pack()
tempscis_var = StringVar()
tempscis_var.set("10")
tempscis_entry = Entry(frame1,textvariable=tempscis_var)
tempscis_entry.pack(pady=10)

sens_var = IntVar()
sens_choice = Checkbutton(frame1,variable=sens_var,text="Reverse shear?",font=("Courrier",text_size),bg=black,fg="white",onvalue=1,offvalue=0,selectcolor=red)
sens_choice.pack(pady=10)

def cis():
	global folder
	sens=sens_var.get()
	vitesse=vitesse_entry.get()
	tempscis=tempscis_entry.get()
	path_posmot=str(str(folder)+'/posmot.txt')
	f=open(path_posmot,"w")
	f.write(str('sens='+str(sens)+';vitesse='+str(vitesse)+';tempscis='+str(tempscis)+'\n'))
	f.write('tempsabsolu;posmot\n')
	f.close()
	if float(vitesse)>0.1 and float(vitesse)<32:
		coef=3.2
		coef_SL=1

		#réducteur 50:1
		rap_vit=0.0178
		rap_pos=50
		#avec réducteur
		vit_mot=int(65535-1e6/(float(vitesse)*coef_SL*coef*12.8/rap_vit))
		distance=float(vitesse)*float(tempscis)
		pos=get_pos_moteur()
		pos0=pos
		if sens: #left
			pos_cible=pos-distance*coef*rap_pos
			sign=-1
		else:
			pos_cible=pos+distance*coef*rap_pos
			sign=1
		sens_change=sens
		t0=time.time()
		set_pos_moteur(sens_change,vit_mot,pos_cible)

		print('Distance à cisailler =')
		print(distance)
		while sign*(pos_cible-get_pos_moteur())>0:
			tps=time.time()-t0
		else:
			tf=time.time()
		posf=get_pos_moteur()
		DELTApos=abs(posf-pos0)/coef/rap_pos
		DELTAt=tf-t0
		Veff=DELTApos/DELTAt
		print('Durée effective')
		print(DELTAt)
		print('Distance parcourure')
		print(DELTApos)
		print('Vitesse effective')
		print(Veff)
		now=datetime.now()
		timestr=str(str(now.strftime("%Y%m%d"))+'_'+str(now.strftime("%H%M%S")))
		path_copy0=str(str(folder)+'/posmot.txt')
		path_copy1=str(str(folder)+'/posmot_'+str(timestr)+'.txt')
		subprocess.call(str('cp '+path_copy0+' '+path_copy1),shell=True)

	else:
		print('Vitesse hors range')



shear_button=Button(frame1,text='Shear', font=('Courrier',12),bg='white',fg=black,command=cis)
shear_button.pack(pady=10)



frame2=Frame(framebottom,bg=black)
title_frame2=Label(frame2,text="Photos",font=('Courrier',title_size),bg=black,fg='white')
title_frame2.pack()

def take_photo():
	global folder_photo,etat_main
	iso = spinboxi1.get()
	ss = spinboxss1.get()
	type_p = tp_entry.get()
	multiple = varCB.get()
	print(multiple)
	if multiple == 0:
		if etat_main:
			main()
		tbefore=[time.time()]
		subprocess.call(str('bash photo.sh -n 1 -i ' + str(iso) + ' -v ' + str(ss)+' -o '+str(type_p)+' -p' +str(folder_photo)),shell=True)
		tafter=[time.time()]
		time.sleep(0.8)
		if not etat_main:
			main()
	else:
		tbefore,tafter=[],[]
		ti = spinboxti1.get()
		nbp = spinboxnbp1.get()
		for i in range(int(nbp)):
			print('Photo number ',i+1,'/',nbp)
			if etat_main:
				main()
			tbefore.append(time.time())
			subprocess.call(str('bash photo.sh -n 1 -i ' + str(iso) + ' -v ' + str(ss)+' -o '+str(type_p)+' -p' +str(folder_photo)),shell=True)
			tafter.append(time.time())
			if float(ti)>0.8:
				if not etat_main:
					main()
				time.sleep(float(ti))
			else:
				print('Intervalle de temps fixé à 0.8s par défaut')
				time.sleep(0.8)
	try:
		fpic=open(str(str(folder_photo)+'/time_pic.txt'),'r')
		fpic.close()
	except:
		fpic=open(str(str(folder_photo)+'/time_pic.txt'),'w')
		fpic.write('type;tbefore;tafter\n')
		fpic.close()
	fpic=open(str(str(folder_photo)+'/time_pic.txt'),'a')
	for i in range(len(tbefore)):
		fpic.write(str(str(type_p)+';'+str(tbefore[i])+';'+str(tafter[i])+'\n'))
	fpic.close()

ISO = Label(frame2,text="ISO",font=("Courrier",text_size),bg=black,fg="white")
ISO.pack(pady=1)
spinboxi1 = Spinbox(frame2, from_=0, to=30, increment=1)
spinboxi1.delete(0,30)
spinboxi1.insert(0,28)
spinboxi1.pack(pady=1)

SS = Label(frame2,text="Shutter Speed",font=("Courrier",text_size),bg=black,fg="white")
SS.pack()
spinboxss1 = Spinbox(frame2, from_=0, to=52, increment=1)
spinboxss1.delete(0,52)
spinboxss1.insert(0,32)
spinboxss1.pack(pady=1)

tp_label = Label(frame2,text="Type of picture",font=("Courrier",text_size),bg=black,fg="white")
tp_label.pack()
tp = StringVar()
tp.set("tb")
tp_entry = Entry(frame2,textvariable=tp)
tp_entry.pack(pady=1)

varCB = IntVar()
CB = Checkbutton(frame2,variable=varCB,text="Several pictures ?",font=("Courrier",text_size),bg=black,fg="white",onvalue=1,offvalue=0,selectcolor=red)
CB.pack(pady=1)

TI = Label(frame2,text="Time interval",font=("Courrier",text_size),bg=black,fg="white")
TI.pack()
spinboxti1 = Spinbox(frame2, from_=1, to=60, increment=1)
spinboxti1.delete(0,60)
spinboxti1.insert(0,4)
spinboxti1.pack(pady=1)

NBP = Label(frame2,text="Number of pictures",font=("Courrier",text_size),bg=black,fg="white")
NBP.pack()
spinboxnbp1 = Spinbox(frame2, from_=1, to=200, increment=1)
spinboxnbp1.delete(0,200)
spinboxnbp1.insert(0,30)
spinboxnbp1.pack(pady=1)

button = Button(frame2,text="Capture",font=("Courrier",button_text_size),bg="white",fg=black,command=take_photo)
button.pack(pady=10,padx=10)

def close_all():
	global root
	closeboitier()
	closeroue()
	root.destroy()

frameend=Frame(framebottom,bg=red)
title_frameend=Label(frameend,text="EXIT",font=('Courrier',title_size),bg=red,fg=black)
title_frameend.pack(fill='x')
end_button=Button(frameend,text='Close all',font=('Courrier',button_text_size),bg="white",fg=red,command=close_all)
end_button.pack(pady=10,padx=10)


frametop.pack(side=TOP,fill=BOTH)
frametoptop.pack(side=TOP)
frametopleft.pack(side=LEFT,fill=BOTH)
frametopright.pack(side=RIGHT,fill=BOTH)
frametopbottom.pack(side=BOTTOM)
framebottom.pack(side=BOTTOM,fill=BOTH)
framedir.pack(side=TOP,fill=BOTH)
framefile.pack(side=TOP,fill=BOTH)
frame0.pack(side=LEFT,fill=BOTH)
frame2.pack(side=RIGHT,fill=BOTH)
frame1.pack(side=TOP,fill=BOTH)
frameboitier.pack(side=LEFT,fill=BOTH)
frameroue.pack(side=RIGHT,fill=BOTH)
frameend.pack(side=BOTTOM,fill=BOTH)
#######

root.mainloop()
