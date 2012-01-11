# this lib used for checkout nat's type
# the process is:
# 
#
#
#
#

import socket
import struct

# defines of public STUN server address info
pub_stuns = [('stun.xten.com',3478),('stun.iptel.org',3478),('stun01.sipphone.com',3478),('stun.iptel.org',3478),('stun.ekiga.net',3478),('stun.softjoys.com',3478),('stun.voipbuster.com',3478),('stun.voxgratia.org',3478),('stunserver.org',3478)]

# defines of msg type
class Msg:
	MsgType = 0x0000
	MAPPED_ADDRESS = 0x0001
	RESPONSE_ADDRESS = 0x0002
	CHANGE_REQUEST = 0x0003
	SOURCE_ADDRESS = 0x0004
	CHANGED_ADDRESS = 0x0005
	USERNAME = 0x0006
	PASSWORD = 0x0007
	MESSAGE_INTEGRITY = 0x0008
	ERROR_CODE = 0x0009
	UNKNOWN_ATTRIBUTES = 0x000a
	REFLECTED_FROM = 0x000b

# define global socket
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

# tools to trace response msges
def traceMsgs(msgs):
	print '==================================='
	for key, value in msgs.items():
		if key == Msg.MAPPED_ADDRESS:
			print 'MAPPED_ADDRESS: fml:%x  port:%d ip:%d.%d.%d.%d'%struct.unpack('!HHBBBB', value)
	
		if key == Msg.SOURCE_ADDRESS:
			print 'SOURCE_ADDRESS: fml:%x  port:%d ip:%d.%d.%d.%d'%struct.unpack('!HHBBBB', value)
	
		if key == Msg.CHANGED_ADDRESS:
			print 'CHANGED_ADDRESS: fml:%x  port:%d ip:%d.%d.%d.%d'%struct.unpack('!HHBBBB', value)
	
	print '==================================='

# onResponse from stun server
def onResponse(data):
	'''on response from stun server, parse all messages into a map'''
	# store msgs
	msgs = {}
	
	subdata = data[0:4]
	stunmsgtype, msglength = struct.unpack('!HH', subdata)
	msgs[Msg.MsgType] = stunmsgtype
	print 'response:%x'%stunmsgtype

	i = 0
	msgdata = data[20:20+msglength]
	while i<msglength:
		subdata = msgdata[i:i+4]
		i += 4
		msgt, msgl = struct.unpack('!HH', subdata)

		if msgl>0:
			msg = msgdata[i:i+msgl]
		else:
			msg = None

		msgs[msgt] = msg
		i+= msgl

		print 'Msg:',msgt,"is:",repr(msg)
	
	#traceMsgs(msgs)

	return msgs


# test1: check udp is enable
def test1_udp_enable(pub_stuns, sock):
	'''send binding requestion to STUN server. if no response received, then UDP is unsupported. else UDP is enabled. return recved data value and responsed address'''
	print 'test1_udp_enable()'
	
	# packing binding request
	sendData = struct.pack('!HH16s',0x0001, 0, '1234567890123456')
	print 'sendData:'+repr(sendData)

	# test udp sending to each server address
	for stun_addr in pub_stuns:

		data = None
		curaddr = None

		# try 5 times
		for i in range(0,5):
			try:
				print 'test:', stun_addr
				sock.sendto(sendData, stun_addr)
				data,(addr,port) = sock.recvfrom(1024)
				curaddr = (addr, port)
				print 'recv:'+repr(data)
				break

			except socket.error as msg:
				print msg
		
		if data != None and curaddr != None:
			break
	
	# parse response messages
	# msgs = onResponse(data)
	
	return data, curaddr


# test2: check is Full Clone NAT
def test2_fullclone(curaddr, sock, msgs):
	'''send binding requestion to STUN server, request server response from different address and port. if resp can be reached,it's Full Clone NAT. if can't, it's Symmetric, Strict or Port Strict NAT.'''
	print 'test2_fullclone'

	# package change request binding
	sendData = struct.pack('!HH16s', 0x0001, 20, '1234567890123456') + struct.pack('!HH', Msg.RESPONSE_ADDRESS, 8) + msgs[Msg.MAPPED_ADDRESS] + struct.pack('!HHBBBB', Msg.CHANGE_REQUEST, 4, 0,0,0,6) 	
	print repr(sendData)

	# repeat 5 times
	for i in range(0,5):
		try:
			data = None
			caddr = None
			sock.sendto(sendData, curaddr)
			data, (addr, port) = sock.recvfrom(1024)
			caddr = (addr, port)
			print 'recv:'+repr(data)
			break;
		
		except socket.error as msg:
			print msg

	return data, caddr



# test3: check is Symmetric NAT
def test3_symmetric(curaddr, sock, msgs):
	'''send binding requestion to two different address. if response address is not same, them it's Symmetric NAT.'''
	print 'test3_symmetric()'
	sendData = struct.pack('!HH16s', 0x0001, 0, '1234567890123456')
	print 'sendData:'+repr(sendData)

	if Msg.CHANGED_ADDRESS in msgs:
		temp, sendPort, a1,a2,a3,a4 = struct.unpack('!HHBBBB', msgs[Msg.CHANGED_ADDRESS])
		sendAddr = '%d.%d.%d.%d'%(a1,a2,a3,a4)
	else: 
		print 'Error: msgs has no key:CHANGED_ADDRESS'
		return None

	# try 5 times
	for i in range(0,5):
		try:
			print 'test:', sendAddr, sendPort
			sock.sendto(sendData, (sendAddr, sendPort))
			data,(addr,port) = sock.recvfrom(1024)
			print 'recv:'+repr(data)
			tmsgs = onResponse(data)
			
			if tmsgs[Msg.MsgType] != 0x0101:
				print 'There is an error in response message'
				return None

			fm1, port1, ip1 = struct.unpack('!HHL', msgs[Msg.MAPPED_ADDRESS])
			fm2, port2, ip2 = struct.unpack('!HHL', tmsgs[Msg.MAPPED_ADDRESS])
			print 'fm1:',fm1,'port1:',port1, 'ip1:',socket.inet_ntoa(struct.pack('!L',ip1))
			print 'fm2:',fm2,'port2:',port2, 'ip2:',socket.inet_ntoa(struct.pack('!L',ip2))

			if port1!=port2 or ip1 != ip2:
				return tmsgs
			else:
				return None

		except socket.error as msg:
			print msg
	
	return None


	

# test4: check is Strict NAT
def test4_restricted(curaddr, sock, msgs):
	'''send binding requestion to STUN server, let it response from the differnt address but the same port. if response can reached,it's a Strict NAT'''
	print 'test4_retricted()'

	# package change request binding
	sendData = struct.pack('!HH16s', 0x0001, 20, '1234567890123456') + struct.pack('!HH', Msg.RESPONSE_ADDRESS, 8) + msgs[Msg.MAPPED_ADDRESS] + struct.pack('!HHBBBB', Msg.CHANGE_REQUEST, 4, 0,0,0,2) 	
	print repr(sendData)

	# repeat 5 times
	for i in range(0,5):
		try:
			data = None
			caddr = None
			sock.sendto(sendData, curaddr)
			data, (addr, port) = sock.recvfrom(1024)
			caddr = (addr, port)
			print 'recv:'+repr(data)
			break;
		
		except socket.error as msg:
			print msg

	return data, caddr



# main function
def main():

	# test 1
	data, curaddr = test1_udp_enable(pub_stuns, sock)
	if data == None:
		print '************** UDP is unsupported! ***************'
		exit(1)
	else:
		print '************** UDP is supported. *****************'

	# parse response
	msgs = onResponse(data)
	traceMsgs(msgs)

	# test 3
	tmsgs = test3_symmetric(curaddr, sock, msgs)
	if tmsgs != None:
		print '************** Symmetric NAT *********************'
		exit(3)
	else:
		print '************* NOT Symmetric NAT*******************'

	# test 2
	data, caddr = test2_fullclone(curaddr, sock, msgs)
	if data != None:
		print '************** Full Clone NAT ********************'
		exit(2)
	else:
		print '************** NOT Full Clone ********************'

	# test 4
	data, caddr = test4_restricted(curaddr, sock, msgs)
	if data != None:
		print '************** Restricted NAT ********************'
		exit(4)
	else:
		print '************** Port Restricted NAT ***************'
		exit(5)

if __name__=='__main__':
	main()

