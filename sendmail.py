#!/usr/bin/python

import sys
import argparse
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Sends a Mail from CLI')
	parser.add_argument('recipients', metavar='N', type=str, nargs='+',
	                   help='The Recipients')
	parser.add_argument('--subject', '-s', dest='subject', action='store', default="Testmail",
	                   help='The Subject for the mail to be send')
	parser.add_argument('--Host', '-H', dest='host', action='store', default="localhost",
	                   help='The mailserver to which the mails gets send to')
	parser.add_argument('--port', '-p', dest='port', action='store', default=2525,
	                   help='The SMTP Port of the Mailserver')
	parser.add_argument('--user', '-u', dest='username', action='store', default=None,
	                   help='Username for the SMTP Auth')
	parser.add_argument('--Password', '-P', dest='password', action='store', default=None,
	                   help='The Password for the SMTP Auth')
	parser.add_argument('--from', '-f', dest='emailfrom', action='store', default="sender@domain.local",
		               help='The Password for the SMTP Auth')
	parser.add_argument('--file', '-F', dest='mailfromfile', action='store',
			           help='The Password for the SMTP Auth')
	parser.add_argument('--cert', '-c', dest='certificate', action='store', default="certs/client",
			           help='Certificate File for the TLS Connection')
	parser.add_argument('--nummails', '-n', dest='nummails', action='store', default=1,
			           help='Number of mails to send, for testing only')
	parser.add_argument('--batv', '-b', dest='batv', action='store', default=0,
			           help='Using BATV. parameter gets added')
	args = parser.parse_args()

	if not args.mailfromfile:
		stdin = sys.stdin.read()
	else:
		stdin = ""

	if not len(args.recipients):
		print "No recipients provided"
		exit(1)
		
	for i in range(int(args.nummails)):
		#for r in args.recipients:
			
		fromAddr = args.emailfrom
		if not fromAddr: fromAddr = args.username
			
		msg = MIMEMultipart()
		msg['Subject'] = args.subject
		msg['From'] = fromAddr
		msg['To'] = ",".join(args.recipients)
		print "-- Sending #%i mail to: %s" % (i,msg['To'])

		msg.attach(MIMEText(stdin, 'plain'))
		print msg
		
		server = smtplib.SMTP(args.host, args.port)
		server.set_debuglevel(9999)
		server.ehlo()
		 
		if args.certificate:
			print "-- Using Certificate"
			keyfile = "%s.key" % args.certificate
			certfile = "%s.crt" % args.certificate
			print "-- Keyfile: %s and Certfile: %s" % (keyfile,certfile)
			server.starttls(keyfile, certfile)
		else:	
			server.starttls()

			pass


		if args.username:
			server.login(args.username, args.password)
		#server.set_debuglevel(1)
		rctpOptions = []	
		#rctpOptions = ['NOTIFY=SUCCESS', 'ORCPT=rfc822;%s' % r]
		envFrom = msg['From']
		if args.batv:
			envFrom = "prvs=%s=%s" % (args.batv, msg['From'])
		
		if not args.mailfromfile:
			rawmessage =  msg.as_string()
		else:
			f = open( args.mailfromfile)
			rawmessage = f.read()
			f.close()
			
		server.sendmail(envFrom, args.recipients,rawmessage)
		server.quit()
	exit(0)
