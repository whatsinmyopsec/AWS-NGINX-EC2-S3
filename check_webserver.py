"""A tiny Python program to check that nginx is running and start it if not.
Try running this program from the command line like this:
  python3 start_webserver.py
"""

import subprocess
import sys


def startnginx():
    cmd = 'ps -A | grep nginx | grep -v grep'

    (status, output) = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if status == 0:
        print("Nginx server is already running")
        sys.exit(1)
    else:
        sys.stderr.write(output)
        print("Nginx Server not running, so let's try to start it now...")
        cmd = 'sudo service nginx start'
        (status, output) = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if status:
            print("--- Error starting nginx! ---")
            sys.exit(2)
        print("Nginx started successfully")
        sys.exit(0)


# Define a main() function.
def main():
    startnginx()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
