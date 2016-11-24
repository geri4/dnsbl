from dnsbl import Base
from providers import BASE_PROVIDERS
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import argparse
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrpit that checks ip address in DNSBL and send alert emails')
    parser.add_argument('-u','--username', help='Input SMTP server username',required=True)
    parser.add_argument('-p','--password', help='Input SMTP server password',required=True)
    parser.add_argument('-s','--server', help='Input SMTP server address',required=True)
    parser.add_argument('-r','--recipient', help='Input email recipient',required=True)
    parser.add_argument('-a','--address', help='Input Ip address to check',required=True)
    parser.add_argument('-P','--port', help='Input SMTP server port',required=False, default=587)
    parser.add_argument('-t','--timeout', help='Input report timeout',required=False, default=3600)
    return parser.parse_args()

def send_email(serverAddress, username, password, recipient, message, ipAddress, serverPort):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = 'Your address {address} is found in DNSBL'.format(address=ipAddress)
    msg.attach(MIMEText(message, 'plain'))
    server=smtplib.SMTP(serverAddress, serverPort)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, recipient, msg.as_string())
    server.quit()

def dnsbl_check(ip):
    backend = Base(ip=ip, providers=BASE_PROVIDERS)
    return backend.check()

def main():
    args = parse_arguments()
    oldmessage = ''
    while True:
        message = ''
        dnsbl_list = dnsbl_check(args.address)
        for dnsbl in dnsbl_list:
            if dnsbl[1]:
                message += 'DNSBL: {dnsbl} Value: {value}\n'.format(dnsbl=dnsbl[0], value=dnsbl[1])
        if message != oldmessage:
            oldmessage = message
            if message:
                send_email(args.server, args.username, args.password, args.recipient, message, args.address, args.port)
        time.sleep(args.timeout)

if __name__ == '__main__':
    main()
