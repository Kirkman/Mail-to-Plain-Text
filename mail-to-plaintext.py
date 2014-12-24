#!/usr/bin/python

##########################################
#                                        #
#          MAIL-TO-PLAINTEXT             #
#            for Synchronet              #
#                                        #
#      author: Kirkman                   #
#       email: josh [] joshrenaud.com    #
#        date: Dec 23, 2014              #
#                                        #
##########################################

import sys
import getopt
import email
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
				if part.get_content_type() == 'text/plain':
					# grab the plain text content and make sure it's a string
					plaintext = str( part.get_payload() )
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



if __name__ == "__main__":
	main(sys.argv[1:])
