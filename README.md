<br />
THIS REPO IS NOW ARCHIVED, TO UNARCHIVE, PLEASE MESSAGE THE OWNER<br />
<br />

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
11.) install cv2<br />
    - (from your venv terminal) pip install opencv-python<br />
12.) install pillow<br />
    - (from your venv terminal) pip install pillow<br />
<br />

=======Running========<br />
(from your venv terminal) python src/main.py<br />
<br />
NOTE: IF you are trying to run the online multiplayer component, you need to first do:<br />
python src/network/server.py this will convert your terminal into a server<br />
<br />
Now you can run<br />
python src/main.py <br />
<br />
and as many instances (up to 4) as you'd like

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

Run the table creation scripts: run scripts 1 - 3 in the scripts folder


macOS setup python virtual environment<br />
======================================<br />
Source: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/<br />
1. python3.10 -m venv .venv (create new virtual environemnt)<br />
2. source .venv/bin/activate (activate virtual environment)<br />
3. which python (to confirm)<br />
