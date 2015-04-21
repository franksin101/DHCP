import DHCPPacket
from socket import *
import sys
import argparse
import struct

ServerInitialState = 'Server Initial State'
ServerWaitState = 'Server Wait State'
ServerGetDiscoverState = 'Server Get Discover State'
ServerGetRequestState = 'Server Get Request State'

class DHCPServer :
	def __init__(self, IPAddress = 'localhost', Port = 68) :
		print(ServerInitialState)
		self.clientIPAddress = 'NONE'
		self.cs = socket(AF_INET, SOCK_DGRAM)
		self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.cs.bind((IPAddress, Port)) 
		while True :
			print(ServerWaitState)
			data, address = self.cs.recvfrom(1024)
			self.clientIPAddress = address
			print('Get packet from : ', self.clientIPAddress)
			P = DHCPPacket.DHCPPacket()
			if P.unpack(data) :
				if P.getDHCPMessageType() == 1 :
					print(ServerGetDiscoverState)
					self.offer()
					print('Send DHCP Offer to ', address)
				elif P.getDHCPMessageType() == 3 :
					print(ServerGetRequestState)
					self.ack()
					print('Send DHCP ACK to ', address)
				else :
					print('Error Type : ', P.getDHCPMessageType())
	def offer(self) :
		P = DHCPPacket.DHCPPacket()
		P.Data[DHCPPacket.OPCODE] = 1
		P.Data[DHCPPacket.HTYPE] = 1
		P.Data[DHCPPacket.HLEN] = 6
		optRow = P.getOptRow(DHCPPacket.DHCPMessageType)
		optRow[2] = [2]
		P.Data[DHCPPacket.OPT].append(optRow)
		self.cs.sendto(P.pack(), self.clientIPAddress)
	def ack(self) :
		P = DHCPPacket.DHCPPacket()
		P.Data[DHCPPacket.OPCODE] = 1
		P.Data[DHCPPacket.HTYPE] = 1
		P.Data[DHCPPacket.HLEN] = 6
		optRow = P.getOptRow(DHCPPacket.DHCPMessageType)
		optRow[2] = [5]
		P.Data[DHCPPacket.OPT].append(optRow)
		self.cs.sendto(P.pack(), self.clientIPAddress)

if __name__ == "__main__" :
	Ser = DHCPServer('192.168.56.1', 68)
	pass
	
