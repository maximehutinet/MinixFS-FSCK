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

class InodesBitmap(object):
    def __init__(self):
        self.bits = []

    # Read the bitmap of the inodes
    def createFromBytes(self, fsimg, offset, size, blockcount):
        minixfs = open(fsimg) 
        minixfs.seek(offset) 
        raw_bitmap = minixfs.read(size)
        i = 0
        bit = 0

        for i in range(blockcount):
            bit = struct.unpack("?", raw_bitmap[i])
            self.bits.append(bit[0])


