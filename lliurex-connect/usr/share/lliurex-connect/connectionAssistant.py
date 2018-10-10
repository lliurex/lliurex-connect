#!/usr/bin/env python3

# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# Menus: http://zetcode.com/gui/pygtk/

import os
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit", "3.0")
import subprocess
from gi.repository import Gtk
from gi.repository import GdkPixbuf
gi.require_version("AppIndicator3", "0.1")
from gi.repository import AppIndicator3 as appindicator
import iniparse
from appdirs import *

import gettext
gettext.textdomain('lliurex-connect')
_ = gettext.gettext

class connectionAssistant:
    def __init__(self):
        self.APPINDICATOR_ID = 'myappindicator'
        self.ManagedConnection=None
        
        os.chdir("/usr/share/lliurex-connect")
        pass
    
    def main(self):
        indicator = appindicator.Indicator.new(self.APPINDICATOR_ID, os.path.abspath('img/tabletllxcon.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())
        Gtk.main()
        pass

    
    def checkNWManaged(self):
        with open("/etc/NetworkManager/NetworkManager.conf",'r') as fin:
            for line in fin:
                if (line.find("managed=true")!=-1):
                    return True;
            return False
        
    
    def createStaticMenuOption(self, image, label, cb):
        
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.abspath(image), 
            width=16, 
            height=16, 
            preserve_aspect_ratio=True)
    
        img=Gtk.Image.new_from_pixbuf(pixbuf)
        
        item=Gtk.ImageMenuItem()
        item.set_image(img)
        item.set_label(label)
        item.set_always_show_image(True)
            
        item.connect('activate', cb)
        return item
        pass;
    
    def build_menu(self):
        menu=Gtk.Menu()
        
        # Item 1: Enable/Disable wifi
        
        self.ManagedConnection=self.checkNWManaged();
        if (self.ManagedConnection):
            item1Text=_("Disable Wireless Management");
            icon="img/wifion.png";
        else:
            item1Text=_("Enable Wireless Management");
            icon="img/wifioff.png";
        
        
        item1=self.createStaticMenuOption(icon, item1Text, self.cbSetupWifi);
        menu.append(item1)
        
        item2=self.createStaticMenuOption('img/mirror.png', _("Mirror Android on this computer"), self.cbMirror);
        menu.append(item2)
        
        item3=self.createStaticMenuOption('img/xsdl.png', _("Launch Application into Android XSDL Server"), self.cbXSDL);
        menu.append(item3)
        
        item4=self.createStaticMenuOption('img/tabletllxcon.png', _("Help Screen"), self.launchSplash );
        menu.append(item4)
        
        itemquit=self.createStaticMenuOption('img/quit.png', _("Quit"), self.quit);
        menu.append(itemquit)
        
        menu.show_all()
        return menu
    
    def launchSplash(self, widget):
        os.system("./splash.py &");
        pass
    def cbSetupWifi(self, widget):
        self.ManagedConnection=self.checkNWManaged()
        if (self.ManagedConnection):
            command='gksudo ManageWifi.sh false';
        else:
            command='gksudo ManageWifi.sh true';
    
        proc = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        '''print "out:"
        print out
        print "err:"
        print err'''
        
        # Set up
        self.ManagedConnection=self.checkNWManaged();
        if (self.ManagedConnection):
            self.set_label(_("Disable Wireless Management"));
            icon="img/wifion.png";
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.abspath(icon), 
            width=16, 
            height=16, 
            preserve_aspect_ratio=True);
            img=Gtk.Image.new_from_pixbuf(pixbuf)
            self.set_image(img);
            
        else:
            self.set_label(_("Enable Wireless Management"));
            icon="img/wifioff.png";
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.abspath(icon), 
            width=16, 
            height=16, 
            preserve_aspect_ratio=True);
            img=Gtk.Image.new_from_pixbuf(pixbuf)
            self.set_image(img);
        
        pass
    
    def cbMirror(self, widget):
        #command="exec /opt/google/chrome/chrome --profile-directory=Default --app-id=hjbljnpdahefgnopeohlaeohgkiidnoe";
        command='mirroring.sh';
        proc = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        #(out, err) = proc.communicate()
        #print "out"
        #print out
        #print "err"
        #print err
        pass
    
    def cbXSDL(self, widget):
        command="xserver.sh";
        proc = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        '''print "out"
        print out
        print "err"
        print err'''
        pass
    
    def checkHelp(self):
        # requires python3-appdirs
        # requires python3-iniparse
        configfile=user_config_dir("lliurex-connect")+"/config.ini";
        Config=iniparse.ConfigParser();
        
        try:
            print ("Reading "+str(configfile));
            Config.read(configfile);
            showConfig=Config.get("main", "ShowAlways")
            
        except Exception as e:
            print ("Exception...");
            showConfig='True'
        
        print ("showCongif is "+str(showConfig));
        
        if (showConfig=='True'):
            os.system("./splash.py")
        pass
    
    def quit(self, self2):
        Gtk.main_quit()
        pass
        

if __name__ == "__main__":
    app=connectionAssistant()
    app.checkHelp();
    app.main();

    


