# Readme for reproducibility submission of paper ID 64

## Source code info
* Repository: https://github.com/ucsb-seclab/SECrow
* Programming Languages: Python/Java/JavaScript/Bytecode 
* Packages/Libraries Needed: [Look for specific instructions below]


## Instructions

Run all code as standard python3 files by using

```
python3 file.py
```

### Required for replicating SECROW sample implementation
- Raspberry Pi 3 (for all SECROW implementation Code -- TD code)
- USB Powermeter [Link](https://smile.amazon.com/Tester-Eversame-Voltmeter-Ammeter-Braided/dp/B07MGQZHGM/ref=pd_ybh_a_2?_encoding=UTF8&psc=1&refRID=6PWGZYVE6AMYY87X5TS8)

### Sample Implementation
- All code for SecROW sample implementation can be found within the `sample-implementation` folder. 
- All the code for TS and CD should be run on the VM, however, all TD code should be run on a raspberry pi 3 running raspbian OS. 
- Before running any files please make sure to open the python-venv by `source .venv/bin/activate` as it contains all needed packages to run the files.
- Always run TD code before running the others (TS and CD).

### Setting up the Raspberry Pi
- Install raspbian OS 
- Create a python3 virtuanenv by using the command `python3 -m venv .venv`
- Activate the venv by `source .venv/bin/activate`
- Install requirements from `sample-implementation/requirements.txt` by using command `pip3 install -r requirements.txt` from within the venv
- If missing: install bluetooth bindings using `sudo apt-get install bluetooth` and `sudo apt-get install pybluez`
- Once everything is installed, find the Bluetooth Address using `hciconfig`
- Replace this address within the `sample-implementation` python files listed below prior to running them. Within the code the location to change this address is within the paramater `serverAddress`.

**Alternative to above instructions for Raspberry Pi**
If you have issues setting up the Raspberry Pi, you can download our working copy of RaspbianOS that contains all the code required for running the SECrow code. You can download this image [here](https://drive.google.com/file/d/1-Oivi3WmQ-9zbxQEWXYzbTLC94_ZG4pO/view?usp=sharing).

- You can use this image and flash it on the SD Card used within your RaspberryPi. 
- Once the Pi is operational, you can find all needed code files within `~/Documents/`

### Code Heirarchy 

Here are the different folders containing code for the following 

* sample-implementation/
	* adding-owner -- contains code for adding owners for a TD
	* location-query -- contains code for querying location for a particular TD
	* location-update -- contains code for updating location for a TD anonymously
	* location-key -- contains code for checking key for obtaining location
	* no-encrypt -- above implementation but without any encryption
	* time-testing -- contains code for running a time test on implementation

For Table 4:
	* Run code for time testing encryption
For Table 5:
	* Run non-encryption code for baseline
	* Run encryption code for SECROW
For Table 6:
	* Use the USB power meter as mentioned above in devices to measure power requirements on TD

### Assume that you have Raspberry PI and our VM : How to run

**Adding Owner**

```
(.venv) chinmaygarg@Chinmays-MacBook-Pro adding-owner % python3 ts.py
TD Public key loaded.
TD Private key loaded.
CD Public key loaded.
```

```
chinmaygarg@Chinmays-MacBook-Pro adding-owner % python3 cd.py
2021-05-17 21:53:43.223 Python[19683:512863] instantiateOnDevice for regular
TD Public key loaded.
CD Public key loaded.
Private key loaded.
c
Total time: 7.977100849151611
```

*(Note: press any key to initiate adding owner)*

```
09:53:37 (.venv) pi@127 adding-owner ±|master ✗|→ python3 td.py
Public key loaded.
Private key loaded.
Total time in TD: 7.709195137023926
```

**Location Key**

```
09:55:53 (.venv) pi@127 location-key ±|master ✗|→ python3 td.py
Public key loaded.
Public key loaded.
Private key loaded.
Total time: 8.059860467910767
```

```
chinmaygarg@Chinmays-MacBook-Pro location-key % python3 cd.py
2021-05-17 21:56:27.157 Python[19785:514586] instantiateOnDevice for regular
TD Public key loaded.
CD Public key loaded.
Private key loaded.
c
Total time: 8.348144292831421
```

*(Note: press any key to initiate adding owner)*


### Required for replicating spoof code
- mitmproxy (installed)
- python3 (installed)
- frida (installed)
- adb (installed)
- 2 Android phones (preferably Pixel devices -- root access)
- GPS Spoofer application (any) installed on one of the Android phone (attacker)

### Spoof code 
- All spoof code used during experiements sits within `spoof-code/` directory.
- There are individual instructions within each folder on how the experiment was performed.
- To recreate please install the non-obfuscated APKs (without -objection.apk) and run the python files. 
- Each device has a set of different ways to test different properties and sample files from our tests have been preserved to the best of ability.
- It is important to install the APKs found within  these folders as the new Google Play Store version may contain updates preventing these attacks. It is also possible some attacks may have been blocked as a result of responsible disclosure by the manufacturer from server-side. 