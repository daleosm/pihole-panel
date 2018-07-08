import gi
import json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import urllib.request
url = "http://192.168.0.12/admin/api.php"
resp = urllib.request.urlopen(url).read().decode("UTF-8")
json_obj = json.loads(resp)

class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Grid Example")

        print (json_obj)
        print(json_obj['ads_blocked_today'])

        grid = Gtk.Grid()
        self.add(grid)

        button1 = Gtk.Button(label="Button 1")
        button2 = Gtk.Label(label="Blocked Today: " + str(json_obj['ads_blocked_today']), angle=0, halign=Gtk.Align.END)
        button3 = Gtk.Button(label="Button 3")
        button4 = Gtk.Label(label="DNS Queries Today: " + str(json_obj['dns_queries_today']), angle=0, halign=Gtk.Align.END)
        button5 = Gtk.Label(label="ADS Percentage Today: " + str(json_obj['ads_percentage_today']), angle=0, halign=Gtk.Align.END)
        #button6 = Gtk.Button(label="Button 6")

        grid.add(button1)
        grid.attach(button2, 1, 0, 2, 1)
        grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(button4, button3, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach(button5, 1, 2, 1, 1)
        #grid.attach_next_to(button5, Gtk.PositionType.RIGHT, 1, 1)

win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
