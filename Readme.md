# Town issues - information system for reporting problems in your city
The system is meant for the following types of users: 
 - Citizens - can report and view the problems in the city
 - City managers - manage the reported problems, add technician accounts and assign technicians to fix the problems
 - Technicians - wiew and discuss the problems they have been asigned

## Setup - to start application locally
Commands: 

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_debug.py
```

## Project files
 * **Procfile** - file that tells heroku how to run this app
 * **requirements.txt** - dependencies which are needed to run this app
 * **run_debug.py** - use this to run app locally in debug mode - it has hardcoded configuration
 * **run.py** - used for running on the server - takes congifuration from enviroment variables
 * **TownIssues/config.py** - contains class with configuration variables for running on the server

#### Running on the server explained
 * Procfile executes run.py which starts creating app instance
 * run.py executes app factory create_app() located in TownIssues/\_\_init\_\_.py
 * create_app() gets configuration from Config class variables located in config.py
 * Config class initializes its config variables form enviroment variables
 * finally app is created inside run.py

#### Running locally explained
 * run_debug.py calls app factory create_app(DebugConfig) with custom configuration parameter
 * DebugConfig is a class with hardcoded configuration variables located inside run_debug.py
 * app is created inside run_debug.py
    
