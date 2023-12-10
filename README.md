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
1. 
2. 

### Tripwire
* **Purpose:** The purpose of using Tripwire is to detect any changes in major directories. If anything slightly changes on a file or within a directory, Tripwire will detect this and notify the admins.

* **Configuration:** 
1. 
2. 

## Disclaimer

This proof of concept code is distributed in the hope that it will be useful for educational purposes only.
