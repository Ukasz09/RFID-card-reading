# RFID Card Reading [![License](https://img.shields.io/badge/licence-MIT-blue)](https://choosealicense.com/licenses/mit/) [![Status](https://img.shields.io/badge/status-work--in--progress-yellow)](https://github.com/Ukasz09/RFID-card-reading)

 
RFID card reading application for Client and Server by using MQTT, with CLI as UI. Client application simulate terminal which can read RFID cards (temporary mocked, target by rasberryPi with RFID card reader). Server application - allow to control data in database and generate various reports
<br/>
- Full documentation <br/>
- Use Case Daigram: `use_case_diagram.pdf`
- Client-Server model (MQTT)

![use_case](https://raw.githubusercontent.com/Ukasz09/RFID-card-reading/master/screenshots/use_case.png)

## Screenshots 

![use_case](https://raw.githubusercontent.com/Ukasz09/RFID-card-reading/master/screenshots/client_server.png)

For more: see `screenshots` directories 

## How to use it
1. Install required packages (MQTT) <br/>

```python
pip install -r requirements.txt --user
```

2. Navigate do client or server directory
3. Run script

- Windows
 
Run bash script `run_windows.bat`

- Linux 

Run shell script `run_linux.sh` 

## Software design stuff
✅ Documentation <br/>
✅ MVC (simplified) <br/>
✅ Client-Server model <br/>
___
## 📫 Contact 
Created by <br/>
<a href="https://github.com/Ukasz09" target="_blank"><img src="https://avatars0.githubusercontent.com/u/44710226?s=460&v=4"  width="100px;"></a>
<br/> gajerski.lukasz@gmail.com - feel free to contact me! ✊
