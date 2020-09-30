# Minix-FS FSCK

This project is a simplified version of a File System Check for the MinixFS file system.

The version 2.7 of Python has been used for this project.

## How to launch the project ?

### Manually

1. Clone the repository

2. If you're using virtualenv, install the requirements to get all the packages necessary to run the program. 

```
pip install -r path/to/requirements.txt
```

3. Run the program

```
python main.py
```

### Docker

1. Clone the repository

2. Create a Docker image locally

```
docker build . -t fsck:v1
```

3. Run the newly created local image

```
docker run -it fsck:v1
```

## The project

The goal of this project was to create a File System Check (FSCK) to check the consistency of a volume formatted with Minix. A FSCK is a tool for checking the consistency of a file system. 

The FSCK created gives informations about :

* The number of inodes and blocks
* The size of the different bitmap of the File System
* The inode table size
* The size of the blocks
* The mounting state
* The number of block used

It also performs some checks to make sure that :

* No file is above the maximum size possible
* The file used are matching the inodes assigned