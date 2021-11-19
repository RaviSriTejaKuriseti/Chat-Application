import socket
import _thread

def reg_process(msg):
	if(len(msg)<=2):
		return (-1,-1)
	else:
		U=msg.split()
		uname=U[2]
		if(U[0]=="REGISTER" and U[1]=="TOSEND" and msg[-1]==msg[-2]=="\n"):
			if(U[2].isalnum()):
				return (1,1,uname)
			else:
				return (0,1,uname)
		elif(U[0]=="REGISTER" and U[1]=="TORECV" and msg[-1]==msg[-2]=="\n"):
			if(U[2].isalnum()):
				return (1,0,uname)
			else:
				return (0,0,uname)
		else:
			return (-1,-1)


def get_key(dic,val):
	for e in dic:
		if(dic[e]==val):
			return e
	return -1


def connect_to_client(nsock,addr,client_map):
	try:
		data=nsock.recv(4096).decode("utf-8")
		A=reg_process(data)

		if(A[0]==0):
			msgg="ERROR 100 Malformed username\n\n"
			nsock.send(msgg.encode("utf-8"))
		elif(A[0]==-1):
			msgg="ERROR 101 No user registered"+"\n\n"
			nsock.send(msgg.encode("utf-8"))
			msg1="Improper Registration Message"+"\n\n"
			nsock.send(msg1.encode("utf-8"))
		else:
			uname=A[2]
			if(uname in client_map.values()):
				msgg="Username was already issued"
				nsock.send(msgg.encode("utf-8"))
				nsock.close()
			else:
				client_map[nsock]=uname
				m1="REGISTERED TOSEND"+" "+A[2]+"\n\n"
				nsock.send(m1.encode("utf-8"))
				m2="REGISTERED TORECV"+" "+A[2]+"\n\n"
				nsock.send(m2.encode("utf-8"))
				print(uname+" "+"Connected to server")
				while(True):
					msg=nsock.recv(4096).decode("utf-8")
					L=msg.split("\n\n")
					if(len(L)==3):
						A1=L[0].split()
						recep_usr=A1[1]
						if(A1[0]=="SEND"):
							if(len(L[2])!=int(L[1])):
								m3="ERROR 103 Header Incomplete\n\n"
								nsock.send(bytes(m3,("utf-8")))
							else:
								if(recep_usr=="ALL"):
									send_all(nsock,client_map,L[1],L[2])

								elif(recep_usr not in client_map.values()):
									m3="ERROR 102 Unable to Send\n\n"
									nsock.send(bytes(m3,("utf-8")))
								else:
									m3="SEND"+" "+recep_usr+"\n\n"
									nsock.send(bytes(m3,("utf-8")))
									fmg="FORWARD"+" "+client_map[nsock]+" "+"\n\n"+L[1]+"\n\n"+L[2]
									get_key(client_map,recep_usr).send(bytes(fmg,("utf-8")))
						else:
							print("Invalid Message")
							nsock.close()


					else:
						if(len(L)==1):
							A1=L[0].split()
							if(len(A1)==2 and A1[0]=="RECEIVED" and A1[1] in client_map.values()):
								print(A1[1]+" "+"received his message")
							elif(len(A1)==4 and A1==["Error","103","Header","Incomplete"]):
								print("Message sent with incomplete header")
							else:
								print("Invalid Message")
								nsock.close()

					
	except:
		print(uname+" "+"Connection lost")
		client_map.pop(nsock)
		nsock.close()



def send_all(nsock,client_map,u,v):
	for e in client_map:
		msg="SEND"+" "+client_map[e]+"\n\n"
		nsock.send(bytes(msg,("utf-8")))
		fmg="FORWARD"+" "+client_map[nsock]+" "+"\n\n"+u+"\n\n"+v
		e.send(bytes(fmg,("utf-8")))
		

client_map={}
port=12345
Serversoc=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP-SOCKET in python
Serversoc.bind(("127.0.0.1",port)) #localhost
Serversoc.listen(10) #listen atmost 10 clients at at time
print("Server is Active")
while True:
	sock=Serversoc
	nsock,addr=sock.accept()
	_thread.start_new_thread(connect_to_client,(nsock,addr,client_map))   #new thread for each client
