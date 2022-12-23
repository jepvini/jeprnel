#!/bin/bash

DIR=$1
URL=$2
URL_SIGN=$3
NAME=$4
VERSION=$5
UCODE=$6
OPTIONS=$7


MAX_THREADS=$(grep -c ^processor /proc/cpuinfo)

SCRIPT_DIR=$(pwd)

mkdir -p "$DIR"

cd "$DIR" || exit

pwd

wget "$URL" -O "$NAME.tar.xz"
wget "$URL_SIGN" -O"$NAME.tar.sign"

echo "unxz-ing the file"
unxz "$NAME.tar.xz"

# add key
echo "adding gpg key"
gpg --recv-keys "$(gpg --list-packets "$NAME.tar.sign" | grep keyid | grep -o -w '\w\{16\}')" >/dev/null

echo "checking gpg key"
set -o pipefail
if echo "(gpg --verify "$NAME.tar.sign" "$NAME.tar" 2>&1 >/dev/null)" | grep 'Good Signature': 
then
    echo "The signature for the tar file is not a good signature. Exiting now."
    exit 1
fi

echo "un-tar-ing the tar"
tar xvf "$NAME.tar" > /dev/null

echo "welcome to the kernel folder"
cd "$NAME" || exit

# # cleans the folder
echo "cleaning..."
make mrproper

# # cp the config
cp "$SCRIPT_DIR"/.config .
echo "your config is here"

sed -i 's/-march=k8/$(call cc-option,-march=native)/' arch/x86/Makefile
echo "arch is good"

echo "compilations will start in 5 seconds"
echo "make shure that you are connected to the AC and the laptop can breath"
echo ""
echo "5"
sleep 1
echo "4"
sleep 1
echo "3"
sleep 1
echo "2"
sleep 1
echo "1"
sleep 1
echo "liftoff"

make -j"$MAX_THREADS"
make -j"$MAX_THREADS" modules
echo "sudo password is required for installing the modules"
sudo make -j"$MAX_THREADS" modules_install
sudo cp -v arch/x86/boot/bzImage /boot/vmlinuz-linux-"$VERSION"
sudo mkinitcpio -k "$VERSION" -g /boot/initramfs-linux-"$VERSION".img

# entry creation 
echo "creating the new entry"
sudo touch /boot/loader/entries/arch-"$VERSION".conf
echo "title   $VERSION" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf
echo "linux   /vmlinuz-linux-$VERSION" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf
echo "initrd  $UCODE" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf
echo "initrd  /initramfs-linux-$VERSION.img" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf
echo "options $OPTIONS" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf

mv "$SCRIPT_DIR/.config" "$SCRIPT_DIR/.config.old"

cp .config "$SCRIPT_DIR"

echo "done!"
echo "everything is set, just restart your laptop and choose $VERSION as kernel entry"
echo "enjoy your kernel"
echo ""
echo "Jep"
