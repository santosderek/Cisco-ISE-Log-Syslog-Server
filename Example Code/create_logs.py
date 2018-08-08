import socket
from random import randint
from time import sleep, gmtime, strftime
from datetime import datetime

def create_log():
    random_ip = '{}.{}.{}.{}'.format(randint(0, 255),
                                     randint(0, 255),
                                     randint(0, 255),
                                     randint(0, 255))
    time_format = strftime("%m %d %H:%M:%S",gmtime())
    exact_time_format = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    log_template = '<181>{tf} dahouck-ise CISE_RADIUS_Accounting 0000008174 1 0 {etf} -04:00 0000106784 3002 NOTICE Radius-Accounting: RADIUS Accounting watchdog update, ConfigVersionId=74, Device IP Address=10.118.113.194, RequestLatency=8, NetworkDeviceName=homeswitch, User-Name=isetest, NAS-IP-Address=10.118.113.194, Service-Type=Framed, Acct-Status-Type=Interim-Update, Acct-Delay-Time=0, Acct-Session-Id=00000000, Acct-Authentic=RADIUS, AcsSessionID=dahouck-ise/321208428/4380, SelectedAccessService=Default Network Access, Step=11004, Step=11017, Step=11117, Step=15049, Step=15008, Step=15048, Step=15048, Step=22094, Step=11005, NetworkDeviceGroups=IPSEC#Is IPSEC Device#No, NetworkDeviceGroups=Location#All Locations, NetworkDeviceGroups=Device Type#All Device Types, CPMSessionID=0a7a6d90J8ZQ4Q0Wj8O6yGEBwbw87i0wurpQFN25LsVzqaxV_So, Model Name=3560-CG, Network Device Profile=Cisco, Location=Location#All Locations, Device Type=Device Type#All Device Types, IPSEC=IPSEC#Is IPSEC Device#No,'
    log_template = log_template.format(tf=time_format,etf=exact_time_format)

    return log_template


def send_log(ip='127.0.0.1', port=8514, log=''):
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(log.encode(), (ip, port))

    sock.close()


def main():
    new_log = create_log()
    send_log(log=new_log)


if __name__ == '__main__':

    for i in range(0, 500):

        main()

        sleep(5)
