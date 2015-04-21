import DHCPPacket
import argparse
import struct
from socket import *
import random

ClientInitialState = 'Client Initial'
ClientDiscoverState = 'Client Send Discover'
ClientRequestState = 'Client Send Request'
ClientGetOfferState = 'Client Get Offer'
ClientGetACKState = 'Client Get ACK'

class DHCPClient :
        def __init__(self) :
               self.cs = socket(AF_INET, SOCK_DGRAM)
               self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
               self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
               self.cs.bind(('192.168.56.1', 67))
               self.serverIPAddress = 'NONE'
               self.state = ClientInitialState
               while True :
                        print('Current State : ', self.state)
                        if self.state == ClientInitialState :
                                #self.test()
                                self.discover()
                                self.state = ClientDiscoverState
                        elif self.state == ClientDiscoverState :
                                self.cs.settimeout(1)
                                try :
                                        self.cs.settimeout(3)
                                        data, address = self.cs.recvfrom(1024) # wait for offer
                                        self.cs.settimeout(None)
                                        P = DHCPPacket.DHCPPacket()
                                        if P.unpack(data) :
                                                if P.getDHCPMessageType() == 2 :
                                                        self.serverIPAddress = address
                                                        self.state = ClientGetOfferState
                                                else :
                                                        self.state = ClientDiscoverState
                                except timeout :
                                        self.state = ClientDiscoverState
                                        self.discover()
                        elif self.state == ClientGetOfferState :
                                self.request()
                                self.state = ClientRequestState
                        elif self.state == ClientRequestState :
                                try :
                                        self.cs.settimeout(1)
                                        data, address = self.cs.recvfrom(1024) # wait for ACK
                                        self.cs.settimeout(None)
                                        P = DHCPPacket.DHCPPacket()
                                        if P.unpack(data) :
                                                if P.getDHCPMessageType() == 5 :
                                                        self.state = ClientGetACKState
                                                else :
                                                        self.state = ClientRequestState
                                except timeout :
                                        self.state = ClientRequestState
                                        self.request()
                        elif self.state == ClientGetACKState :
                                print('All work is done, Do you want to try again ?(Y, y will be continue)')
                                Q = input()
                                if Q in ['Y', 'y'] :
                                        self.state = ClientInitialState
                                else :
                                        self.cs.close()
                                        print('Close client, Bye')
                                        break
                        else :
                                print('Error State')
        def discover(self) :
                P = DHCPPacket.DHCPPacket()
                P.Data[DHCPPacket.OPCODE] = 1
                P.Data[DHCPPacket.HTYPE] = 1
                P.Data[DHCPPacket.HLEN] = 6
                optRow = P.getOptRow(DHCPPacket.DHCPMessageType)
                optRow[2] = [1]
                P.Data[DHCPPacket.OPT].append(optRow)
                self.cs.sendto(P.pack(), ('255.255.255.255', 68))
        def request(self) :
                P = DHCPPacket.DHCPPacket()
                P.Data[DHCPPacket.OPCODE] = 1
                P.Data[DHCPPacket.HTYPE] = 1
                P.Data[DHCPPacket.HLEN] = 6
                optRow = P.getOptRow(DHCPPacket.DHCPMessageType)
                optRow[2] = [3]
                P.Data[DHCPPacket.OPT].append(optRow)
                if self.serverIPAddress != 'NONE' :
                        self.cs.sendto(P.pack(), self.serverIPAddress)
        def test(self) :
                for i in range(1, 9) :
                        P = DHCPPacket.DHCPPacket()
                        P.Data[DHCPPacket.OPCODE] = 1
                        P.Data[DHCPPacket.HTYPE] = 1
                        P.Data[DHCPPacket.HLEN] = 6
                        optRow = P.getOptRow(DHCPPacket.DHCPMessageType)
                        optRow[2] = [i]
                        P.Data[DHCPPacket.OPT].append(optRow)
                        self.cs.sendto(P.pack(), ('255.255.255.255', 68))
        
if __name__ == "__main__" :
    Cli = DHCPClient()
    print('end')
    pass
