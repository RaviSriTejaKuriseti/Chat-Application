import threading
import socket


def thread_to_send(soc):
	
	while True:
		try:
			msg=input()
			X=msg.split(" ",1)

			if(X[0][0]!="@"):
				print("Message is not in Valid Format.Please Type Again")
			else:
				fmg="SEND"+" "+X[0][1:]+" "+"\n\n"+str(len(X[1]))+"\n\n"+X[1]
				soc.send(bytes(fmg,("utf-8")))

		except:
			soc.close()
			return

	
def thread_to_recv(soc):
	while True:
		try:
			data=soc.recv(4096).decode("utf-8")
			U=data.split()
			L=data.split("\n\n")
			if(len(U)>2 and U[0]=="ERROR"):
				print(L[0])
			elif(U[0]=="SEND"):
				print("Message delivered to"+":-"+U[1])
			else:
				if(len(L)==3):
					A1=L[0].split()
					recep_usr=A1[1]
					if(A1[0]=="FORWARD"):
						if(len(L[2])!=int(L[1])):
							m3="ERROR 103 Header Incomplete\n\n"
							soc.send(bytes(m3,("utf-8")))
						else:
							print("Message from "+recep_usr+":-"+L[2])
							m3="RECEIVED"+" "+recep_usr+"\n\n"
							soc.send(bytes(m3,("utf-8")))

					
		except:
			soc.close()
			return


def main():
	uname=str(input("Enter the UserName:-"))
	hostname=str(input("Enter the Server's IP Address:-"))
	host="127.0.0.1"
	host=hostname
	port=12345
	Clientsoc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		Clientsoc.connect((host,port))
		print("Connected to Server")
	except:
		print("Cannot connect to server")
		sys.exit()

	soc=Clientsoc
	reg_msg="REGISTER TOSEND"+" "+uname+"\n\n"
	soc.send(reg_msg.encode("utf-8"))
	print("Registering"+" "+uname+" "+"to send messages")
	data=soc.recv(4096).decode("utf-8")
	if(data=="REGISTERED TOSEND"+" "+uname+"\n\n"):
		print("Registered"+" "+uname+" "+"to send messages")
	else:
		if(data=="ERROR 100 Malformed username"+"\n\n"):
			print(data)
			print("Please Enter a Valid Username")
		elif(data=="ERROR 101 No user registered"+"\n\n"):
			print(data)
			print("Please send registration message")
		elif(data=="Improper Registration Message"+"\n\n"):
			print("Please send proper registration message")
			
		elif(data=="Username was already issued"):
			print(data)
			print("Please use another username")

		soc.close()
		return

	reg_msg1="REGISTER TORECV"+" "+uname+"\n\n"
	soc.send(reg_msg1.encode("utf-8"))
	print("Registering"+" "+uname+" "+"to receieve messages")
	data=soc.recv(4096).decode("utf-8")
	if(data=="REGISTERED TORECV"+" "+uname+"\n\n"):
		print("Registered"+" "+uname+" "+"to receieve messages")
	t1=threading.Thread(target=thread_to_send,args=(soc,))
	t1.start()
	t2=threading.Thread(target=thread_to_recv,args=(soc,))
	t2.start()


main()




