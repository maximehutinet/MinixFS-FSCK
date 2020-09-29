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

class Inode(object):
    def __init__(self):
        self.mode = None  # Type of file and permission
        self.uid = None  # UID of the file owner
        self.size = None  # File size in byte
        self.time = None  # Timestamp of the last modification
        self.gid = None  # ID of the group able to access the file
        self.nlinks = None  # Number of links pointing to this inode
        self.blocks1 = None  # Addresses of the file blocks
        self.blocks2 = None  
        self.blocks3 = None  
        self.blocks4 = None  
        self.blocks5 = None  
        self.blocks6 = None  
        self.blocks7 = None 
        self.indBlock = None  # Address of a block with the block file addresses
        self.doubleIndBlock = None 

    def createFromBytes(self, fsimg, offset, size):
        minixfs = open(fsimg)
        minixfs.seek(offset)
        raw_superblock = minixfs.read(size)
        self.mode, self.uid, self.size, self.time, self.gid, self.nlinks, self.blocks1, self.blocks2,\
        self.blocks3, self.blocks4, self.blocks5, self.blocks6, self.blocks7, self.indBlock, self.doubleIndBlock = struct.unpack("<HHIIBBHHHHHHHHH", raw_superblock[0:32])