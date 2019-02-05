import os
import time
import datetime
import socket
import random
import signal


#import threading #WILL SUPPORT
#import ipaddr #GOOGLE SORCE CODE

#status = 0 # status of connection

def Menu():
#	global loggin
	global choice
	global verbose
	global net4
	print "\n\
 ____           _               _   \n\
| __ )  ___ ___| | ___   _ _ __| |_ \n\
|  _ \ / _ \_  / |/ / | | | '__| __|\n\
| |_) | (_) / /|   <| |_| | |  | |_ \n\
|____/ \___/___|_|\_\\__,_|_|   \__|\n\
\n\
    ___                      _           ________________          \n\
   /   |  ____  ____  ____  (_)___ ___  / ____/_  __/ __ \        \n\
  / /| | / __ \/ __ \/ __ \/ / __ `__ \/ /_    / / / /_/ /       \n\
 / ___ |/ / / / /_/ / / / / / / / / / / __/   / / / ____/     \n\
/_/  |_/_/ /_/\____/_/ /_/_/_/ /_/ /_/_/     /_/ /_/              \n\
                                           by ankongeneral       \n\
\n\
	Bu Arac FTP Agi Taramak Icindir.\n\
	FTP Ve Anonim Baglantilari Kullanan Sunucular Icindir.\n\
	1)IP Aralik Ve Baglanti Kullanin. Ve anonim girisleri kontrol edin.\n\
	2)Gelecekte Maskeleme Ve Destek Kullanacak.\n\
	3)IP Listesi Olusturucu\n"
	#logging = str(raw_input("[*] Would you like to enable loging? Yes(Y) or No(N)"))   #Will Support Logging of data and what you want to store
	verbose = str(raw_input("[*] Ayrintili veya VV ister misiniz? Evet (Y) veya VV (vv) veya Hayir icin bos birakin: "))
	if verbose == "yes" or verbose == "Yes" or verbose ==  "YES" or verbose == "y" or verbose == "Y" or verbose == "v":
		verbose = 1
		print bcolors.Green + "[*] Ayrintili Etkinlestirildi", bcolors.ENDC
	elif verbose == "VV" or verbose == "vv":
		verbose = 2
		print bcolors.Green + "[*] Cok Ayrintili Etkinlestirildi", bcolors.ENDC
	choice = str(raw_input("[*] Hangi Secenegi Yapmak Istersin : "))
	return choice, #logging # will return loggin value
	
def ChoiceSelection():
	global status
	if choice == "1":
		if verbose == 1 or verbose == 2:
			print bcolors.Green + "[*] IP Menzil Olusturucuyu Baslatma", bcolors.ENDC
		#print "\nWhat is you network range you would like to scan using masking?"
		#print "Using classfull maksing:\n\
	#/8 = 255.0.0.0        ex. 192.0.0.0/8\n\
	#/16 = 255.255.0.0     ex. 192.168.0.0/16\n\
	#/24 = 255.255.255.0   ex. 192.168.1.0/24\n\
	#	Classless is also supported:\n\
	#/25 = 255.255.255.128 ex. 192.168.1.0/25 = .0 -> .127\n"
		#net4 = raw_input("[*]What is your IP: ")   #Still not working -- NEED TO CONVERT OUTPUT TO STRING
		#net4 = ipaddr.IPv4Network(net4)			#Still not working
		start_ip = raw_input("[*] Baslangic IP Adresi Nedir: ")
		end_ip = raw_input("[*] Bitis IP Adresi Nedir: ")
		ipRange(start_ip,end_ip)
		status = 0
		#port = []
		#port.append(21)
		#port.append(990)
		if verbose == 1 or verbose == 2:
			print bcolors.Green + "[*] Port Taramasi Baslatiliyor", bcolors.ENDC
		for address in ip_range:
			portscan(address,port)
			if status == 1:
				if verbose == 1 or verbose == 2:
					print bcolors.Green + "[*] Adresine Anonim Giris Baslatiliyor:", address, bcolors.ENDC
				AnonLogin(address,port)
			status = 0	
	if choice == "3":
		count = 0
		net4 = raw_input("[*] IP'niz Nedir: ") 
		if verbose == 1 or verbose == 2:
			print bcolors.Green + "[*] Dosyayi Ipaddress.txt Olarak Acilmaya Baslatiliyor", bcolors.ENDC
		try:
			output = open("Ipaddress.txt" ,"ab+")
		except:
			print bcolors.Red + "Dosya Olusturulamadi!", bcolors.ENDC
			main()
		net4 = ipaddr.IPv4Network(net4)
		if verbose == 1 or verbose == 2:
			print bcolors.Green + "[*] IP'leri Dosyaya Yazmaya Baslatiliyor", bcolors.ENDC
		for x in net4.iterhosts():  # will use this for masking
			count += 1
			k = x
			k = str(k)
			try:
				output.write(k + "\n");
			except:
				print bcolors.Red + "Dosya Yazilamadi!", bcolors.ENDC 
				print IOError
				print "Eve Geri Donuluyor...."
				main()
		output.close()
		print bcolors.Green + "[*] DIR'de Calisirken Ipaddress.txt Olarak Kaydedildi", bcolors.ENDC
		print bcolors.Green + "[*] Sozler:", count, " IP Kullanicisinin", bcolors.ENDC
		
	main()

def signal_handler(signum, frame):
	raise Exception("Zaman Asimina Ugradi!")
	

def ipRange(start_ip, end_ip):
   global ip_range
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []
   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))    
   return ip_range

def AnonLogin(address,port):
	ftp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ftp.settimeout(9)
	try: 
		ftp.connect((address, port)); # passing it our address and port we want to connect to
		banner=ftp.recv(45)
		signal.signal(signal.SIGALRM, signal_handler)
		signal.alarm(3)
		try:
			banner += ftp.recv(1024) # receive the rest of the banner
		except: 
			pass
		if verbose == 1 or verbose ==2:
			print banner
		banner.replace("\r\n", ' ')
		ftp.send("USER anonymous\r\n")
		ftp.recv(1024)
		ftp.send("PASS anon@\r\n")
		response=ftp.recv(1024)
		if verbose == 1 or verbose == 2:
			print response
		try:
			if response.index("230")!=-1:
				status="Basarili"
				print bcolors.Cyan + "-----Basarili-----", bcolors.ENDC
				print "[*]", address, "", status, "Anonim Oturum Portu:", port
				input("Kapatmak Icin Enter Tusuna Basin ...")
		except ValueError:
			status="Basarisizlik"
			if verbose == 1 or verbose == 2:
				print bcolors.FAIL + "[*]", status, "Giris Yaparken", address, bcolors.ENDC
		else:
			print status
	except socket.error: # if we cant connect at all we will pass
		pass
	ftp.close()
	return

def portscan(address,port): # will perfrom a socket connection and if error detection is seen it will return status of 0
	global verbose
	global status
	status = 0
	port = [21] #still working this list / LOOP out but it works for now
	address = str(address)
	for portscan in port:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(1) #how long will we wait to hear for a connection "NEED TO ADD OPTION FOR THIS"
			s.connect((address,21))
			if verbose == 1 or verbose == 2:
				print bcolors.Magenta + "[*]", address,"uzerinde: ",portscan,"Acik", bcolors.ENDC
				if portscan == 990:
					print bcolors.Magenta + "[-] Muhtemelen Uzerinde Bir SFTP Servisi Bulundu", portscan, bcolors.ENDC
			s.shutdown(socket.SHUT_RDWR)
			s.close
			status = 1
		except socket.error as msg: # we can print the caught error
			if verbose == 2:
				print bcolors.Yellow +"[*]", msg, bcolors.ENDC
				print bcolors.Yellow + "[*] Baglanti Noktasinda Hata:", portscan, "en:", address, bcolors.ENDC
			err = True
		except: continue # if its not a socket error? Do i need this?
		finally: #insuring that the socket is closed to be reopened 
			s.close()
	return status
	
	
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'	
	Red = '\033[91m'
	Green = '\033[92m'
	Blue = '\033[94m'
	Cyan = '\033[96m'
	White = '\033[97m'
	Yellow = '\033[93m'
	Magenta = '\033[95m'
	Grey = '\033[90m'
	Black = '\033[90m'
	Default = '\033[99m'
	

def main():
	global choice
	global port
	global verbose
	global start_ip
	global end_ip
	print bcolors.WARNING + "Uyari Bu, internette tarama yapmak kendi sorumlulugunuzda olacaktir :)" + bcolors.ENDC
	port = 21 # global port we want to check 
	Menu() #Print Menu
	ChoiceSelection() # What we do if we pick something

		

if __name__=="__main__":
    main()
