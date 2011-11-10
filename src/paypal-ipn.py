#!/usr/bin/python

# PHP to Python translation from: https://cms.paypal.com/cms_content/US/en_US/files/developer/IPN_PHP_41.txt

import urllib
import cgi
import cgitb
import socket, ssl, pprint
import pickle
import sys
import json


cgitb.enable(logdir='../logs/')

form = cgi.FieldStorage()

req = 'cmd=_notify-validate'
for k in form.keys():
	v = form[k]
	value = urllib.quote(v.value.decode('string_escape')) # http://stackoverflow.com/questions/13454/python-version-of-phps-stripslashes
	req = req + '&{0}={1}'.format(k, value)

header = 'POST /cgi-bin/webscr HTTP/1.0\r\n'
header += 'Content-Type: application/x-www-form-urlencoded\r\n'
header += 'Content-Length: ' + str(len(req)) + '\r\n\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s)
ssl_sock.connect(('www.sandbox.paypal.com', 443)) # Use this for sandbox testing
# ssl_sock.connect(('www.paypal.com', 443)) # Use this for production


ssl_sock.write(header + req)

data = ssl_sock.read()
VERIFIED = False
while len(data) > 0:
	if 'VERIFIED' in data:
		VERIFIED = True
		break
	elif 'INVALID' in data:
		VERIFIED = False
		break


	data = ssl_sock.read()



ssl_sock.close()


if not VERIFIED:
	print "Content-type: text/plain"
	print
	print "Not Verified"
	sys.exit(1)

fields = {	'item_name': None, 
		'item_number': None,
		'payment_status': None,
		'mc_gross': None,
		'mc_currency': None,
		'txn_id': None,
		'receiver_email': None,
		'payer_email': None,
		'custom': None,
	}


for k in fields.keys():
	if k in form:
		fields[k] = form[k].value



item_name = fields['item_name']
item_number = fields['item_number']
payment_status = fields['payment_status']
payment_amount = fields['mc_gross']
payment_currency = fields['mc_currency']
txn_id = fields['txn_id']
receiver_email = fields['receiver_email']
payer_email = fields['payer_email']

# check the payment_status is Completed
# check that txn_id has not been previously processed
#  check that receiver_email is your Primary PayPal email
# check that payment_amount/payment_currency are correct
# process payment

print "Content-type: text/plain"
print
print "Verified"
