# Install Linux on Windows with WSL

## Install Ubuntu on WSL for Windows:   

**Installing WSL**: is now easier than ever. Search for **Windows PowerShell** in your Windows search bar, then select **Run as administrator**. 

- [Setting up WSL for a Seamless Data Science Workflow on Windows](https://www.youtube.com/watch?v=IWfsbOzQgXA)

- https://learn.microsoft.com/tr-tr/windows/wsl/install

- https://learn.microsoft.com/tr-tr/windows/wsl/basic-commands


###  Option 1
- At the command prompt type below code, And wait for the process to complete. Ubuntu will then install on your machine. 
```sh 
# Setup WSL install defaulth Ubuntu(WSL)
wsl --install
```
```sh
# Check WSL version
wsl --version
```
```sh
# Update WSL 
wsl --update
```

- **Download Spesific Linux Distros (WSL) on Windows**
```sh 
# Check Available WSL Distros
wsl --list --online
```

###  Option 2 The one line install!

- There is a single command that will install both WSL and Ubuntu at the same time.
When opening PowerShell for the first time, simply modify the initial instruction to:
```sh 
# Download Ubuntu
wsl --install -d ubuntu
```
```sh 
# Set Defaulth WSL Ubuntu
wsl --setdefault ubuntu
```

**Update Ubuntu existing local update packages and upgrade Linux Last Version currently like 23.04 Ubuntu(WSL) on Windows**

- Update existing packages (Required)
```sh
sudo apt update -y
```

- Upgrade Linux currently last Version (Optionally)
```sh
sudo apt upgrade -y
```
```sh 
# Exit WSL
logout
```

- **Check State and Version Ubuntu(WSL) on Windows**
```sh 
# Check State and Version
wsl -l -v
```
```sh
# if ubuntu version 1 set 2 
wsl --set-version ubuntu 2
```
```sh 
# List Installed WSL Distros
wsl --list --all
```

- **Connect Ubuntu(WSL) on `Windows Powershell` or `Command Prompt (CMD)`**
```sh 
# Connect WSL Ubuntu
wsl
```
```sh 
# Restart or Reconnect All Distros WSL
wsl.exe --shutdown
```

- **Remove Ubuntu(WSL) on Windows**
```sh 
# Remove or Delete Ubuntu
wsl --unregister ubuntu
```

### **Start WSL Ubuntu in specific or current folder on Windows**
- Option 1 cd change directory before wsl command in folder
```sh 
cd C:\Users\<USERNAME>
wsl
```

- Option 2 cd change directory with wsl command in folder
```sh 
wsl --cd C:\Users\<USERNAME>
```

- Option 3 cd change directory after wsl command in folder
```sh 
wsl ~
cd /mnt/c/Users/<USERNAME>
```

### for Some Errors 


- [**(OLd Windows) if some error linux-kernel-update-package Ubuntu(WSL) on Windows**](https://learn.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)

- [enabling gpu acceleration on ubuntu on wsl2 on Windows](https://ubuntu.com/tutorials/enabling-gpu-acceleration-on-ubuntu-on-wsl2-with-the-nvidia-cuda-platform#2-install-the-appropriate-windows-vgpu-driver-for-wsl)

### Next