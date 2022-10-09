# Setup - to start application
Commands: 
 * pip install virtualenv
 * python -m venv .venv
 * source .venv/bin/activate
 * pip install requirements.txt
 * export FLASK_APP=app
 * export FLASK_DEBUG=1
 * flask run
 


 ## Connecting to the database
 1. Connecting to the db via terminal (for modifying db scheme etc.):


    ```
    $ psql --host=ec2-34-247-72-29.eu-west-1.compute.amazonaws.com --port=5432 --username=zrrprrwknjjdep --password --dbname=d4fts6bs7pgc1d

    ```
    You will be aksed for password, which is:
    d143387eaa7912d36c839ea21ca1a22725c86a68c87ecd05ec5f0c54fad453cd

    connection string:
    ```
    postgresql://zrrprrwknjjdep:d143387eaa7912d36c839ea21ca1a22725c86a68c87ecd05ec5f0c54fad453cd@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/d4fts6bs7pgc1d
    ```