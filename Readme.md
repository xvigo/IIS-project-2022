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


 ## Connecting to the database
  ##### Connecting to the db via terminal (psql has to be installed on your machine):


    $ psql --host=ec2-54-194-180-51.eu-west-1.compute.amazonaws.com --port=5432 --username=xrazzggtkegawp --password --dbname=dfur7dcgfmutjb

* You will be aksed for password, which is:
    ```
    38c7259d2fb0f773960265fa484c1725954e22d58496cc988aa6697a8c4f6b6a
    ```


 ##### Example use after connecting to db - List all users using sql command: 

    $ select * from u_user;
    id_user | u_name  | u_surname |       u_email        |                          u_password                          
    ---------+---------+-----------+----------------------+--------------------------------------------------------------
        1 | Karel   | Havlíček  | karel.hav@seznam.cz  | $2a$06$hWZMwd3le8ecHIJqeJ0m7uQBQxEKtpWUr6GH5lPmRZqYK7ir.Hxz2
        2 | Adam    | Novák     | adam.novak@seznam.cz | $2a$06$JKfeY8B2ZmnpsC.C3tQBWeG6N77l6N3RmzlOjbPiONnXaF0Jffudy
        3 | Test1   | Test1     | test1@test1.cz       | $2a$06$lOz4SKgNPUIWDGJLc5RLuurndAkwGpGiTMpu9vtcYH3MvuqKrFxGy
        4 | Test2   | Test2     | test2@test2.cz       | $2a$06$Yns7BGwi05bJop00FK3NXupbwpslOp2m9OSDkKTaziI2JnqhQ5QRa
        5 | Test3   | Test3     | test3@test3.cz       | $2a$06$/sOLzui8PYoKeR2yn5Ob0uuoPiZaotvVGkV5VeX7X5aBtPhjwcqY.
    (5 rows)

### App connection string

    
    postgresql://xrazzggtkegawp:38c7259d2fb0f773960265fa484c1725954e22d58496cc988aa6697a8c4f6b6a@ec2-54-194-180-51.eu-west-1.compute.amazonaws.com:5432/dfur7dcgfmutjb
    