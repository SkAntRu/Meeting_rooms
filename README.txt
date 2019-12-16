This Application developed with Python 3.7.0
Using PostgresQL 11

To set up app
1. Download project
2. Install Requirements.txt
3. Set Up PostgresQL
With an exsiting settings in settings.py, run commands below in SQL shell or something else, whatever:

create user atos with password 'atos';
alter user atos createdb;

4. Run from OS shell:
Windows:
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

Linux:
cd to project location
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic

5. Continue in SQL shell:
grant all privileges on database atos_test_conv to atos;
\c atos_test_conv
----------------------------
You are now connected to database "atos_test_conv" as user "postgres".
----------------------------
ALTER ROLE atos SET client_encoding TO 'utf8';
ALTER ROLE atos SET default_transaction_isolation TO 'read committed';
ALTER ROLE atos SET timezone TO 'Europe/Moscow';
GRANT ALL ON ALL TABLES IN SCHEMA public to atos;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to atos;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to atos;
6. Enjoy
