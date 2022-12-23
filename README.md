# JEPRNEL

JEPRNEL is a simple bash and python script for the mad-lads who run self compiled kernel on arch linux.  

*It checks for update, downloads them, checks gpg keys, compiles, makes mkinitcpio, adds boot entries.* 

It works only using systemd-boot and not grub, it's an easy fix but I have to study for my exams :(

### GUIDE

- make sure that you have all the dependencies for the compilation:

```# pacman -S base-devel xmlto kmod inetutils bc libelf git cpio perl tar xz```

- the only requirments for the script are wget, python3 and some pip modules:

```# pacman -S wget```  
```$ pip install requests beautifulsoup4```

- edit the jeprnel.py file and set the dir name (default will be in $HOME, and called Kernel)

- in the jeprnel.py set the UCODE and the OPTIONS

- simply run the script and everything should work out of the box

**NOTE: after compiling the kernel the user password will be required!**
