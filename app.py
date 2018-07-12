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
        Gtk.Window.__init__(self, title="PiHole-Panel")

        print (json_obj)
        print(json_obj['ads_blocked_today'])

        grid = Gtk.Grid(margin=10)
        grid.set_column_homogeneous(True)
        self.add(grid)

        frame_vert = Gtk.Frame(label='Stats', halign=Gtk.Align.FILL)

        button1 = Gtk.Switch()
        #button1.connect("notify::active", self.on_switch_activated)
        #button1.set_active(True)

        box = Gtk.Box(spacing=8)


        stats = Gtk.Label(label="Blocked Today: " + str(json_obj['ads_blocked_today']) + "\n" +
        "Ads Percentage Today: " + str(json_obj['ads_percentage_today']) + "%\n"
        "DNS Queries Today: " + str(json_obj['dns_queries_today']) + "\n"
        "Unique Domains: " + str(json_obj['unique_domains']) + "\n"
        "Queries Forwarded: " + str(json_obj['queries_forwarded']) + "\n"
        "Queries Cached: " + str(json_obj['queries_cached']) + "\n"
        "Clients Ever Seen: " + str(json_obj['clients_ever_seen']) + "\n"
        "Unique Clients: " + str(json_obj['unique_clients']) + "\n"
        "Status: " + str(json_obj['status']), margin=4, halign=Gtk.Align.START)

        box.pack_start(stats, True, True, 0)

        frame_vert.add(box)

        grid.attach(button1, 4, 1, 1, 1)
        grid.attach(frame_vert, 1, 2, 4, 1)


win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
