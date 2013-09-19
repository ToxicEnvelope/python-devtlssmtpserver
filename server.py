from twisted.internet import reactor, ssl
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver


class TLSFactory(ServerFactory):
    mailcontent = []
    communication = []


class TLSServer(LineReceiver):
    inData = False

    def connectionMade(self):
        self.sendLine("220 this.mx ESMTP Dev Server")
    
    def lineReceived(self, line):
        self.factory.communication.append(line)

        if "ehlo" in line:
            self.sendLine("250-this.mx at your service")
            self.sendLine("250-SIZE 35882577")
            self.sendLine("250-8BITMIME")
            self.sendLine("250 STARTTLS")
            print "Hello yourself"
            return

        if "starttls" in line.lower():
            print "-- Switching to TLS"
            self.sendLine('220 Go ahead, i like TLS')
            ctx = ssl.DefaultOpenSSLContextFactory(
                    privateKeyFileName='certs/server.key', 
                    certificateFileName='certs/server.crt',
                    sslmethod=ssl.SSL.SSLv23_METHOD)
                    
            self.transport.startTLS(ctx, self.factory)
            return
       
        if line == "quit":
            self.sendLine("221 2.0.0 Bye")
            self.transport.loseConnection()
            reactor.stop()

        if not "data" in line:
            if not self.inData:
                self.sendLine("250 OK")
                return

            if line == ".":
                self.sendLine("250 2.0.0 OK, MESSAGE ACCEPTED")
            else:
                self.factory.mailcontent.append(line)
        else:
            self.sendLine("354 End data with <CR><LF>.<CR><LF>")
            print "--- 354 End data with <CR><LF>.<CR><LF>"
            self.inData = True


class SMTPDevServer(object):
    port = None

    def __init__(self, port=102525):
        self.port = port

    def receiveOneMail(self):
        factory = TLSFactory()
        factory.protocol = TLSServer
        con = reactor.listenTCP(self.port, factory)
        reactor.run()
        con.stopListening()
        return {"communication": factory.communication, "rawmail": factory.mailcontent}

if __name__ == '__main__':
    smtp = SMTPDevServer(port=2525)
    comm, mail = smtp.receiveOneMail()
