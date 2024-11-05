#!/usr/bin/env bash

cp .config "$1"
cd "$1" || exit

echo "loading..."

make menuconfig

cp .config "$2"
