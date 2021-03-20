#!/usr/bin/env python
# -*- coding: utf-8 -*-

import OpenSSL
import ssl, socket
import argparse

# get domain
parser = argparse.ArgumentParser()
parser.add_argument("domain")
args = parser.parse_args()
domain = args.domain

# get SSL Cert info
cert = ssl.get_server_certificate((domain, 443))
x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
x509info = x509.get_notAfter()

exp_day = x509info[6:8].decode('utf-8')
exp_month = x509info[4:6].decode('utf-8')
exp_year = x509info[:4].decode('utf-8')
exp_date = str(exp_day) + "-" + str(exp_month) + "-" + str(exp_year)

print("SSL Certificate for domain", domain, "will be expired on (DD-MM-YYYY)", exp_date)
