import sys
import os
import json
import uuid
import logging
from queue import  Queue

class Chat:
	def __init__(self):
		self.sessions={}
		self.users = {}
		self.users['messi']={ 'nama': 'Lionel Messi', 'negara': 'Argentina', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
		self.users['henderson']={ 'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['lineker']={ 'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya','incoming': {}, 'outgoing':{}}
	def proses(self,data):
		j=data.split(" ")
		try:
			command=j[0].strip()
			if (command=='auth'):
				username=j[1].strip()
				password=j[2].strip()
				logging.warning("AUTH: auth {} {}" . format(username,password))
				return self.autentikasi_user(username,password)
			elif (command=='send'):
				sessionid = j[1].strip()
				usernameto = j[2].strip()
				message=""
				for w in j[3:]:
					message="{} {}" . format(message,w)
				usernamefrom = self.sessions[sessionid]['username']
				logging.warning("SEND: session {} send message from {} to {}" . format(sessionid, usernamefrom,usernameto))
				return self.send_message(sessionid,usernamefrom,usernameto,message)
			elif (command=='inbox'):
				sessionid = j[1].strip()
				username = self.sessions[sessionid]['username']
				logging.warning("INBOX: {}" . format(sessionid))
				return self.get_inbox(username)
			else:
				return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
		except KeyError:
			return { 'status': 'ERROR', 'message' : 'Informasi tidak ditemukan'}
		except IndexError:
			return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}
	def autentikasi_user(self,username,password):
		if (username not in self.users):
			return { 'status': 'ERROR', 'message': 'User Tidak Ada' }
		if (self.users[username]['password']!= password):
			return { 'status': 'ERROR', 'message': 'Password Salah' }
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid]={ 'username': username, 'userdetail':self.users[username]}
		return { 'status': 'OK', 'tokenid': tokenid }
	def get_user(self,username):
		if (username not in self.users):
			return False
		return self.users[username]
	def send_message(self,sessionid,username_from,username_dest,message):
		if (sessionid not in self.sessions):
			return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
		s_fr = self.get_user(username_from)
		s_to = self.get_user(username_dest)
		
		if (s_fr==False or s_to==False):
			return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

		message = { 'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message }
		outqueue_sender = s_fr['outgoing']
		inqueue_receiver = s_to['incoming']
		try:	
			outqueue_sender[username_from].put(message)
		except KeyError:
			outqueue_sender[username_from]=Queue()
			outqueue_sender[username_from].put(message)
		try:
			inqueue_receiver[username_from].put(message)
		except KeyError:
			inqueue_receiver[username_from]=Queue()
			inqueue_receiver[username_from].put(message)
		return {'status': 'OK', 'message': 'Message Sent'}

	def get_inbox(self,username):
		s_fr = self.get_user(username)
		incoming = s_fr['incoming']
		msgs={}
		for users in incoming:
			msgs[users]=[]
			while not incoming[users].empty():
				msgs[users].append(s_fr['incoming'][users].get_nowait())
			
		return {'status': 'OK', 'messages': msgs}
	def send_file_realm(self, sessionid, realm_id, username_from, username_dest, filepath, encoded_file, data):
		if (sessionid not in self.sessions):
			return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
		if (realm_id not in self.realms):
			return {'status': 'ERROR', 'message': 'Realm Tidak Ditemukan'}
		s_fr = self.get_user(username_from)
		s_to = self.get_user(username_dest)
		if (s_fr==False or s_to==False):
			return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}
        
		filename = os.path.basename(filepath)
		message = {
			'msg_from': s_fr['nama'],
			'msg_to': s_to['nama'],
			'file_name': filename,
			'file_content': encoded_file
        }
		self.realms[realm_id].put(message)
        
		now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		folder_name = f"{now}_{username_from}_{username_dest}_{filename}"
		folder_path = join(dirname(realpath(__file__)), 'files/')
		os.makedirs(folder_path, exist_ok=True)
		folder_path = join(folder_path, folder_name)
		os.makedirs(folder_path, exist_ok=True)
		file_destination = os.path.join(folder_path, filename)
		if 'b' in encoded_file[0]:
			msg = encoded_file[2:-1]

			with open(file_destination, "wb") as fh:
				fh.write(base64.b64decode(msg))
		else:
			tail = encoded_file.split()
        
		j = data.split()
		j[0] = "recvfilerealm"
		j[1] = username_from
		data = ' '.join(j)
		data += "\r\n"
		self.realms[realm_id].sendstring(data)
		return {'status': 'OK', 'message': 'File Sent to Realm'}
    
	def recv_file_realm(self, sessionid, realm_id, username_from, username_dest, filepath, encoded_file, data):
		if (sessionid not in self.sessions):
			return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
		if (realm_id not in self.realms):
			return {'status': 'ERROR', 'message': 'Realm Tidak Ditemukan'}
		s_fr = self.get_user(username_from)
		s_to = self.get_user(username_dest)
		if (s_fr==False or s_to==False):
			return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}
        
		filename = os.path.basename(filepath)
		message = {
            'msg_from': s_fr['nama'],
            'msg_to': s_to['nama'],
            'file_name': filename,
            'file_content': encoded_file
        }
		self.realms[realm_id].put(message)
        
		now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		folder_name = f"{now}_{username_from}_{username_dest}_{filename}"
		folder_path = join(dirname(realpath(__file__)), 'files/')
		os.makedirs(folder_path, exist_ok=True)
		folder_path = join(folder_path, folder_name)
		os.makedirs(folder_path, exist_ok=True)
		file_destination = os.path.join(folder_path, filename)
		if 'b' in encoded_file[0]:
			msg = encoded_file[2:-1]

			with open(file_destination, "wb") as fh:
				fh.write(base64.b64decode(msg))
		else:
			tail = encoded_file.split()
        
		return {'status': 'OK', 'message': 'File Received to Realm'}

if __name__=="__main__":
	j = Chat()
	sesi = j.proses("auth messi surabaya")
	print(sesi)
	#sesi = j.autentikasi_user('messi','surabaya')
	#print sesi
	tokenid = sesi['tokenid']
	print(j.proses("send {} henderson hello gimana kabarnya son " . format(tokenid)))
	print(j.proses("send {} messi hello gimana kabarnya mess " . format(tokenid)))

	#print j.send_message(tokenid,'messi','henderson','hello son')
	#print j.send_message(tokenid,'henderson','messi','hello si')
	#print j.send_message(tokenid,'lineker','messi','hello si dari lineker')


	print("isi mailbox dari messi")
	print(j.get_inbox('messi'))
	print("isi mailbox dari henderson")
	print(j.get_inbox('henderson'))
















