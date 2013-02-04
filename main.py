#!/usr/bin/env python

# main function of program
# author: Prakash Gamit <prakashgamit23@gmail.com>
#         Indian Institute of Technology, Roorkee

import threading, Queue, getopt, time, sys
import topports, parseoptions, scanner, ScannerThread


def main():
    
    print "TCP-SYN-Scanner", scanner.version

    parseoptions.parseOptions(sys.argv[1:])

    # check if portlist is empty or not
    # if empty, scan top ten default ports
    if scanner.portlist.empty():
        for p in topports.topports:
            scanner.portlist.put(p)

    print "Scanning started..."

    scanner.output += "%5s\tSTATE" %("PORT")

    threads = []
    if scanner.verbose:
        print "creating" scanner.totalThreads, "..."

    for i in range(1, scanner.totalThreads+1):
        if scanner.verbose:
            print "creating Thread", i, "..."

        t = ScannerThread.ScannerThread(scanner.portlist, i)
        t.setDaemon(True)
        t.start()
        threads.append(t)

        if scanner.verbose:
            print "created Thread", i, "..."
    # end for block

    scanner.portlist.join()

    # wait for all threads to finish
    for item in threads:
        item.join()

    print scanner.output
    print "Finished scanning..."


if __name__ == "__main__":
    main()
