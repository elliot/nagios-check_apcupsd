#!/usr/bin/env python

##################################################
# check_apcupsd
#
# Author:  Elliot Anderson <elliot.a@gmail.com>
# License: MIT
##################################################

import optparse
import os
import subprocess
import sys

class APCUPSd(object):

    options = [
        optparse.make_option("-H", "--hostname", dest="host",
                          help="Host to Check", default="127.0.0.1"),
        optparse.make_option("-p", "--port", dest="port",
                          help="Host to Check", default=3551, type="int"),
        optparse.make_option("-m", "--metric", dest="metric",
                          help="APCUPSd metric to check", default="status"),
        optparse.make_option("-C", "--critical", dest="critical",
                          help="Critical Threshold"),
        optparse.make_option("-W", "--warning", dest="warning",
                          help="Warning Threshold")
    ]

    def run(self):
        if not os.path.isfile('/sbin/apcaccess'):
            print "APCUPSd not installed"
            sys.exit(3)

        parser = optparse.OptionParser(option_list=self.options)

        (options, args) = parser.parse_args()

        if options.metric != "status":
            if not options.warning or not options.critical:
                print "Metric '%s' requires threshold levels" % options.metric
                sys.exit(3)

        try:
            self.monitor(options, args)
            sys.exit()
        except Exception, e:
            sys.exit(e)

    def monitor(self, options, args):
        target = "{0}:{1}".format(options.host, options.port)

        command = ['/sbin/apcaccess', 'status', target]
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

        output, err = process.communicate()

        if err:
            print err
            sys.exit(3)

        result = dict((k.strip(), v.strip()) for k, v in (line.split(':', 1) for line in output.splitlines()))

        check = getattr(self, 'check_%s' % (options.metric), self.check_unknown)
        check(result, options)

        sys.exit(0)

    def threshold(self, value, warning, critical):
        value = float(value)

        if value < float(critical):
            sys.exit(2)
        elif value < float(warning):
            sys.exit(1)

    def check_status(self, result, options):
        value = result['STATUS']

        print "Status: {0}".format(value)

        if value != "ONLINE":
            sys.exit(2) 

    def check_charge(self, result, options):
        value = result['BCHARGE'].split(' ')[0]

        print "Battery Charge: {0}%".format(value)

        self.threshold(value, options.warning, options.critical)

    def check_time(self, result, options):
        value = result['TIMELEFT'].split(' ')[0]

        print "Time Remaining: {0} minutes".format(value)

        self.threshold(value, options.warning, options.critical)

    def check_unknown(self, result, options):
        print "Unknown metric"
        sys.exit(3)

if __name__ == '__main__':
    monitor = APCUPSd()
    monitor.run()