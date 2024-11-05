#!/usr/bin/env bash


# # cp the config
cd "$1" || exit


SCRIPT_DIR="$2"
cp "$SCRIPT_DIR"/.config .
echo "your config is here"
echo ""

MAX_THREADS=$(($(grep -c ^processor /proc/cpuinfo) + 1))

echo "compilations will start in 10 seconds"
echo "make sure that you are connected to the AC and the laptop can breath"
echo ""
sleep 5
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
echo ""

make -j"$MAX_THREADS"
make -j"$MAX_THREADS" modules
echo ""
echo "sudo password is required for installing the modules"
echo "press enter to continue..."
echo ""
read -r
sudo make -j"$MAX_THREADS" modules_install
sudo cp -v arch/x86/boot/bzImage /boot/vmlinuz-linux-"$3"

# entry creation
sudo grub-mkconfig -o /boot/grub/grub.cfg

echo ""
echo "done!"
echo "everything is set, just restart your laptop and choose $3 as kernel entry"
echo "enjoy your kernel"
echo ""
echo "Jep"
