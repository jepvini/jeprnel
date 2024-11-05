#!/usr/bin/env python

import os
import subprocess as sb
import sys

import bs4
import requests

# Macro Sections
URL = "https://www.kernel.org/"

# name of the directory where the kernels will be downloaded, if not present it will be created
DIR_NAME = "Kernel"

#################################################################
#                         CODE SECTION                          #
#################################################################
USER_NAME = sb.check_output("whoami", encoding="utf-8").strip()
DIR = "/home/" + str(USER_NAME) + "/" + DIR_NAME
SCRIPT_DIR = os.getcwd() + "/kernel.sh"


# Checks latest kernel from URL
def get_kernel():
    try:
        req = requests.get(URL)
        bs_txt = bs4.BeautifulSoup(req.text, "html.parser")
        kernel_version_td = bs_txt.find(id="latest_link")
        return [
            kernel_version_td.find("a").get("href"),
            kernel_version_td.find("a").getText(),
        ]
    except requests.ConnectionError:
        print("URL not reachable, check connection and retry")
        exit(0)


# Checks current kernel
def check_kernel():
    return sb.check_output(["uname", "-r"], encoding="utf-8").split("-")[0]


# Updates the kernel -> kernel.sh is a bash script
def update(last_version):
    folder_name = "linux-" + last_version[1]
    sb.run(
        [
            SCRIPT_DIR,
            DIR,
            last_version[0],
            last_version[0].replace(".xz", ".sign"),
            folder_name,
            last_version[1],
        ]
    )
    return


# main
def main():

    if len(sys.argv) == 2:
        if sys.argv[1] == "-v":
            print(get_kernel()[1])
            exit()

    print("--  --  JEPRNEL, by Jep  -- --")
    print("")

    if len(sys.argv) == 3:
        if sys.argv[1] == "-c":
            sb.run(
                [
                    sys.argv[0].replace("jeprnel.py", "rebuild.sh"),
                    DIR + "/linux-" + sys.argv[2],
                    sys.argv[0].replace("jeprnel.py", ""),
                    sys.argv[2],
                ]
            )
            exit()
        if sys.argv[1] == "-e":
            sb.run(
                [
                    sys.argv[0].replace("jeprnel.py", "edit.sh"),
                    DIR + "/linux-" + sys.argv[2],
                    sys.argv[0].replace("jeprnel.py", ""),
                ]
            )
            exit()
        if sys.argv[1] == "-d":

            print("Are you sure to delete Linux ", sys.argv[2], "? [y,N]")

            if input().lower().strip() != "y":
                print("Exiting...")
                exit(0)

            vmlinuz = "/boot/vmlinuz-linux-" + sys.argv[2]

            sb.run(["sudo", "rm", vmlinuz])
            sb.run(["sudo", "grub-mkconfig", "-o", "/boot/grub/grub.cfg"])

            print("Linux version", sys.argv[2], "removed")
            exit(0)

    elif len(sys.argv) > 1:
        print(len(sys.argv))
        sb.run(["cat", "README.md"])
        exit(0)

    last_version = get_kernel()
    last_version_splitted = str(last_version[1]).split(".")
    current_version_splitted = check_kernel().strip().split(".")

    same = True
    for i in range(3):
        if current_version_splitted[i] < last_version_splitted[i]:
            same = False

    if not same:
        print("New kernel", last_version[1], "available")
        print("Would you like to update? [Y,n]")
        while 1:
            char = input()
            if char.strip().lower() == "y":
                update(last_version)
                break
            elif not char:
                update(last_version)
                break
            elif char.strip().lower() == "n":
                print("Exiting...")
                exit()

            print("Input is not valid, please type 'Y' or 'n'")

    else:
        print(check_kernel().strip(), "is the latest version")
        print("Would you like to re-update [y, N]")
        while 1:
            char = input()
            if char.strip().lower() == "y":
                update(last_version)
                break
            elif not char:
                print("Exiting...")
                break
            elif char.strip().lower() == "n":
                print("Exiting...")
                exit()

            print("Input is not valid, please type 'y' or 'N'")


if __name__ == "__main__":
    sys.exit(main())
