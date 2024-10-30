# JEPRNEL

JEPRNEL is a simple bash and python script for the mad-lads who run self compiled kernel on arch linux.

*It checks for update, downloads them, checks gpg keys, compiles, makes mkinitcpio, adds boot entries.*

It works only with grub and does **NOT** support systemd-boot, it's an easy fix but I have to study for my exams :(

The script will not create a initramfs as the filesystems' types as well as the ssd protocol should be included in the kernel and not loaded as a module

### USE

The script with no arguments will search online for the last kernel version and update if necessary

**Flags**

- `-d [kernel_version]` -> deletes initrams, mvlinuz and entry of the kernel version

- `[kernel_file.tar.xz] [kernel_version]` -> the script will install that kernel
note: if there is a `kernel_file.tar.sign` in the same folder of the file the gpg key will be checked

### GUIDE

- make sure that you have all the dependencies for the compilation:

`# pacman -S base-devel xmlto kmod inetutils bc libelf git cpio perl tar xz`

- the only requirements for the script are wget, python3 and some pip modules:

`# pacman -S wget python-bs4 python-requests`

- edit the jeprnel.py file and set the dir name (default will be in $HOME, and called Kernel)

- simply run the script and everything should work out of the box

- put a .config file on this folder, more info below

**NOTE: after compiling the kernel the user password will be required!**

### CONFIG FILE

The configuration file of the kernel is called `.config` and it must be placed in this directory. Don't worry, the script handles everything. You just need to provide a `.config` file and put it in this folder.

For the creation of the file I suggest to take a look at the [Gentoo Wiki](https://wiki.gentoo.org/wiki/Kernel/Configuration), the [Arch Wiki](https://wiki.archlinux.org/title/Kernel/Traditional_compilation) and some yt videos.

If before compiling you're asked to include or no some entries it is normal. New features are not in your `.config` so you need to manually set them.
