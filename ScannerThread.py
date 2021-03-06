
import threading
import Queue
import time
import topports, parseoptions, scanner
from scapy.all import *


class ScannerThread(threading.Thread):
    def __init__(self, portlist, tid):
        threading.Thread.__init__(self)
        self.portlist = portlist
        self.tid = tid


    def run(self):
        if scanner.verbose:
            print "started Thread", self.tid

        # ports scanned by this thread
        totalPorts = 0

        while True:
            port = 0
            try:
                port = self.portlist.get(timeout=1)
            except Queue.Empty:
                return

            response = sr1(IP(dst=scanner.target)/TCP(dport=port, flags="S"),verbose=False, timeout=0.2)

            if response:
                # flags is 18 if SYN,ACK received
                # i.e port is open
                if response[TCP].flags == 18:
                    scanner.output += "%5d\tOPEN\n" %port

            totalPorts += 1
            self.portlist.task_done()
        # end while block

        if scanner.verbose:
            print "Thread", self.tid, "scanned", totalPorts, "ports"
