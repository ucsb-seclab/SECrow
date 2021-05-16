# Instructions

## Required 
- mitmproxy
- python3
- frida
- adb 
- Raspberry Pi 3 (for all SecROW implementation Code -- TD code)
- 2 Android phones (preferably Pixel devices -- root access)
- GPS Spoofer application (any) installed on one of the Android phone (attacker)

## Spoof code 
- All spoof code used during experiements sits within `spoof-code/` directory.
- There are individual instructions within each folder on how the experiment was performed.
- To recreate please install the non-obfuscated APKs (without -objection.apk) and run the python files. 
- Each device has a set of different ways to test different properties and sample files from our tests have been preserved to the best of ability.
- It is important to install the APKs found within  these folders as the new Google Play Store version may contain updates preventing these attacks. It is also possible some attacks may have been blocked as a result of responsible disclosure by the manufacturer from server-side. 

## Sample Implementation
- All code for SecROW sample implementation can be found within the `sample-implementation` folder. 
- All the code for TS and CD should be run on the VM, however, all TD code should be run on a raspberry pi 3 running raspbian OS. 


