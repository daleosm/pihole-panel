import gi
import json
from urllib.request import urlopen

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# If you have UTF-8 problems then uncomment next 3 lines
#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

# HELP: https://discourse.pi-hole.net/t/pi-hole-api/1863
# HELP: https://github.com/pi-hole/AdminLTE/issues/575
# HELP: https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html

# Change to Your Pi-Hole Admin Console Url
# base_url = "http://pi.hole/admin/"
base_url = "http://0.0.0.0/admin/"
# Change to Your Pi-Hole Admin Console Hashed Password (see WEBPASSWORD in /etc/base_url/setupVars.conf)
web_password = "47ed9ce211732629cc190f09a6d6f427b3b35e9b8f3b1c0b9a8a552021a4e95f"



class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="PiHole-Panel")

        grid = Gtk.Grid(margin=4)
        grid.set_column_homogeneous(True)
        self.add(grid)

        self.status_label = None

        status, statistics = self.get_status_and_statistics(base_url)
        self.draw_status_elements(grid, status)
        self.draw_statistics_frame(grid, statistics)

        top_queries_dict, top_ads_dict = self.get_top_items(base_url, web_password)
        self.draw_top_queries(grid, top_queries_dict)
        self.draw_top_ads(grid, top_ads_dict)


    def get_status_and_statistics(self, base_url):
        url = base_url + "api.php?summary"
        result = urlopen(url, timeout=15).read()
        json_obj = json.loads(result)
        print(json_obj)

        status = str(json_obj['status'])

        statistics = "Blocked Today: " + str(json_obj['ads_blocked_today']) + "\n" + \
                    "Ads Percentage Today: " + str(json_obj['ads_percentage_today']) + "%\n" \
                    "DNS Queries Today: " + str(json_obj['dns_queries_today']) + "\n" \
                    "Unique Domains: " + str(json_obj['unique_domains']) + "\n" \
                    "Queries Forwarded: " + str(json_obj['queries_forwarded']) + "\n" \
                    "Queries Cached: " + str(json_obj['queries_cached']) + "\n" \
                    "Clients Ever Seen: " + str(json_obj['clients_ever_seen']) + "\n" \
                    "Unique Clients: " + str(json_obj['unique_clients'])

        return status, statistics


    def draw_status_elements(self, grid, status):
        button1 = Gtk.Switch(halign=Gtk.Align.END)
        if status == "enabled":
            button1.set_active(True)

        button1.connect("notify::active", self.on_status_switch_activated)

        status_label = Gtk.Label(label="Status: " + status, margin=4)

        grid.attach(status_label, 1, 1, 1, 1)
        grid.attach_next_to(button1, status_label, Gtk.PositionType.RIGHT, 1, 1)

        self.status_label = status_label


    def draw_statistics_frame(self, grid, statistics):
        stats_label = Gtk.Label(label=statistics, margin=4, halign=Gtk.Align.START)

        box = Gtk.Box(spacing=8)
        box.pack_start(stats_label, True, True, 0)

        frame_vert = Gtk.Frame(label='Stats')
        frame_vert.add(box)

        grid.attach(frame_vert, 0, 2, 3, 3)


    def get_top_items(self, base_url, web_password):
        url = base_url + "api.php?topItems&auth=" + web_password
        results = urlopen(url, timeout=15).read()
        json_obj = json.loads(results)
        print(json_obj)

        top_queries_dict = json_obj['top_queries']
        top_ads_dict = json_obj['top_ads']

        return top_queries_dict, top_ads_dict


    def draw_top_queries(self, grid, top_queries_dict):
        queries_str = dict_to_str(top_queries_dict)
        queries_label = Gtk.Label(label=queries_str, margin=4, halign=Gtk.Align.START)

        box = Gtk.Box(spacing=8)
        box.pack_start(queries_label, True, True, 0)

        frame_vert = Gtk.Frame(label='Top Queries')
        frame_vert.add(box)

        grid.attach(frame_vert, 0, 40, 3, 3)


    def draw_top_ads(self, grid, top_ads_dict):
        ads_str = dict_to_str(top_ads_dict)
        queries_label = Gtk.Label(label=ads_str, margin=4, halign=Gtk.Align.START)

        box = Gtk.Box(spacing=8)
        box.pack_start(queries_label, True, True, 0)

        frame_vert = Gtk.Frame(label='Top Ads')
        frame_vert.add(box)

        grid.attach(frame_vert, 0, 100, 3, 3)


    def on_status_switch_activated(self, switch, gparam):
        if switch.get_active():
            status = self.send_enable_request()
        else:
            status = self.send_disable_request()

        self.status_label.set_text("Status: " + status)

        # To ensure the actual status reflects the button state
        if status == "enabled":
            switch.set_active(True)
        else:
            switch.set_active(False)


    def send_enable_request(self):
        url = base_url + "api.php?enable&auth=" + web_password
        results = urlopen(url, timeout=15).read()
        json_obj = json.loads(results)
        print(json_obj)
        return json_obj['status']


    def send_disable_request(self):
        url = base_url + "api.php?disable&auth=" + web_password
        results = urlopen(url, timeout=15).read()
        json_obj = json.loads(results)
        print(json_obj)
        return json_obj['status']


def dict_to_str(top_queries_dict):
    string = ''
    for key, val in top_queries_dict.items():
        string = string + str(key) + ": " + str(val) + "\n"
    return string


win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
