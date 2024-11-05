# JEPRNEL

JEPRNEL is a *simple* bash and python script for the mad-lads who run self compiled kernel on arch linux.

*It checks for update, downloads them, checks gpg keys, compiles, makes mkinitcpio, adds boot entries.*

It works only with grub and does **NOT** support systemd-boot, it's an easy fix but I have to study for my exams :(

The script will not create a initramfs as the filesystems' types as well as the ssd protocol should be included in the kernel and not loaded as a module (cool factor +69420)

### USE

The script with no arguments will search online for the last kernel version and update if necessary

**Flags**


- `-e [kernel_version]` -> edit the `.config` in the git repo and copies it to the `version` dir
- `-c [kernel_version]` -> compile the `version` kernel and installs it. Useful if the .config has been edited but the kernel version i still the same
- `-d [kernel_version]` -> deletes mvlinuz and entry of the kernel version

### GUIDE

- make sure that you have all the dependencies for the compilation:

`# pacman -S base-devel xmlto kmod inetutils bc libelf git cpio perl tar xz`

- the only requirements for the script are wget and some python modules:

`# pacman -S wget python-bs4 python-requests`

- edit the jeprnel.py file and set the dir name (default will be in $HOME, and called Kernel)

- simply run the script and everything should work out of the box

- put a .config file on this folder, more info below

**NOTE: after compiling the kernel the user password will be required!**

### CONFIG FILE

The configuration file of the kernel is called `.config` and it must be placed in this directory. Don't worry, the script handles everything. You just need to provide a `.config` file and put it in this folder.

For the creation of the file I suggest to take a look at the [Gentoo Wiki](https://wiki.gentoo.org/wiki/Kernel/Configuration), the [Arch Wiki](https://wiki.archlinux.org/title/Kernel/Traditional_compilation) and some yt videos.

If before compiling you're asked to include or no some entries it is normal. New features are not in your `.config` so you need to manually set them.
