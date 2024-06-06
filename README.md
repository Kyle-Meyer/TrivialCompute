DEVELOPMENT WORK IN PROGRESS

NO WHEEL FILE OR INIT.PY

=======Required========
-git
-python 3.1 or higher
-pygame
-cairo

=======To setup a run time environment========
1.) get the latest python distrib: https://www.python.org/downloads/
2.) install git: https://www.git-scm.com/book/en/v2/Getting-Started-Installing-Git
3.) install python
4.) clone this repo to wherever you'd like
5.) setup a python virtual environment
    - open a terminal or command prompt to the TOP LEVEL of your wherever you cloned the repo
    - run the following: "python -m venv env"  
    - a folder should be created at the top of your repo named env, the git ignore is tracked to ignore this
6.) activate your virtual environment in a terminal
    - env\Scripts\activate
7.) install pygame
    - (from your venv terminal) pip install pygame
8.) install cairo
    - (from your venv terminal) pip install pycairo

=======Running========
python main.py
