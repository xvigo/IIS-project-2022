# Setup - to start application
Commands: 
 * pip3 install virtualenv
 * python -m venv .venv
 * source .venv/bin/activate
 * pip install requirements.txt
 * export FLASK_APP=TownIssues
 * export FLASK_DEBUG=1
 * flask run
 


 ## Connecting to the database
  Connecting to the db via terminal (psql has to be installed on your machine):


    $ psql --host=ec2-34-247-72-29.eu-west-1.compute.amazonaws.com --port=5432 --username=zrrprrwknjjdep --password --dbname=d4fts6bs7pgc1d

* You will be aksed for password, which is:
    ```
    d143387eaa7912d36c839ea21ca1a22725c86a68c87ecd05ec5f0c54fad453cd
    ```


 Example use after connecting to db - List all users using sql command: 

    $ select * from u_user;
    id_user | u_name  | u_surname |       u_email        |                          u_password                          
    ---------+---------+-----------+----------------------+--------------------------------------------------------------
        1 | Karel   | Havlíček  | karel.hav@seznam.cz  | $2a$06$hWZMwd3le8ecHIJqeJ0m7uQBQxEKtpWUr6GH5lPmRZqYK7ir.Hxz2
        2 | Adam    | Novák     | adam.novak@seznam.cz | $2a$06$JKfeY8B2ZmnpsC.C3tQBWeG6N77l6N3RmzlOjbPiONnXaF0Jffudy
        3 | Test1   | Test1     | test1@test1.cz       | $2a$06$lOz4SKgNPUIWDGJLc5RLuurndAkwGpGiTMpu9vtcYH3MvuqKrFxGy
        4 | Test2   | Test2     | test2@test2.cz       | $2a$06$Yns7BGwi05bJop00FK3NXupbwpslOp2m9OSDkKTaziI2JnqhQ5QRa
        5 | Test3   | Test3     | test3@test3.cz       | $2a$06$/sOLzui8PYoKeR2yn5Ob0uuoPiZaotvVGkV5VeX7X5aBtPhjwcqY.
        6 | pridano | webem     | aa@aaa.cz            | heslo
    (6 rows)

### App connection string:

    
    postgresql://zrrprrwknjjdep:d143387eaa7912d36c839ea21ca1a22725c86a68c87ecd05ec5f0c54fad453cd@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/d4fts6bs7pgc1d
    