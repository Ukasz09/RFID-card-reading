# RFID Card Reading [![License](https://img.shields.io/badge/licence-MIT-blue)](https://choosealicense.com/licenses/mit/) [![Status](https://img.shields.io/badge/status-work--in--progress-yellow)](https://github.com/Ukasz09/RFID-card-reading)

 
RFID card reading application for Client and Server. Client application simulate terminal which can read RFID cards (temporary mocked, target by rasberryPi with RFID card reader). Server application - allow to control data in database and generate various reports
<br/>
- :white_check_mark: Client server publish/subscribe messaging pattern (by using MQTT 3.1.1 protocol) <br/>
- :white_check_mark: Security and authentication (By using SSL and uthentication mechanism)
- :white_check_mark: MVC (Model-View-Controller)
- :white_check_mark: Documentation <br/>
- :white_check_mark: Use Case Daigram: `use_case_diagram.pdf`


![use_case](https://raw.githubusercontent.com/Ukasz09/RFID-card-reading/master/screenshots/use_case.png)
![use_case](https://raw.githubusercontent.com/Ukasz09/RFID-card-reading/master/screenshots/class_diagram.png)

## Screenshots 

![use_case](https://raw.githubusercontent.com/Ukasz09/RFID-card-reading/master/screenshots/client_server.png)

For more: see `screenshots` directories 

## How to use it
1. Install required packages (MQTT) <br/>

```bash
pip install -r requirements.txt --user
```
2. Generate certificates and keys:
   Generate pair of keys: <br/>
	`openssl genrsa -des3 -out ca.key 2048`
   Make certificate: <br/>
	`openssl req -new -x509 -days 1826 -key ca.key -out ca.crt`
   Make another pair of keys: <br/>
	`openssl genrsa -out server.key 2048`
	Sign certificate: <br/>
	`openssl req -new -out server.csr -key server.key`
	Verify certificate <br/>
	`openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360`

3.	Make password file (in your mosquitto installation folder, e.g. `/etc/mosquitto/`): 
	`mosquitto_passwd -c passwd.conf server` 
4.  Modify mosquitto.conf file. Append this lines to it: 
	```bash
	allow_anonymous false
	password_file //path to passwd.conf which you had made in section 3//
	port 8883
	cafile //path to ca.crt which you had made in section 2//
	certfile //path to server.crt which you had made in section 2//
	keyfile //path to server.key which you had made in section 2//
	```
2. Navigate do client or server directory
3. Run script

- Windows
 
Run bash script `run_windows.bat`

- Linux 

Run shell script `run_linux.sh` <br/>

You can also run this application by commend: 

```bash
python3 main.py
```

## Documentation and Report

To open documentation:
- open `server` or `client` directory
- unzip `doc.zip` file
- open `index.html` file

You can also find report for this project (PL language, 16 pages)
- `Report_PL.pdf` 

___
## 📫 Contact 
Created by <br/>
<a href="https://github.com/Ukasz09" target="_blank"><img src="https://avatars0.githubusercontent.com/u/44710226?s=460&v=4"  width="100px;"></a>
<br/> gajerski.lukasz@gmail.com - feel free to contact me! ✊
