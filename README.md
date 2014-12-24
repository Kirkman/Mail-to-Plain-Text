Mail to Plain Text
=================

This is a Python "Mail Processor" module for use with Synchronet's mail server. The purpose of this module is to convert multi-part MIME emails received via SMTP into pure, plain text emails.

---

Why would someone want to do this?
----------------------------------

This module is useful if you read your Synchronet email primarily through the telnet BBS interface. It ensures that messages remain readable, and don't display with lots of weird codes and symbols.

Why would someone NOT want to do this?
--------------------------------------

If instead you read your Synchronet email using POP or IMAP, then you probably would not want to use this module. This module will strip out every part of the message except the plain text. That means file attachments are removed as well!

How do I install it? 
--------------------

* Make sure you have Python 2.7 installed on your system.

* Put `mail-to-plaintext.py` into `/sbbs/mods/`

* Add the following to your `/sbbs/ctrl/mailproc.ini` file:

```
[PlainText]
	Command = /sbbs/mods/mail-to-plaintext.py -m %m -l %l -e %e
	Native = true
	ProcessSPAM = false
	ProcessDNSBL = false
	Disabled = false
```

* That's it!

---

Credit
------

I learned how to use Python's email processor from this [Stack Overflow answer](http://stackoverflow.com/a/1463144)
