#!/usr/bin/env bash

cp "$2".config "$1"
cd "$1" || exit

echo "loading..."

make menuconfig

cp .config "$2"
