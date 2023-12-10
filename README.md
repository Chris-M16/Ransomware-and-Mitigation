# Ransomware and Mitigation Tech Journal

## Overview

This repository serves as a tech journal containing a proof of concept source code for educational purposes. The code included in this project is designed to demonstrate certain concepts, techniques, or technologies and should be used solely for learning and experimentation. It is not intended for production use, and its reliability or security in real-world applications is not guaranteed.

## Proof of Concept Source Code

This repository contains the proof of concept source code. This code is provided as-is and may not be suitable for use in production environments. It is recommended to review and understand the code thoroughly before attempting to use or modify it.

### Usage

To run the proof of concept code, follow these steps:
_**NOTE:** These scripts were made with the intention of being run on Linux. Our use case was with xubuntu._

1. Clone the repository to the target machine:

    ```bash
    git clone https://github.com/Chris-M16/Ransomware-and-Mitigation
    ```

2. Navigate to the cloned repo:

    ```bash
    cd ./Ransomware-and-Mitigation
    ```

3. Run the encryption script
    * _**NOTE:** The directory being encrypted within this script is set to /home/chris/Documents. You will need to update this to the desired directory._
    ```bash
    python3 ./encrypt.py
    ```
5. Copy the smem-enc file and store it somewhere safely on your device


6. Delete the entire Ransomware-and-Mitigation directory along with all the files within it.

To decrypt the directory:
1. Upload the decrypt.py file back to the target machine along with smem-enc.

2. Make sure both files are in the same directory and that you updated the directory path in decrypt.py to match the one in encrypt.py

3. Run decrypt.py
    ```bash
    python3 ./decrypt.py
    ```

## Mitigation

### Backup and Restoration Scheme
* **Purpose:** Implementing a Backup and Restoration Scheme allows you to back up to a state before being attacked by ransomware which will in turn restore files to their normal state. For this to work well you need to have backups taken daily at the minimum. There are a lot of different schemes that can be used. The following configuration goes over the scheme we chose and the procedure we followed.

* **Configuration:** 
1. Create the following backup.sh file in a safe directory:
    ```bash
    #!/bin/bash

    SOURCE_DIR="/path/to/source"
    BACKUP_DIR="/path/to/backup"
    DATE_FORMAT=$(date +"%Y%m%d")

    tar -cvzf "$BACKUPDIR/backup$DATE_FORMAT.tar.gz" "$SOURCE_DIR"
    ```
2. Add the following line to crontab as the root user:
    ```bash
    0 14 * * * /path/to/backup.sh
    ```
3. This script should now be run every day at 2 pm. Try to set this time to a time when you know you will be on the device roughly every day. This will ensure that the backup remains up to date.

### Tripwire
* **Purpose:** The purpose of using Tripwire is to detect any changes in major directories. If anything slightly changes on a file or within a directory, Tripwire will detect this and notify the admins.

* **Configuration:** 
1. Install Tripwire
   ```bash
   sudo apt update
   sudo apt install -y tripwire
   ```
2. Use all the default answers for every prompt. Insert a password when prompted that you will remember.
3. Initialize Database
    ```bash
    sudo tripwire --init
    ```
4. Edit the following lines in /etc/tripwire/twpol.txt to look like the below
    ```bash
    (
       rulename = "Boot Scripts",
       severity = $(SIG_HI)
    )
    {
             /etc/init.d             -> $(SEC_BIN) ;
             #/etc/rc.boot           -> $(SEC_BIN) ;
             /etc/rcS.d              -> $(SEC_BIN) ;
    ```

    ```bash
    (
       rulename = "System boot changes",
       severity = $(SIG_HI)
     )
     {
             #/var/lock               -> $(SEC_CONFIG) ;
             #/var/run                -> $(SEC_CONFIG) ; # daemon PIDs
             /var/log                -> $(SEC_CONFIG) ;

    ```
    ```bash
    (
       rulename = "Root config files",
       severity = 100
     )
     {
             /root                           -> $(SEC_CRIT) ; # Catch all additions to /root
             #/root/mail                     -> $(SEC_CONFIG) ;
             #/root/Mail                     -> $(SEC_CONFIG) ;
             #/root/.xsession-errors         -> $(SEC_CONFIG) ;
             #/root/.xauth                   -> $(SEC_CONFIG) ;
             #/root/.tcshrc                  -> $(SEC_CONFIG) ;
             #/root/.sawfish                 -> $(SEC_CONFIG) ;
             #/root/.pinerc                  -> $(SEC_CONFIG) ;
             #/root/.mc                      -> $(SEC_CONFIG) ;
             #/root/.gnome_private           -> $(SEC_CONFIG) ;
             #/root/.gnome-desktop           -> $(SEC_CONFIG) ;
             #/root/.gnome                   -> $(SEC_CONFIG) ;
             #/root/.esd_auth                        -> $(SEC_CONFIG) ;
             #/root/.elm                     -> $(SEC_CONFIG) ;
             #/root/.cshrc                   -> $(SEC_CONFIG) ;
             /root/.bashrc                   -> $(SEC_CONFIG) ;
             #/root/.bash_profile            -> $(SEC_CONFIG) ;
             #/root/.bash_logout             -> $(SEC_CONFIG) ;
             /root/.bash_history             -> $(SEC_CONFIG) ;
             #/root/.amandahosts             -> $(SEC_CONFIG) ;
             #/root/.addressbook.lu          -> $(SEC_CONFIG) ;
             #/root/.addressbook             -> $(SEC_CONFIG) ;
             #/root/.Xresources              -> $(SEC_CONFIG) ;
             #/root/.Xauthority              -> $(SEC_CONFIG) -i ; # Changes Inode number on login
             #/root/.ICEauthority                -> $(SEC_CONFIG) ;
    ```
    ```bash
    (
       rulename = "Devices & Kernel information",
       severity = $(SIG_HI),
     )
     {
             /dev            -> $(Device) ;
             /dev/pts        -> $(Device);
             /dev/shm        -> $(Device);
             /dev/hugepages  -> $(Device);
             /dev/mqueue     -> $(Device);
             #/proc          -> $(Device) ;
             /proc/devices           -> $(Device) ;
             /proc/net               -> $(Device) ;
             /proc/tty               -> $(Device) ;
             /proc/cpuinfo           -> $(Device) ;
             /proc/modules           -> $(Device) ;
             /proc/mounts            -> $(Device) ;
             /proc/dma               -> $(Device) ;
             /proc/filesystems       -> $(Device) ;
             /proc/interrupts        -> $(Device) ;
             /proc/ioports           -> $(Device) ;
             /proc/scsi              -> $(Device) ;
             /proc/kcore             -> $(Device) ;
             /proc/self              -> $(Device) ;
             /proc/kmsg              -> $(Device) ;
             /proc/stat              -> $(Device) ;
             /proc/loadavg           -> $(Device) ;
             /proc/uptime            -> $(Device) ;
             /proc/locks             -> $(Device) ;
             /proc/meminfo           -> $(Device) ;
             /proc/misc              -> $(Device) ;
     }
    ```
5. Add the following to the very end of /etc/tripwire/twpol.txt to enable tripwire detection on your desired directory
    ```bash
    # Ruleset for Chris
    (
      rulename = "Chris Directory Ruleset",
      severity= $(SIG_HI)
    )
    {
            /home/chris/Documents        -> $(SEC_CRIT);
    }
    ```
6. Make sure to save these changes and then run the following command to edit the config file:
    ```bash
    sudo twadmin -m P /etc/tripwire/twpol.txt
    ```
7. Then reinitialize tripwire database with the following
    ```bash
    sudo tripwire --init
    ```
8. Run the following command to check the integrity of the system files
    ```bash
    sudo tripwire --check
    ```
9. Now whenever a file or a directory changes that tripwire monitors it will give you a detailed explanation as to what happened when you run:
    ```bash
    sudo tripwire --check
    ```

## Disclaimer

This proof of concept code is distributed in the hope that it will be useful for educational purposes only.
