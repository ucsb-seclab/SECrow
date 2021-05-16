Readme for reproducibility submission of paper ID 64

# Source code info
Repository: https://github.com/ucsb-seclab/SECrow
Programming Languages: Python/Java/JavaScript/Bytecode 
Packages/Libraries Needded: [Look for specific instructions below]


# Instructions

## Required for replicating SECROW sample implementation
- Raspberry Pi 3 (for all SECROW implementation Code -- TD code)

## Sample Implementation
- All code for SecROW sample implementation can be found within the `sample-implementation` folder. 
- All the code for TS and CD should be run on the VM, however, all TD code should be run on a raspberry pi 3 running raspbian OS. 
- Before running any files please make sure to open the python-venv by `source .venv/bin/activate` as it contains all needed packages to run the files.
- Always run TD code before running the others

Here are the different folders containing code for the following 

* sample-implementation/
	* adding-owner -- contains code for adding owners for a TD
	* location-query -- contains code for querying location for a particular TD
	* location-update -- contains code for updating location for a TD anonymously
	* location-key -- contains code for checking key for obtaining location
	* no-encrypt -- above implementation but without any encryption
	* time-testing -- contains code for running a time test on implementation


## Required for replicating spoof code
- mitmproxy (installed)
- python3 (installed)
- frida (installed)
- adb (installed)
- 2 Android phones (preferably Pixel devices -- root access)
- GPS Spoofer application (any) installed on one of the Android phone (attacker)

## Spoof code 
- All spoof code used during experiements sits within `spoof-code/` directory.
- There are individual instructions within each folder on how the experiment was performed.
- To recreate please install the non-obfuscated APKs (without -objection.apk) and run the python files. 
- Each device has a set of different ways to test different properties and sample files from our tests have been preserved to the best of ability.
- It is important to install the APKs found within  these folders as the new Google Play Store version may contain updates preventing these attacks. It is also possible some attacks may have been blocked as a result of responsible disclosure by the manufacturer from server-side. 


