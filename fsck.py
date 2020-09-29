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

from bitstring import ConstBitStream

class Fsck(object):

    # Init
    def __init__(self):
        self.filesizeStatus = None

    # Make sure there are no oversized file
    def checkFilesSizes(self, blockDevice):
        biggerSize = 0
        for i in range(blockDevice.superBlock.inodeCount):
            if blockDevice.inodes[i].size > blockDevice.superBlock.maxFileSize:
                biggerSize += 1
        if biggerSize == 0:
            print("\nNo file above the max size")
        else:
            print("\nThere are %d file with a size above the max size") % biggerSize

    # Check that the number of blocks used matches the number of bits flaged as used
    def checkUsedBlocks(self, blockDevice):
        blocks = 0
        for i in range(blockDevice.superBlock.inodeCount):
            blocks += blockDevice.inodes[i].size/blockDevice.superBlock.blockSize
        if blocks == blockDevice.getUsedBlockCount(blockDevice.superBlock.blockCount, blockDevice.blockBitmap):
            print("\nNumber of block used : OK")
        else:
            print("\nNumber of block used doesn't match the bitmap\n------\n- Reel: %d \n- Bitmap: %d\n------") % (blocks, blockDevice.getUsedBlockCount(blockDevice.superBlock.blockCount, blockDevice.blockBitmap))

    # Check that there are no anonymous inodes
    def checkAnonymousInodes(self, blockDevice):
        anonymous = 0
        for i in range(blockDevice.superBlock.inodeCount):
            if blockDevice.inodes[i].nlinks < 1:
                anonymous += 1
        if anonymous > 0:
            print("\nThere are %d anonymous inode(s)!") % anonymous

    # Check the validity of a repository
    def checkValideDir(self, inodeTotalNumber, fsimg, offset, size):
        validDir = 0
        minixfs = open(fsimg)
        minixfs.seek(offset)
        raw_table = minixfs.read(size)

        for i in range(inodeTotalNumber):
            raw_table.seek(i)
            s = ConstBitStream(raw_table.read(1))
            type = s.readlist('uintle:4')
            if type == 4:  
                validDir += 1
        return validDir

    # Count the number of inodes with a name
    def getFileCount(inodeTotalNumber, list):
        fileCount = 0
        for i in range(inodeTotalNumber):
            if list[i].nlinks > 0:
                fileCount += 1
        return fileCount