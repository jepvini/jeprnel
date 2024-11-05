#!/usr/bin/env bash

cd "$1" || exit

echo "loading..."

make menuconfig
echo "$2"
cp .config "$2"
