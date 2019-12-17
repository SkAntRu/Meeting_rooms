This app allows you to reserve Meeting Rooms and do some necessary things

Application developed with Python 3.7.0
Using PostgresQL 11

To set up app
1. Download project
2. Creare venv
3. Install Requirements.txt
4. Set Up PostgresQL
With an exsiting settings in settings.py, run commands below in SQL shell or something else, whatever:

create user atos with password 'atos';
alter user atos createdb;

5. Run from OS shell:

5.1 cd to project location

5.2 Windows:
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser

5.2 Linux:
python3 ./manage.py makemigrations
python3 ./manage.py migrate
python3 ./manage.py collectstatic
python3 ./manage.py createsuperuser

6. Continue in SQL shell:
grant all privileges on database atos_test_conv to atos;
\c atos_test_conv
----------------------------
You are now connected to database "atos_test_conv" as user "postgres".
----------------------------
ALTER ROLE atos SET client_encoding TO 'utf8';
ALTER ROLE atos SET default_transaction_isolation TO 'read committed';
ALTER ROLE atos SET timezone TO 'Europe/Moscow';
7. Enjoy
