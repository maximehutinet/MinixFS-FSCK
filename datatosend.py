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
import randompy

CMD_READ = 0
MAGIC_REQUEST = 0x76767676

class dataToSend(object):
    def __init__(self):
        self.magicHeaderSeparator = None
        self.type = None
        self.handle = None
        self.offset = None
        self.length = None
        self.ip = None
        self.port = None
        self.message = None
        self.sizeOfTheMessage = None

    def send(self, ip, port, length, offset, mySocket):
        handle = randompy.integer(1, 2**32)
        self.handle = handle
        print type(handle)

        self.magicHeaderSeparator = MAGIC_REQUEST
        self.offset = offset
        print type(offset)
        self.length = length
        self.type = CMD_READ

        message = struct.pack(">IILII", self.magicHeaderSeparator, self.type, self.handle, self.offset, self.length)
        self.sizeOfTheMessage = len(message)
        sock = mySocket
        sock.connect((ip, port))
        sock.send(message)


