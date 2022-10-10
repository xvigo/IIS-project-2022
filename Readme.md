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


    $ psql --host=ec2-54-194-180-51.eu-west-1.compute.amazonaws.com --port=5432 --username=xrazzggtkegawp --password --dbname=dfur7dcgfmutjb

* You will be aksed for password, which is:
    ```
    38c7259d2fb0f773960265fa484c1725954e22d58496cc988aa6697a8c4f6b6a
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

    
    postgresql://xrazzggtkegawp:38c7259d2fb0f773960265fa484c1725954e22d58496cc988aa6697a8c4f6b6a@ec2-54-194-180-51.eu-west-1.compute.amazonaws.com:5432/dfur7dcgfmutjb
    