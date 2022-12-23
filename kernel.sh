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

rm -r "$NAME*"

wget "$URL"
wget "$URL_SIGN"

unxz "$NAME.tar.xz"

# # add key
gpg --recv-keys "$(gpg --list-packets "$NAME.tar.sign" | grep keyid | grep -o -w '\w\{16\}')" >/dev/null


set -o pipefail
if echo "(gpg --verify "$NAME.tar.sign" "$NAME.tar" 2>&1 >/dev/null)" | grep 'Good Signature': 
then
    echo "The signature for the tar file is not a good signature. Exiting now."
    exit 1
fi

tar xvf "$NAME.tar" > /dev/null

cd "$NAME" || exit

# # cleans the folder
make mrproper

# # cp the config
cp "$SCRIPT_DIR"/.config .

sed -i 's/-march=k8/$(call cc-option,-march=native)/' arch/x86/Makefile

echo "Now will start the compilation of the kernel"
sleep 5

make -j"$MAX_THREADS"
make -j"$MAX_THREADS" modules
sudo make -j"$MAX_THREADS" modules_install
sudo cp -v arch/x86/boot/bzImage /boot/vmlinuz-linux-"$VERSION"
sudo mkinitcpio -k "$VERSION" -g /boot/initramfs-linux-"$VERSION".img

# entry creation 
sudo touch /boot/loader/entries/arch-"$VERSION".conf
echo "title   $VERSION" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf
echo "linux   /vmlinuz-linux-$VERSION" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf
echo "initrd  $UCODE" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf
echo "initrd  /initramfs-linux-$VERSION.img" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf
echo "options $OPTIONS" | sudo tee -a /boot/loader/entries/arch-"$VERSION".conf

mv "$SCRIPT_DIR/.config" "$SCRIPT_DIR/.config.old"

cp .config "$SCRIPT_DIR"
