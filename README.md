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

- put a .config file on this folder, more info below

**NOTE: after compiling the kernel the user password will be required!**

### CONFIG FILE

The configuration file of the kernel is called ```.config``` and it must be placed in the kernel main directory. Don't worry, the script handles everything. You just need to provide a ```.config``` file and put it in this folder. 

For the creation of the file I suggest to take a look at the [Gentoo Wiki](https://wiki.gentoo.org/wiki/Kernel/Configuration), the [Arch Wiki](https://wiki.archlinux.org/title/Kernel/Traditional_compilation) and some yt videos.

If before compiling you're asked to include or no some entries it is normal. New features are not in your ```.config``` so you need to manually set them. 
