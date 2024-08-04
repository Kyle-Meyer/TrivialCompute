
import subprocess

def launch_pygame_instance():
    # Start main.py and wait for 
    # it to finish
    subprocess.Popen(["python", "src/main.py"])

if __name__ == "__main__":
    # Launch two instances of main.py
    launch_pygame_instance()
    launch_pygame_instance()