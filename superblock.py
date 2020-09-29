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


class SuperBlock(object):
    def __init__(self):
        self.inodeCount = None  # Total number of inodes
        self.blockCount = None  # Number of blocks, block 0 included
        self.inodeBitmapSize = None # Inode bitmap size
        self.zoneBitmapSize = None # Size of the block bitmap
        self.firstDataBlockOffset = None # Index of the first data block
        self.blockSize = None # Size of a block in byte
        self.maxFileSize = None # Max size of a file in bytes
        self.version = None # Version Minix
        self.unmounted = None # Indicate if the volume has properly been unmounted

    def createFromBytes(self, fsimg, offset, size, mode, data):
        if mode == 0:
            minixfs = open(fsimg)
            minixfs.seek(offset)
            raw_superblock = minixfs.read(size)
            self.inodeCount, self.blockCount, self.inodeBitmapSize, self.zoneBitmapSize, self.firstDataBlockOffset, self.blockSize,\
            self.maxFileSize, self.version, self.unmounted = struct.unpack("<HHHHHHIHH", raw_superblock[0:20])
            self.blockSize = 1024 * 2 ** self.blockSize  
        elif mode == 1:
            self.inodeCount, self.blockCount, self.inodeBitmapSize, self.zoneBitmapSize, self.firstDataBlockOffset, self.blockSize, \
            self.maxFileSize, self.version, self.unmounted = struct.unpack("<HHHHHHIHH", data[0:20])
            self.blockSize = 1024 * 2 ** self.blockSize
            print self.inodeCount
            print self.blockCount
        else:
            print "Cannot read the data"

