from superblock import SuperBlock
from inode import Inode
from datatoreceive import dataToReceive
from inodesbitmap import InodesBitmap
from blocksbitmap import BlocksBitmap


class BlockDevice(object):
    def __init__(self, fsimg, superBlockOffset, superBlockSize, mode, data):
        self.superBlock = self.createSuperBlock(fsimg, superBlockOffset, superBlockSize, mode, data)
        self.inodes = self.createInodeList(self.superBlock.inodeCount, fsimg, self.superBlock.blockSize*(2+self.superBlock.inodeBitmapSize+self.superBlock.zoneBitmapSize), 32)
        self.inodeBitmap = self.createInodeBitmap(fsimg)
        self.blockBitmap = self.createBlockBitmap(fsimg)  
        self.blocks = []

    def createSuperBlock(self, fsimg, superBlockOffset, superBlockSize, mode, data):
        superBlock = SuperBlock()

        if mode == 0:  # If we work locally
            superBlock.createFromBytes(fsimg, superBlockOffset, superBlockSize, mode, None)
            return superBlock
        elif mode == 1:  # If we work remotely
            superBlock.createFromBytes(None, None, None, mode, data)
            print superBlock.inodeCount

    # Reference the volume inodes
    def createInodeList(self, inodeTotalNumber, fsimg, offset, size):
        inodeList = []
        offsetInt = offset
        for i in range(inodeTotalNumber):
            inodeList.append(Inode())
            inodeList[i].createFromBytes(fsimg, offsetInt, size)
            offsetInt += size
        return inodeList

    def createInodeBitmap(self, fsimg):
        inodesBitmap = InodesBitmap()
        inodesBitmap.createFromBytes(fsimg, 2 * self.superBlock.blockSize, self.superBlock.inodeBitmapSize * self.superBlock.blockSize * 8, self.superBlock.inodeCount)
        return inodesBitmap

    def createBlockBitmap(self, fsimg):
        blocksBitmap = BlocksBitmap()
        # Parameters : fsimg, offset, size, blockcount
        blocksBitmap.createFromBytes(fsimg, self.getBlockBitmapOffset() * self.superBlock.blockSize, self.superBlock.zoneBitmapSize * self.superBlock.blockSize * 8, self.superBlock.blockCount)
        return blocksBitmap

    # Compute the size of the inodes table
    def getInodesTableSize(self):
        InodeTotalSize = self.superBlock.inodeCount * 32
        return InodeTotalSize / self.superBlock.blockSize

    # Compute the inode table offset
    def getInodesTableOffset(self):
        InodeTableOffset = 2 + self.superBlock.inodeBitmapSize + self.superBlock.zoneBitmapSize  # La valeur 2 correspond au bloc 0 (reserve) et 1 (superbloc)
        return InodeTableOffset

    # Compute the block bitmap offset
    def getBlockBitmapOffset(self):
        return 2 + self.superBlock.inodeBitmapSize

    # Read a section of data
    def createFromBytes(self, fsimg, offset, size):
        minixfs = open(fsimg)
        minixfs.seek(offset)
        raw_superblock = minixfs.read(size)
        return raw_superblock

    # Get the number of inodes that are allocated in the inodes bitmap
    def getUsedInodesCount(self, data, inodeCount):
        usedInodesCount = 0

        print hexdump.dump(data)
        print "\nusedInodesCount :", usedInodesCount
        return usedInodesCount

    # Count the number of blocks allocated in the block bitmap
    def getUsedBlockCount(self, blockCount, myBitmap):
        allocatedBlocks = 0
        for i in range(blockCount):
            if myBitmap.bits[i] == 1:
                allocatedBlocks += 1
        return allocatedBlocks

    # Count the number of free blocks in the block bitmap
    def getFreeBlockCount(self, blockCount, myBitmap, allocatedBlocks):
        freeBlocks = 0
        for i in range(blockCount):
            if myBitmap.bits[i] == 0:
                freeBlocks += 1
        if freeBlocks == blockCount-allocatedBlocks:  # On s'assure ici de la coherence du nombre de bloc libre trouve
            return freeBlocks
        else :
            print("Probleme avec le check")

    # Count the number of inodes with a name
    def getFileCount(self):
        fileCount = 0
        for i in range(self.superBlock.inodeCount):
            if self.inodes[i].nlinks > 0:
                fileCount += 1
        return fileCount
