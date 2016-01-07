#!/usr/bin/env python
import gtk
import appindicator
import threading
import subprocess
import sys

# usage : 
# python bash-indicator.py <bash script> <applet icon>
# exemples : 
#  './bash-indicator.py' "while true ; do cut -d\  -f1,2,3 /proc/loadavg ; sleep 3; done"  
#  './bash-indicator.py' "while true ; do weather  -i LFBO -m | grep Temperature:|cut -d: -f2; sleep 300; done"
#  './bash-indicator.py' "ssh  user@xxxxxxx  'while [ 1 ] ; do cut -d\  -f1,2,3 /proc/loadavg ; sleep 3; done'" "raspberry-pi.png"
#  './bash-indicator.py'  "while true ; do sensors -A radeon-pci-0200 | grep temp | cut -d\  -f9  ; sleep 3; done "  "twb_thermometer.png"
#  ./bash-indicator/bash-indicator.py  "while true ; do sensors -u | grep '_input:' | cut -d: -f2|cut -c 2-|sed 's|.000||g'|sort|tail -n 1; sleep 1; done" "thermometer.png"

class AppIndicator:
    def __init__(self):
        self.ind = appindicator.Indicator("bash-indicator",
            "bash", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.menu = gtk.Menu()
        item = gtk.MenuItem("Quitter")
        item.connect("activate", self.quit, None)
        self.menu.append(item)
        self.menu.show_all()
        self.ind.set_menu(self.menu)
        self.ind.set_label(" ")
        self.th = threading.Thread(target=self.tail)
        if len(sys.argv) > 2:
        	self.ind.set_icon(sys.argv[2])
        self.th.start()
    
    def quit(self, *args):
        print "quit"
        self.pp.kill()
        self.th._Thread__stop()
        gtk.main_quit()
        sys.exit()

    def tail(self):
       self.pp = subprocess.Popen(["/bin/bash", "-c", sys.argv[1]], stdout=subprocess.PIPE)
       line = self.pp.stdout.readline()[0:-1][0:30]
       self.ind.set_label(line)
       while line:
         line = self.pp.stdout.readline()[0:-1][0:30]
         self.ind.set_label(line)

    
gtk.gdk.threads_init()
AppIndicator()
gtk.main()

