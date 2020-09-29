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
