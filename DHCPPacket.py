"""
使用方法 :
P = DHCPPacket.DHCPPacket()

給封包值 :

P.Data[DHCPPacket.OPCODE] = 100 修改封包 OPCODE

取封包值 :

Opcode = P.Data[DHCPPacket.OPCODE]

----------------------------------------------------------------------------

Options 使用方法 :

R = P.getOptRow(DHCPPacket.RequireIPAddress) 取得一個 DHCP Options 欄位格式 
R[2] = [123,123,123,123] 設定欄位資料，所有的資料皆須用 list 包起來
值為字串
R[2] = '123'
值為單值
R[2] = [1]
P.Data[DHCPPacket.OPT].append(R)  將Option放進封包裡

----------------------------------------------------------------------------

重要函式 :

pack() : 將封包編碼
unpack(binary string) : 將所傳入的binary資料解碼到封包
Flag(bool) : 設定封包 Flag 欄位

"""

import struct
import random

DHCPMAXSIZE = 548

OPCODE = "OPcode"
HTYPE = "HardwareType"
HLEN = "HardwareAddressLength"
HOPS = "HOPS"
TRANSID = "TRANSCATION ID"
SECONDS = "SECONDS"
FLAGS = "FLAGS"
CIADDR = "Client IP Address"
YIADDR = "Your IP Address"
SIADDR = "Server IP Address"
GIADDR = "Relay IP Address"
CHADDR = "Client Ethernet Address"
SNAME = "Server Host Name"
FILE = "file"
OPT = "Options"
	
# Options Code
RequireIPAddress = (50, 4, [0 for i in range(4)], "!BBBBBB") # IPv4 Address
IPAddressLeaseTime = (51, 4, [0], "!BBI") # int
FileORSnameFields = (52, 1, [0], "!BBB")
DHCPMessageType = (53, 1, [0], "!BBB")
ServerIdentifier = (54, 4, [0 for i in range(4)], "!BBBBBB") # IPv4 Address
ParameterRequestList = (55, "variable", [], "I") # int code 
Message = (56, "variable", [], "B") # text, by server
ClientIdentifier = (56, "variable", [], "B") # text, by client
MaximumDHCPMessageSize  = (57, 2, [0], "!BBH") # max value is 576
RenewalTimeValueT1 = (58, 4, [], "!BBI") # int
RebindingTimeValueT2 = (59, 4, [], "!BBI") # int 
VendorClassIdentifier = (60, "variable", [], "B") # text

class DHCPPacket:

	DHCPMAXSIZE = 548

	OPCODE = "OPcode" 
	HTYPE = "HardwareType"
	HLEN = "HardwareAddressLength"
	HOPS = "HOPS"
	TRANSID = "TRANSCATION ID"
	SECONDS = "SECONDS"
	FLAGS = "FLAGS"
	CIADDR = "Client IP Address"
	YIADDR = "Your IP Address"
	SIADDR = "Server IP Address"
	GIADDR = "Relay IP Address"
	CHADDR = "Client Ethernet Address"
	SNAME = "Server Host Name"
	FILE = "file"
	OPT = "Options"
	
	# Options Code
	RequireIPAddress = (50, 4, [0 for i in range(4)], "!BBBBBB") # IPv4 Address
	IPAddressLeaseTime = (51, 4, [0], "!BBI") # int
	FileORSnameFields = (52, 1, [0], "!BBB") # unsigned char
	DHCPMessageType = (53, 1, [0], "!BBB") # unsigned char
	ServerIdentifier = (54, 4, [0 for i in range(4)], "!BBBBBB") # IPv4 Address
	ParameterRequestList = (55, "variable", [], "I") # int code 
	Message = (56, "variable", [], "B") # text, by server
	ClientIdentifier = (56, "variable", [], "B") # text, by client
	MaximumDHCPMessageSize  = (57, 2, [0], "!BBH") # max value is 576, unsigned short
	RenewalTimeValueT1 = (58, 4, [], "!BBI") # int
	RebindingTimeValueT2 = (59, 4, [], "!BBI") # int 
	VendorClassIdentifier = (60, "variable", [], "B") # text
	
	__Options__ = (
		RequireIPAddress, 
		IPAddressLeaseTime,
		FileORSnameFields,
		DHCPMessageType,
		ServerIdentifier,
		ParameterRequestList,
		Message,
		ClientIdentifier,
		MaximumDHCPMessageSize,
		RenewalTimeValueT1,
		RebindingTimeValueT2,
		VendorClassIdentifier
	)
	
	
	
	offset = {
		"OPcode" : (0,1), # 8 bits/1
		"HardwareType" : (1,2), # 8 bits/1
		"HardwareAddressLength" : (2,3), # 6 bytes MAC Address, 8 bits/1
		"HOPS" : (3,4), # 8 bits/1
		"TRANSCATION ID" : (4, 8), # random number (int), 32 bits/4
		"SECONDS" : (8, 10), # 16 bits/2
		"FLAGS" : (10, 12), # bit 0 control broadcast, other is 0 (reserve), 16 bits/2
		"Client IP Address" : (12, 16), # 32 bits/4
		"Your IP Address" : (16, 20), # 32 bits/4
		"Server IP Address" : (20, 24), # 32 bits/4
		"Relay IP Address" : (24, 28), # 32 bits/4
		"Client Ethernet Address" : (28, 44) , # 16 bytes
		"Server Host Name" : (44, 108), # 64 bytes end of 0x00 code
		"file" : (108,236), # 128 bytes
		"Options" : (240,552) # 312 bytes
	}
	
	format = {
		OPCODE : '!B',
		HTYPE : '!B',
		HLEN : '!B',
		HOPS : '!B',
		TRANSID : '!I',
		SECONDS : '!H',
		FLAGS : '!H',
		CIADDR : '!BBBB',
		YIADDR : '!BBBB',
		SIADDR : '!BBBB',
		GIADDR : '!BBBB',
		CHADDR : '!' + 'B'*16,
		SNAME : 'B',
		FILE : 'B'
	}
	
	def __init__(self) :
		self.Packet = {
			"OPcode" : 0, # 8 bits/1
			"HardwareType" : 0, # 8 bits/1
			"HardwareAddressLength" : 0, # 6 bytes MAC Address, 8 bits/1
			"HOPS" : 0, # 8 bits/1
			"TRANSCATION ID" : 0, # random number (int), 32 bits/4
			"SECONDS" : 0, # 16 bits/2
			"FLAGS" : 0, # bit 0 control broadcast, other is 0 (reserve), 16 bits/2
			"Client IP Address" : [0 for i in range(4)], # 32 bits/4 IPv4
			"Your IP Address" : [0 for i in range(4)], # 32 bits/4 IPv4
			"Server IP Address" : [0 for i in range(4)], # 32 bits/4 IPv4
			"Relay IP Address" : [0 for i in range(4)], # 32 bits/4 IPv4
			"Client Ethernet Address" : [0 for i in range(16)], # 16 bytes, MAC Address
			"Server Host Name" : "\00"*64, # 64 bytes end of 0x00 code
			"file" : "\00"*128, # 128 bytes, boot file name
			"Options" : [] # 312 bytes
		}
		
		self.Data = self.Packet
		self.data = self.Packet
	
	def Flags(self, isBroadcast) :
		if isBroadcast :
			self.Packet[self.FLAGS] = 32768
		return self.Packet[self.FLAGS]
		
	def SnameP(self) :
		L = list(self.Packet[self.SNAME])
		L = [ord(E) for E in L]
		binstr = struct.pack('!' + self.format[self.SNAME]*len(self.Packet[self.SNAME]), *L)
		rm = 64 - len(binstr)
		binstr += b'\x00'*rm
		return binstr
	
	def FileP(self) :
		L = list(self.Packet[self.FILE])
		L = [ord(E) for E in L]
		binstr = struct.pack('!' + self.format[self.FILE]*len(self.Packet[self.FILE]), *L)
		rm = 128 - len(binstr)
		binstr += b'\x00'*rm
		return binstr
		
	def OptionsP(self) :
		row = ()
		binstr = b''
		
		for E in self.Packet[self.OPT] :
			if E[0] == self.RequireIPAddress[0] :
				row = self.RequireIPAddress
			elif E[0] == self.IPAddressLeaseTime[0] :
				row = self.IPAddressLeaseTime
			elif E[0] == self.FileORSnameFields[0] :
				row = self.FileORSnameFields
			elif E[0] == self.DHCPMessageType[0] :
				row = self.DHCPMessageType
			elif E[0] == self.ServerIdentifier[0] :
				row = self.ServerIdentifier
			elif E[0] == self.ParameterRequestList[0] :
				row = self.ParameterRequestList
			elif E[0] == self.Message[0] :
				row = self.Message
			elif E[0] == self.ClientIdentifier[0] :
				row = self.ClientIdentifier
			elif E[0] == self.MaximumDHCPMessageSize[0] :
				row = self.MaximumDHCPMessageSize
			elif E[0] == self.RenewalTimeValueT1[0] :
				row = self.RenewalTimeValueT1
			elif E[0] == self.RebindingTimeValueT2[0] :
				row = self.RebindingTimeValueT2
			elif E[0] == self.VendorClassIdentifier[0] :
				row = self.VendorClassIdentifier
			else :
				print('Error Option code', E[0])
			
			if E[0] in [self.Message[0], self.ClientIdentifier[0], self.VendorClassIdentifier[0], self.ParameterRequestList[0]]:
				if str(type(E[2][0])) == "<type 'str'>" or str(type(E[2][0])) == "<class 'str'>":
					L = [ord(C) for C in list(E[2][0])]
					if len(E) < 4 :
						row = (E[0], len(L), L, "!BB" + "B"*len(L))
					else :
						row = (E[0], len(L), L, "!BB" + E[3]*len(L))
				else :
					if E[0] == self.ParameterRequestList[0] :
						intFix = 4
						if len(E) < 4 :
							row = (E[0], len(E[2])*intFix, list(E[2]), "!BB" + "I"*len(E[2]))
						else :
							row = (E[0], len(E[2])*intFix, list(E[2]), "!BB" + E[3]*len(E[2]))
					else :
						row = (E[0], len(E[2]), list(E[2]), "!BB" + E[3]*len(E[2]))
			else :
				row = (E[0], E[1], E[2], row[3])
			
			# print("final Opt row ", row)		
			
			binstr += struct.pack(row[3], row[0], row[1], *row[2])
			
		return binstr
	
	def getDHCPMessageType(self) :
		for O in self.Packet[self.OPT] :
			if O[0] == self.DHCPMessageType[0] :
				return O[2][0]
		return -1
	
	def getOptRow(self, OptRow) :
		return [E for E in OptRow]
		
	def pack(self) :
		self.Data[self.TRANSID] = random.randint(0, 65536)
		packet = b''
		packet += struct.pack(self.format[self.OPCODE], self.Packet[self.OPCODE])
		packet += struct.pack(self.format[self.HTYPE], self.Packet[self.HTYPE])
		packet += struct.pack(self.format[self.HLEN], self.Packet[self.HLEN])
		packet += struct.pack(self.format[self.HOPS], self.Packet[self.HOPS])
		packet += struct.pack(self.format[self.TRANSID], self.Packet[self.TRANSID])
		packet += struct.pack(self.format[self.SECONDS], self.Packet[self.SECONDS])
		packet += struct.pack(self.format[self.FLAGS], self.Packet[self.FLAGS])
		packet += struct.pack(self.format[self.CIADDR], *self.Packet[self.CIADDR])
		packet += struct.pack(self.format[self.YIADDR], *self.Packet[self.YIADDR])
		packet += struct.pack(self.format[self.SIADDR], *self.Packet[self.SIADDR])
		packet += struct.pack(self.format[self.GIADDR], *self.Packet[self.GIADDR])
		packet += struct.pack(self.format[self.CHADDR], *list(self.Packet[self.CHADDR]))
		packet += self.SnameP()
		packet += self.FileP()
		packet += b'\x63\x82\x53\x63'
		packet += self.OptionsP()
		packet += b'\xff'
		# packet += b'\x00'*(self.DHCPMAXSIZE - len(packet))
		return packet
		
	def unpackVarLen(self, binsrc, start, Offset, Type, typeFix = 1) :
		newStart = start + Offset + 1
		size = int(binsrc[newStart])
		nop = size + 1
		newStart = newStart + 1
		content = binsrc[newStart:newStart + size]
		row = self.getOptRow(Type)
		row = row[0:3]
		format = Type[3]
		size = int(size/typeFix)
		format = "!BB" + format*size
		return (row, size, content, format, nop)
		
	def unpackFixLen(self, binsrc, start, Offset, Type) :
		newStart = start + Offset + 1
		size = int(binsrc[newStart])
		nop = size + 1
		newStart = newStart + 1
		content = binsrc[newStart:newStart + size]
		row = self.getOptRow(Type)
		row = row[0:3]
		format = Type[3]
		return (row, size, content, format, nop)
		
	def unpack(self, binstr) :
		MaxPacketLen = len(binstr)
		
		try :
			self.Data[self.OPT] = []
			data = ''
			start, end = self.offset[self.OPCODE]
			data = struct.unpack(self.format[self.OPCODE], binstr[start:end])
			self.Packet[self.OPCODE] = data[0]
		
			start, end = self.offset[self.HTYPE]
			data = struct.unpack(self.format[self.HTYPE], binstr[start:end])
			self.Packet[self.HTYPE] = data[0]
		
			start, end = self.offset[self.HLEN]
			data = struct.unpack(self.format[self.HLEN], binstr[start:end])
			self.Packet[self.HLEN] = data[0]
		
			start, end = self.offset[self.HOPS]
			data = struct.unpack(self.format[self.HOPS], binstr[start:end])
			self.Packet[self.HOPS] = data[0]
		
			start, end = self.offset[self.TRANSID]
			data = struct.unpack(self.format[self.TRANSID], binstr[start:end])
			self.Packet[self.TRANSID] = data[0]
		
			start, end = self.offset[self.SECONDS]
			data = struct.unpack(self.format[self.SECONDS], binstr[start:end])
			self.Packet[self.SECONDS] = data[0]
		
			start, end = self.offset[self.FLAGS]
			data = struct.unpack(self.format[self.FLAGS], binstr[start:end])
			self.Packet[self.FLAGS] = data[0]
		
			start, end = self.offset[self.CIADDR]
			data = struct.unpack(self.format[self.CIADDR], binstr[start:end])
			self.Packet[self.CIADDR] = [E for E in data]
		
			start, end = self.offset[self.YIADDR]
			data = struct.unpack(self.format[self.YIADDR], binstr[start:end])
			self.Packet[self.YIADDR] = [E for E in data]
		
			start, end = self.offset[self.SIADDR]
			data = struct.unpack(self.format[self.SIADDR], binstr[start:end])
			self.Packet[self.SIADDR] = [E for E in data]
		
			start, end = self.offset[self.GIADDR]
			data = struct.unpack(self.format[self.GIADDR], binstr[start:end])
			self.Packet[self.GIADDR] = [E for E in data]
		
			start, end = self.offset[self.CHADDR]
			data = struct.unpack(self.format[self.CHADDR], binstr[start:end])
			self.Packet[self.CHADDR] = [E for E in data]
		
			start, end = self.offset[self.SNAME]
			data = struct.unpack('!' + self.format[self.SNAME]*len(binstr[start:end]), binstr[start:end])
			self.Packet[self.SNAME] = ''.join([chr(E) for E in data if not int(E) == 0])
		
			start, end = self.offset[self.FILE]
			data = struct.unpack('!' + self.format[self.FILE]*len(binstr[start:end]), binstr[start:end])
			self.Packet[self.FILE] = ''.join([chr(E) for E in data if not int(E) == 0])
		except struct.error :
			print('Incorrect DHCP packet format !')
			return False
			pass
		
		start, maxEnd = self.offset[self.OPT] 
		
		Offset = 0
		nop = 0
		size = 0
		content = []
		row = []
		format = []
		
		try :
		
			for E in binstr[start:MaxPacketLen] : 
				if nop > 0 :
					Offset = Offset + 1
					nop = nop - 1
					continue
				if int(E) == self.RequireIPAddress[0] :
					row,size,content,format,nop = self.unpackFixLen(binstr, start, Offset, self.RequireIPAddress)
				elif int(E) == self.IPAddressLeaseTime[0] :
					row,size,content,format,nop = self.unpackFixLen(binstr, start, Offset, self.IPAddressLeaseTime)
				elif int(E) == self.FileORSnameFields[0] :
					row,size,content,format,nop = self.unpackFixLen(binstr, start, Offset, self.FileORSnameFields)
				elif int(E) == self.DHCPMessageType[0] :
					row,size,content,format,nop = self.unpackFixLen(binstr, start, Offset, self.DHCPMessageType)
				elif int(E) == self.ServerIdentifier[0] :
					row,size,content,format,nop = self.unpackFixLen(binstr, start, Offset, self.ServerIdentifier)
				elif int(E) == self.ParameterRequestList[0] : # integer special
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, self.ParameterRequestList, 4)
				elif int(E) == self.Message[0] :
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, self.Message)
				elif int(E) == self.ClientIdentifier[0] :
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, self.ClientIdentifier)
				elif int(E) == self.MaximumDHCPMessageSize[0] :
					row,size,content,format,nop = self.unpackFixLen(binstr, start, Offset, self.MaximumDHCPMessageSize)
				elif int(E) == self.RenewalTimeValueT1[0] :
					row,size,content,format,nop = self.unpackFixLen(binstr, start, Offset, self.RenewalTimeValueT1)
				elif int(E) == self.RebindingTimeValueT2[0] :
					row,size,content,format,nop = self.unpackFixLen(binstr, start, Offset, self.RebindingTimeValueT2)
				elif int(E) == self.VendorClassIdentifier[0] :
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, self.VendorClassIdentifier)
				elif int(E) == 255 :
					return True
				else :
					print(E, 'is Error code, stop unpack')
					return False
				
				format = '!' + format[3:len(format)] 
				
				row[0] = E
				row[1] = size
				if E in [self.Message[0], self.ClientIdentifier[0], self.VendorClassIdentifier[0]] :
					row[2] = [''.join([chr(C) for C in list(struct.unpack(format, content))])]
				else :
					row[2] = list(struct.unpack(format, content))
			
				Offset = Offset + 1
				self.Data[self.OPT].append(row)
		except struct.error :
			print('DHCP Option format error')
			return False
			pass
		return True