Python-DevTLSSMTPServer
=======================

Python based TLS-SMTP Server for Development and Testing. The SMTP "Server" does simply nothing with the receiving mail.


Installation
------------

    sudo pip install twisted
    sudo pip install git+git://github.com/tspycher/python-devtlssmtpserver.git#egg=devtlssmtpserver


Usage
-----

    python server.py
    echo "this is a fancy mail" | python sendmail.py recipient@domain.tld