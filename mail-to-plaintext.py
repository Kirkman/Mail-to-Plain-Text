#!/usr/bin/python

##########################################
#                                        #
#          MAIL-TO-PLAINTEXT             #
#            for Synchronet              #
#                                        #
#      author: Kirkman                   #
#       email: josh [] joshrenaud.com    #
#        date: Apr 12, 2015              #
#                                        #
##########################################

import sys
import getopt
import email
import base64

# import logging
# logging.basicConfig(filename='/sbbs/mods/mail-to-plaintext/python.log', filemode='a', level=logging.DEBUG)
# logger = logging.getLogger('mail-to-plaintext')

def main(argv):

	msgPath = ''
	recipPath = ''
	errorPath = ''

	try:
		opts, args = getopt.getopt(argv,"hm:l:e:")
	except getopt.GetoptError:
		print 'mail-to-plaintext.py -m <mail msg filename> -l <recip list filename> -e <proc error filename>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'mail-to-plaintext.py -m <mail msg filename> -l <recip list filename> -e <proc error filename>'
			sys.exit()
		elif opt == '-m':
			msgPath = arg
		elif opt == '-l':
			recipPath = arg
		elif opt == '-e':
			errorPath = arg


	if msgPath:
		with open(msgPath) as msgFile:
			data = msgFile.read()

			plaintext = None
			headers = None

			msg = email.message_from_string(data)

			headers = msg.items()

			for part in msg.walk():
				# each part is a either non-multipart, or another multipart message
				# that contains further parts... Message is organized like a tree
				if 'text/plain' in part.get_content_type():

					# grab the content and make sure it's a string
					payload = str( part.get_payload(decode=True) )

					####################################################
					##  I think this commented-out code is obsolete.
					##  Adding "decode=True" to the get_payload() above
					##  seems to have fixed the base64 problem.
					####################################################
					# Get the content encoding. 
					# enc = part['Content-Transfer-Encoding']
					# # Check if encoding is base64. If so, we need to decode it first.
					# if enc == "base64":
					# 	plaintext = base64.decodestring(payload)
					# else:
					# 	plaintext = payload

					plaintext = payload

					# remove any remaining '=' (soft breaks) at end of lines
					plaintext = plaintext.replace('=\r\n','')
					plaintext = plaintext.replace('=\n','')
					plaintext = plaintext.replace('=\r','')
		# if we parsed both headers and plain text, then write the new email
		if plaintext and headers:
			with open(msgPath,'wb') as newMsgFile:
				for header in headers:
					newMsgFile.write( header[0] + ': ' + header[1] + '\r\n' )
				newMsgFile.write( '\r\n\r\n' )
				# write the plain text message
				newMsgFile.write( plaintext )
				newMsgFile.close()
 
		else:
			with open(errorPath,'wb') as errFile:
				errFile.write( 'A mail processing error occurred.')
				if not headers:
					errFile.write( ' No headers detected.')
				if not plaintext:
					errFile.write( ' No plain text detected.')
				errFile.close()


if __name__ == "__main__":
	main(sys.argv[1:])
