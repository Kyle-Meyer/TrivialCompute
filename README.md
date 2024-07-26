DEVELOPMENT WORK IN PROGRESS<br />
<br />
NO WHEEL FILE OR INIT.PY<br />
<br />
=======Required========<br />
-git<br />
-python 3.1 or higher<br />
-pygame<br />
-cairo<br />

=======To setup a run time environment======== <br />
1.) get the latest python distrib: https://www.python.org/downloads/<br />
2.) install git: https://www.git-scm.com/book/en/v2/Getting-Started-Installing-Git<br />
3.) install python<br />
4.) clone this repo to wherever you'd like<br />
5.) setup a python virtual environment<br />
    - open a terminal or command prompt to the TOP LEVEL of your wherever you cloned the repo<br />
    - run the following: "python -m venv env"  <br />
    - a folder should be created at the top of your repo named env, the git ignore is tracked to ignore this<br />
6.) activate your virtual environment in a terminal<br />
    - env\Scripts\activate<br />
7.) install pygame<br />
    - (from your venv terminal) pip install pygame<br />
8.) install cairo<br />
    - (from your venv terminal) pip install pycairo<br />
9.) install numpy<br />
    - (from your venv terminal) pip install numpy<br />
10.) install psycopg2<br />
    - (from your venv terminal) pip install psycopg2-binary<br />
11>) install cv2<br />
    - (from your venv terminal) pip install opencv-python<br />
<br />
=======Running========<br />
(from your venv terminal) python src/main.py<br />
<br />

Database setup<br />
======================================<br />
Download PostgreSQL (This will install pgAdmin 4 as well)<br />
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads<br />

password: postgres<br />
port: 5432<br />
locale: Default locale<br />

Open pgAdmin 4<br />
Create a database with the following:<br />

Host name/address: localhost<br />
Port: 5432<br />
Username: postgres<br />
Password: postgres<br />
database name: trivialCompute<br />

Run the table creation scripts: scripts/01_table_creation_scripts.sql<br />
Run the following script to insert sample categories and questions into the db tables: scripts/02_sample_categories_and_questions.sql<br />


macOS setup python virtual environment<br />
======================================<br />
Source: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/<br />
1. python3.10 -m venv .venv (create new virtual environemnt)<br />
2. source .venv/bin/activate (activate virtual environment)<br />
3. which python (to confirm)<br />
