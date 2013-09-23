Python-DevTLSSMTPServer
=======================

Python based TLS-SMTP Server for Development and Testing. The SMTP "Server" does simply nothing with the receiving mail.


Installation
------------

    sudo pip install twisted
    sudo pip install https://github.com/tspycher/python-devtlssmtpserver/archive/master.zip#egg=devtlssmtpserver


Usage
-----

How to use the class in your unittest or test application

    root@devbox01:~# python
    Python 2.x.x
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from devtlssmtpserver import SMTPDevServer
    >>> s = SMTPDevServer(port=22525, timeout=5,tlscert='certs/server.crt', tlskey='certs/server.key')
    >>> s.receiveOneMail()
    Waiting for mail timeout, shutting down reactor
    {'rawmail': [], 'communication': []}

Or to run the standalone version

    python server.py
    echo "this is a fancy mail" | python sendmail.py recipient@domain.tld