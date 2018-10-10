#!/usr/bin/env python3
import gi
import os
import apt
import subprocess
gi.require_version('Gtk', '3.0')
gi.require_version("WebKit", "3.0")
from gi.repository import Gtk, Gdk, Pango, WebKit, Gio
import webbrowser
import iniparse
from appdirs import *

import gettext
gettext.textdomain('lliurex-connect')
_ = gettext.gettext


class Splash(Gtk.Window):

    def setTogled(self, widget, data=None):
        if(self.active==True):
            self.active=False
        else:
            self.active=True;
            
        #print("self active is"+str(self.active));
        pass
        

    def __init__(self, checked):
        Gtk.Window.__init__(self, title="splashtitle")
        #print (checked);
        # Set check status
        self.active=False;
        #self.chromeInstalled=False;
        
        if (checked=="True"):
            self.active=True;
            
        '''
        Not needed yet...
        # Is google chrome installed
        #cache=apt.Cache()
        #self.chromeInstalled=cache['google-chrome-stable'].is_installed
        '''
                       
        
        # Creating main container        
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        container.set_border_width(10)
        self.add(container)
        
        #Create Webkit view
        
        self.view = WebKit.WebView();
        self.view.open(os.path.abspath("help/info.html"));
        self.view.connect('navigation-policy-decision-requested', self.on_nav_request)
        self.view.connect('load-finished', self._finished_loading)
        #view.connect("navigation-requested", self.on_click_link)
        
        # Create Message "Don't show in the future"
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        label = Gtk.Label(_("Show this message"), xalign=0)
        check = Gtk.CheckButton()
        check.set_active(self.active)
        check.connect("toggled", self.setTogled, "check button")
        hbox.pack_start(check, False, True, 0)
        hbox.pack_start(label, True, True, 0)
        row.add(hbox)
        
        # Create Close Button
        buttonClose = Gtk.Button(label="Close")
        buttonClose.connect("clicked", self.quit);
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        hbox.pack_end(buttonClose, False, True, 0);
        
        container.add(self.view);
        container.add(row);
        container.add(hbox);

        #view.execute_script("$('#info').html('%s')" % "Pajaritos tralari");
        
        #view.execute_script('tralari()');
        
    #def on_click_link(self, view, frame, request):
    #   print("Mavigation change requested")
    #   #self.webview.get_back_forward_list().clear()
    #   return False
    #    pass
    
    def _finished_loading(self, webview, webfame):
        description=_("LliureX Connect is an small assistant to achieve the connection between tablet and your LliureX computer. For use it, you need to have installed some apps in your tablet:");
        google_desc=_("You need Google Chrome to use Mirroring capabilities in this computer. Press the following link to download Google Chrome."); # not used
        google_link=_("Download Chrome"); # not used
        allcast_desc=_("Allcast Receiver is a Google Chrome App to receive video streaming from an Android Device through Recording and Mirroring App."); # not used
        allcast_link=_("Download AllCast Receiver"); #not used
        mirroring_desc=_("Screen Cast is an Android App that allows us to view our tablet content in a browser window in our computer.");
        mirroring_link=_("Go to app Screen Cast in Google Play");
        xserver_desc=_("XDSL Server is a Linux graphical server for your Android device. It alloys you to launch any application in yout system and see it in your device.");
        xserver_link=_("Go to app X Server for Android in Google Play");
    
        #parameters='"'+description+'","'+google_desc+'","'+google_link+'","'+allcast_desc+'","'+allcast_link+'","'+mirroring_desc+'","'+mirroring_link+'","'+xserver_desc+'","'+xserver_link+'"';
        parameters='"'+description+'","'+google_desc+'","'+google_link+'","'+allcast_desc+'","'+allcast_link+'","'+mirroring_desc+'","'+mirroring_link+'","'+xserver_desc+'","'+xserver_link+'"';
        
        print (parameters);
        
        self.view.execute_script('populateText('+parameters+')');
        pass
    
    def on_nav_request(self, view, frame, request, action, policy, data=None):
        
        # Loading URL in Firefox
        url = request.get_uri()
        
        browser="firefox ";
        #if (self.chromeInstalled):
        #    browser="/opt/google/chrome/google-chrome ";
        
        # BUG: Command is not launched in background!!!
        command=browser+url;
    
        proc = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        
        
        policy.ignore()
        
    
    

    def quit(self, self2):
    
        configdir=user_config_dir("lliurex-connect");
        if not os.path.exists(configdir):
            os.makedirs(configdir)
    
        configfile=configdir+"/config.ini";
        
        Config=iniparse.ConfigParser();
        Config.add_section('main')
        Config.set("main", "ShowAlways", str(self.active))
        with open(configfile, "w") as configfile:
            Config.write(configfile);
        
        Gtk.main_quit()
        pass


        ''' ids del info.html...
        info
        mirror_description
        mirrror_app_link
        
        xsdl_description
        xsdl_app_link'''


def checkConfigFile():
    configfile=user_config_dir("lliurex-connect")+"/config.ini";
    Config=iniparse.ConfigParser();
        
    try:
      Config.read(configfile);
      showConfig=Config.get("main", "ShowAlways")
      #print(showConfig);
    except Exception as e:
      #print ("Exception...");
      showConfig='True'
        
    #print ("showCongif is "+str(showConfig));
    return showConfig
        
    pass
    

def splashwindow():
    checked=checkConfigFile()
    #print (checked);
    window = Splash(checked)
    window.set_size_request(640, 480);
    window.set_decorated(False)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()

splashwindow()


