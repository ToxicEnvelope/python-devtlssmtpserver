import threading
import time
import json
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
            return

        if "starttls" in line.lower():
            self.sendLine('220 Go ahead, i like TLS')
            ctx = ssl.DefaultOpenSSLContextFactory(
                    privateKeyFileName='certs/server.key', 
                    certificateFileName='certs/server.crt',
                    sslmethod=ssl.SSL.SSLv23_METHOD)
                    
            self.transport.startTLS(ctx, self.factory)
            return
       
        if line == "quit":
            self.sendLine("221 2.0.0 Bye")
            self.stopProducing()

        if not "data" in line:
            if not self.inData:
                self.sendLine("250 OK")
                return

            if line == ".":
                self.inData = False
                self.sendLine("250 2.0.0 OK, MESSAGE ACCEPTED")
            else:
                self.factory.mailcontent.append(line)
        else:
            self.sendLine("354 End data with <CR><LF>.<CR><LF>")
            self.inData = True

    def connectionLost(self, reason=None):
        self.transport.loseConnection()
        reactor.stop()


class SMTPDevServer(object):
    port = None
    timeout = None

    def __init__(self, port=102525, timeout=None):
        self.port = port
        self.timeout = timeout

    def receiveOneMail(self):
        factory = TLSFactory()
        factory.protocol = TLSServer
        reactor.listenTCP(self.port, factory)

        # setting up thread to check timeout
        if self.timeout:
            self._thread_stop = threading.Event()
            t = threading.Thread(target=self._timeoutCounter, args=())
            t.daemon = True
            t.start()

        #reactor.addSystemEventTrigger('before', 'shutdown', reactor.disconnectAll)
        reactor.run()
        self._thread_stop.set()

        return {"communication": factory.communication, "rawmail": factory.mailcontent}

    def _timeoutCounter(self):
        timeWaited = 0
        while True:
            time.sleep(1)
            timeWaited += 1
            if timeWaited >= self.timeout:
                print "Waiting for mail timedout, shuting down reactor"
                break
        reactor.callFromThread(reactor.stop)

if __name__ == '__main__':
    smtp = SMTPDevServer(port=2525, timeout=10)
    data = smtp.receiveOneMail()
    print json.dumps(data, indent=2)
