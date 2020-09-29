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

import socket
from fsck import Fsck
from blockdevice import BlockDevice
from datatosend import dataToSend
from datatoreceive import dataToReceive

fsimg = "minixfs.img"

myDataToReceive = dataToReceive()

while True:
    try:
        mode = int(raw_input("Enter 0 to access a local FS and 1 to access a remote FS:\n"))
        if mode == 0:
            myBlockDevice = BlockDevice(fsimg, 1024, 20, mode, None)
            break
        elif mode == 1:
            # Creation of the socket
            mySocket = socket.socket()

            # Get informations about the server
            IP = raw_input("Remote IP address:\n")
            PORT = int(raw_input("Remote listening port number:\n"))

            # Prepare the message to send
            myDataToSend = dataToSend()
            myDataToSend.send(IP, PORT, 20, 1024, mySocket)
            myDataToReceive.receive(20, mySocket)

            # Creation of the Blockdevice object
            myBlockDevice = BlockDevice(None, None, None, mode, myDataToReceive.payload)
            break
    except ValueError:
        print "Ugh that's not an integer !"


print "---------------------------------------------"
print "                  SUPERBLOC"
print "---------------------------------------------\n"

print "Total number of inodes :", myBlockDevice.superBlock.inodeCount
print "Total number of blocks :", myBlockDevice.superBlock.blockCount
print "Size of the inodes bitmap :", myBlockDevice.superBlock.inodeBitmapSize
print "Size of the block zone bitmap :", myBlockDevice.superBlock.zoneBitmapSize
print "Index of the first data block :", myBlockDevice.superBlock.firstDataBlockOffset
print "Size of a data block in bytes :", myBlockDevice.superBlock.blockSize
print "Maximum size of a file in bytes :", myBlockDevice.superBlock.maxFileSize
print "Version :", myBlockDevice.superBlock.version
print "Mouting state of the volume :", myBlockDevice.superBlock.unmounted

print "\n---------------------------------------------"
print "                 STATS"
print "---------------------------------------------"

print "\nInode table size in block :", myBlockDevice.getInodesTableSize()
print "\nThe inode table goes from the block :", myBlockDevice.getInodesTableOffset(), "to the block :", myBlockDevice.getInodesTableSize()+myBlockDevice.getInodesTableOffset()-1

print "\nNumber of inodes with at least a name :", myBlockDevice.getFileCount()

print "\n---------------------------------------------"
print "                 VERIFICATIONS"
print "---------------------------------------------"

# We call the function to make sure that no file is above the max size
myFsck = Fsck()
myFsck.checkFilesSizes(myBlockDevice)
myFsck.checkUsedBlocks(myBlockDevice)
myFsck.checkAnonymousInodes(myBlockDevice)

print "Number of free blocks :", myBlockDevice.getFreeBlockCount(myBlockDevice.superBlock.blockCount, myBlockDevice.blockBitmap, \
                                                                myBlockDevice.getUsedBlockCount(myBlockDevice.superBlock.blockCount, myBlockDevice.blockBitmap))
