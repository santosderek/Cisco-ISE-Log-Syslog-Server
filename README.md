# Cisco-ISE-Log-Syslog-Server
Repository Joe Galtman, Ava Masseria, and Derek Santos (me) created to parse Cisco ISE logs by IP Address during our internship at Cisco 2018.

### Installation (Independent to Docker)

Tested on Python 3.6.X.

The project uses two 3rd party python modules; ```requests``` and ```Flask```. These need to be installed prior to running the project.

This can be used with ***pip3***:

    pip3 install flask requests

***or***

Use the setup.py script provided:

MacOS & Linux

     python3 setup.py install

Windows

     python setup.py install
## Using the Project

### Running the project

    python3 run.py

### Running in debug mode

    python3 run.py --debug

### Help page

    python3 run.py --help

### Change default port

    python3 run.py --port 8080

### Change default ip address

    python3 run.py --ip 192.168.1.23

## Installation w/ Docker

***Within root project directory***

*Build docker container:*

    docker build -t cisco-syslog .

*Run docker container*

     docker run -d --name cisco -p 8514:8514/udp -p 8066:80/tcp cisco-syslog
    
***Now project is accessible through http://\<ip address\>:80***
