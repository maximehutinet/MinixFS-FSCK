#!/usr/local/bin/python
# @author Maxime Hutinet & Livio Nagy

#   Fsck : This projet is a simplified version of a File System Check for the MinixFS file system.
#   Copyright (C) 2018  Maxime Hutinet & Livio Nagy

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import struct
import socket


class dataToReceive(object):
    def __init__(self):
        self.magicHeaderSeparator = None
        self.error = None
        self.handle = None
        self.payload = None

    def receive(self, buffer, mySocket):
        sock = mySocket
        data = sock.recv(12+buffer)
        self.magicHeaderSeparator, self.error, self.handle = struct.unpack(">III",data[0:12])
        self.payload = data[12:12+buffer]
        print "Length payload : ",len(self.payload)




