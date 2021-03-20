#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ssl
from datetime import datetime
import pytz
import OpenSSL
import socket
import getpass
from datetime import timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


print("Program to check SSL certificate validity \n")
# opening file
ipfile = open('server_ip.txt')
cur_date = datetime.utcnow()
mailbody = ""
expcount = 0
expday = input("Please provide threshold expiry date :")
from_mail = input("Your mail id : ")
passwd = getpass.getpass("password : ")
to_mail = input("Target mail id : ")

# checking certificate validity
for ip in ipfile:
    try:
        host = ip.strip().split(":")[0]
        port = ip.strip().split(":")[1]
        print("\nChecking certifcate for server ", host)
        ctx = OpenSSL.SSL.Context(ssl.PROTOCOL_TLSv1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        cnx = OpenSSL.SSL.Connection(ctx, s)
        cnx.set_connect_state()
        cnx.do_handshake()
        cert = cnx.get_peer_certificate()
        s.close()
        server_name = cert.get_subject().commonName
        print (server_name)
        edate = cert.get_notAfter()
        edate = edate.decode()
        exp_date = datetime.strptime(edate, '%Y%m%d%H%M%SZ')
        days_to_expire = int((exp_date - cur_date).days)
        print("day to expire", days_to_expire)
        # preparing mail body
        if days_to_expire < int(expday):
            expcount = expcount+1
            mailbody = mailbody+"\n  Server name ="+server_name + \
                ", Days to expire:"+str(days_to_expire)

    except:
        print ("error on connection to Server,", host)
print (mailbody)

# sending mail if any certificate going to expire within threshold days
if expcount >= 1:
    try:
        print("\nCertifcate alert for "+str(expcount)+" Servers,Sending mails")

        body = "Following certificate going to expire, please take action \n"+mailbody
        # change here if you want to use other smtp server
        s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        s.starttls()
        s.login(from_mail, passwd)

        msg = MIMEMultipart()       # create a message
        msg['From'] = from_mail
        msg['To'] = to_mail
        msg['Subject'] = "Certificate Expire alert"
        # add in the message body
        msg.attach(MIMEText(str(body), 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        print("Mail sent")
        s.close()
    except:
        print ("Sending mail failed")
else:
    print("All certificate are below the threshold date")

print ('\nCert check completed')
