# 1. Introduction


## MLOPS Environment Preparation

**Note**: You don't have to rent an instance in the cloud. Skip the Cloud Steps go to Environment Steps, then You can follow the same instructions 
for setting up your local environment. `Recommended development environment: Mac, Linux, WSL on Windows`. Another Option: Windows but Not Recommended.


## Cloud Steps:

### Cloud Step 1: Create an AWS Account for EC2 Instance.
- Build EC2 Instance: Ubuntu Linux with free tier configuration
	- Give Name EC2 Instance: mlops-... 
	- t2.micro (free tier)
	- Build or Select SSH Key: *.pem file 
	- Disk Space: 30 GB (max free tier)
- Start Created EC2 Instance


### Cloud Step 2: Connect Ubentu EC2 Instance

#### Cloud Step 2.1: Open Local Terminal or GIT Bash on Mac, Linux, WSL

```sh
# For Windows Bash to Connect WSL
wsl
```

#### Cloud Step 2.2: Update existing local packages 

```sh
# Update existing local packages
sudo apt update
```

#### Cloud Step 2.3: Check local home folder

```sh
# Go to local home folder
cd

# Check local directory is in home folder
pwd

# Check local home folder
ls -al
```

#### Cloud Step 2.4: Create local .ssh folder, then copy in ssh key *.pem
**Note**: If you get `It is required that your private key files are NOT accessible by others. This private key will be ignored.` error, you should change permits on the downloaded file to protect your private key:

```sh
# Create local .ssh folder
mkdir .ssh

# Go to local .ssh folder
cd .ssh/

# Copy local *.pem key to in .ssh folder
cp "pem key path" .

# or Copy Manual local mac
open .

# or Copy Manual local wsl
explorer.exe .

# or Copy Manual local linux
sudo apt install nautilus -y
nautilus .

# for local ssh pem key permission error
chmod 400 ~/.ssh/name-of-your-private-key-file.pem
```

#### Cloud Step 2.5: Configure local ssh Connection

```sh
# Build local ssh config File with nano editor in .ssh folder
nano ~/.ssh/config

# Copy Configuration in local nano editor, then Save it! 
Host mlops-zoomcamp             # ssh connection calling name
    User ubuntu                 # username
    HostName 44.206.241.110     # public ip 
    IdentityFile ~/.ssh/name-of-your-private-key-file.pem   # pem file path
    StrictHostKeyChecking no
```
  
#### Cloud Step 2.6: Connect Created EC2 Instance

```sh  
# Connect Created EC2 Instance
ssh mlops-zoomcamp

# Check user is Connected EC2

# for exit
logout
```

## Environment Steps:   

### Step 1: Download and install the Anaconda distribution of Python.

```sh
# Download
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh

# Setup - Attention make sure after installing type yes for auto connect conda enviroment 
bash Anaconda3-2022.05-Linux-x86_64.sh

# exit
logout

# connect and check active environment conda base on wsl
wsl

# connect and check active environment conda base on EC2
ssh mlops-zoomcamp
```

### Step 2: Update existing packages

```sh
sudo apt update
```

### Step 3: Install Docker

```sh
sudo apt install docker.io
```

To run docker without `sudo`:

```sh
sudo groupadd docker
sudo usermod -aG docker $USER
```

### Step 4: Install Docker Compose

Install docker-compose in a separate directory

```sh
mkdir soft
cd soft
```

To get the latest release of Docker Compose, go to https://github.com/docker/compose and download the release for your OS.

```sh
wget https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -O docker-compose
```

Make it executable

```sh
chmod +x docker-compose
```

Add to the `soft` directory to `PATH`. Open the `.bashrc` file with `nano`:

```sh
nano ~/.bashrc
```

In `.bashrc`, add the following line:

```bash
export PATH="${HOME}/soft:${PATH}"
```

Save it and run the following to make sure the changes are applied:

```bash
source ~/.bashrc
```


### Step 5: Run Docker

```sh
docker run hello-world
```

If you get `docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/create": dial unix /var/run/docker.sock: connect: permission denied.` error, restart your VM instance. 



### Step 6: Run jupyter notebook

```sh
# go to home 
cd

# for WSL - go to local windows home
cd /mnt/c/Users/your-windows-username

# create folder jupyter_notebook, then go
mkdir -p jupyter_notebook && cd jupyter_notebook

# run jupyter notebook
jupyter notebook

# for WSL - Close Tilix: Terminal 
# Click to any Link access the notebook on Terminal with Ctrl+
```

### Step 7: Open new Notebook with Python Kernel

```sh
# Python Version Check
!python -V

# Python path check
!which python

```

# Ready For Any Project
