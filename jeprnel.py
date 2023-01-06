#!/bin/python

import requests
import bs4
import subprocess as sb
import sys

# Macro Sections
URL='https://www.kernel.org/'

# name of the directory where the kernels will be downloaded, if not present it will be created
DIR_NAME='Kernel'

# change it to intel-ucode.img if using an intel processor
UCODE='/amd-ucode.img'

# simply copy and paste the last line of the /boot/loader/entries/arch.conf
OPTIONS='root="LABEL=arch_os" rw log quiet loglevel=0 resume=UUID=5282f4ff-5e48-444b-99f5-550383537484 resume_offset=17693035'

#################################################################
#                         CODE SECTION                          #
#################################################################
USER_NAME=sb.check_output('whoami', encoding='utf-8').strip()
DIR='/home/' + str(USER_NAME) + '/' + DIR_NAME

# Checks latest kernel from URL
def get_kernel():
    try:
        req = requests.get(URL)
        bs_txt = bs4.BeautifulSoup(req.text, 'html.parser')
        kernel_version_td = bs_txt.find(id="latest_link")
        return [kernel_version_td.find('a').get('href'), kernel_version_td.find('a').getText()]
    except requests.ConnectionError:
        print("URL not reachable, check connection and retry")
        exit(0)

# Checks current kernel
def check_kernel():
    return sb.check_output(['uname', '-r'], encoding='utf-8').split('-')[0]


# Updates the kernel -> kernel.sh is a bash script
def update(last_version):
    folder_name = 'linux-' + last_version[1]
    sb.run(['./kernel.sh', DIR, last_version[0], last_version[0].replace('.xz', '.sign'), folder_name, last_version[1], UCODE, OPTIONS])
    return

# main
def main():

    print("--  --  JEPRNEL, by Jep  -- --")
    print("")

    if len(sys.argv) == 3:
        if sys.argv[1] == '-d':

            print('Are you shure to delete Linux ', sys.argv[2], '? [y,N]')

            if input().lower().strip() != 'y': 
                print('Exiting...')
                exit(0) 

            initrams = '/boot/initramfs-linux-' + sys.argv[2] + '.img'
            vmlinuz = '/boot/vmlinuz-linux-' + sys.argv[2]
            entry = '/boot/loader/entries/arch-' + sys.argv[2] + '.conf'

            sb.run(['sudo', 'rm', initrams])
            sb.run(['sudo', 'rm', vmlinuz])
            sb.run(['sudo', 'rm', entry])

            print('Linux version', sys.argv[2], 'removed')
            exit(0)

        else:
            folder_name = 'linux-' + sys.argv[2]
            sb.run(['./kernel_manual.sh', sys.argv[1].replace('.tar.xz', ''), sys.argv[1].replace('.xz', '.sign'), folder_name, sys.argv[2], UCODE, OPTIONS])
            exit(0)
        
    elif len(sys.argv) > 1:
        print(len(sys.argv))
        sb.run(['cat', 'README.md'])
        exit(0)


    last_version = get_kernel()

    if last_version[1] > check_kernel().strip():
        print("New kernel", last_version[1], "avaible")
        print("Would you like to update? [Y,n]")
        while 1:
            char = input()
            if char.strip().lower() == 'y': 
                update(last_version)
                break
            elif not char: 
                update(last_version)
                break
            elif char.strip().lower() == 'n': 
                print("Exiting...")
                exit()

            print("Input is not valid, please type 'Y' or 'n'")

    else:
        print(check_kernel().strip(), "is the latest version")
        print('Would you like to re-update [y, N]')
        while 1:
            char = input()
            if char.strip().lower() == 'y': 
                update(last_version)
                break
            elif not char: 
                print('Exiting...')
                break
            elif char.strip().lower() == 'n': 
                print("Exiting...")
                exit()

            print("Input is not valid, please type 'y' or 'N'")


if __name__ == '__main__':
    sys.exit(main())
