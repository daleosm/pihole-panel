# If you have UTF-8 problems then uncomment next 3 lines
#import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

# HELP: https://discourse.pi-hole.net/t/pi-hole-api/1863
# HELP: https://github.com/pi-hole/AdminLTE/issues/575
# HELP: https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html


import json
from urllib.request import urlopen
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

# AssistantApp window class
from gtk_assistant import AssistantApp
wc = AssistantApp()

# Configuration variables of the app
config_directory = str(Path.home()) + "/.config"
config_filename = "gtk_assistant_configs.xml"


class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="PiHole Panel")

        grid = Gtk.Grid(margin=4)
        grid.set_column_homogeneous(True)
        self.add(grid)

        self.grid = grid

        # Create the various elements of the window
        self.status_label, self.status_button = self.draw_status_elements()
        self.statistics_frame = self.draw_statistics_frame()
        self.top_queries_frame = self.draw_top_queries_frame()
        self.top_ads_frame = self.draw_top_ads_frame()

        self.fetch_data_and_update_display()    # Initial data fetch-and-display

        # Create a timer --> self.on_timer will be called periodically
        GObject.timeout_add_seconds(update_interval_seconds, self.on_timer)

    # This function is called periodically

    def on_timer(self):
        self.fetch_data_and_update_display()
        return True

    # Fetch required data from the Pi-Hole API, and update the window elements using responses received

    def fetch_data_and_update_display(self):
        # Fetch data
        status, statistics_dict = self.get_status_and_statistics(base_url)
        readable_statistics_dict = make_dictionary_keys_readable(
            statistics_dict)
        top_queries_dict, top_ads_dict = self.get_top_items(
            base_url, web_password)

        # Update frames
        self.update_status_elements(status)
        self.update_statistics_frame(readable_statistics_dict)
        self.update_top_queries_frame(top_queries_dict)
        self.update_top_ads_frame(top_ads_dict)

    # Following 4 functions draw the elements of the window (labels, buttons and 3 frames for statistics, top queries and top ads)

    def draw_status_elements(self):
        button1 = Gtk.Switch(halign=Gtk.Align.CENTER)
        button1.connect("notify::active", self.on_status_switch_activated)

        status_label = Gtk.Label(halign=Gtk.Align.END)
        status_label.set_markup("<b>%s</b>" % 'Status:')

        box = Gtk.Box(spacing=3)
        box.pack_start(status_label, True, True, 4)
        box.pack_start(button1, True, True, 4)

        # To add space between elements
        empty_label_1 = Gtk.Label(label='', margin=1)
        self.grid.attach(empty_label_1, 2, 1, 1, 1)

        self.grid.attach(box, 2, 2, 1, 1)

        # To add space between elements
        empty_label_2 = Gtk.Label(label='', margin=1)
        self.grid.attach(empty_label_2, 2, 3, 1, 1)

        return status_label, button1

    def draw_statistics_frame(self):
        frame_vert = Gtk.Frame(label='Statistics')
        frame_vert.set_border_width(10)
        frame_vert.table_box = None

        self.grid.attach(frame_vert, 0, 4, 1, 1)
        return frame_vert

    def draw_top_queries_frame(self):
        frame_vert = Gtk.Frame(label='Top Queries')
        frame_vert.set_border_width(10)
        frame_vert.table_box = None

        self.grid.attach(frame_vert, 1, 4, 1, 1)
        return frame_vert

    def draw_top_ads_frame(self):
        frame_vert = Gtk.Frame(label='Top Ads')
        frame_vert.set_border_width(10)
        frame_vert.table_box = None

        self.grid.attach(frame_vert, 2, 4, 1, 1)
        return frame_vert

    # Following 4 functions updates the values of window elements with given (fetched) values

    def update_status_elements(self, status):
        # Activate/ deactivate the button so that it reflects the actual current status
        if status == "enabled":
            self.status_button.set_active(True)
        else:
            self.status_button.set_active(False)

        # Update the status label
        self.status_label.set_markup("<b>Status:</b> " + status)

    def update_statistics_frame(self, statistics_dict):
        if self.statistics_frame.table_box:
            # Destroy and remove current data table box
            self.statistics_frame.table_box.destroy()

        # Create new data table box with given values
        table_box = self.create_table_box(
            "Statistic", "Value", statistics_dict)
        # Save so that it can be destroyed later
        self.statistics_frame.table_box = table_box
        self.statistics_frame.add(table_box)

        table_box.show_all()    # Show the new data table box

    def update_top_queries_frame(self, top_queries_dict):
        if self.top_queries_frame.table_box:
            self.top_queries_frame.table_box.destroy()

        if top_queries_dict:
            table_box = self.create_table_box(
                "Domain", "Hits", top_queries_dict)
            # Save so that it can be destroyed later
            self.top_queries_frame.table_box = table_box
            self.top_queries_frame.add(table_box)
            table_box.show_all()

    def update_top_ads_frame(self, top_ads_dict):
        if self.top_ads_frame.table_box:
            self.top_ads_frame.table_box.destroy()

        if top_ads_dict:
            table_box = self.create_table_box("Domain", "Hits", top_ads_dict)
            # Save so that it can be destroyed later
            self.top_ads_frame.table_box = table_box
            self.top_ads_frame.add(table_box)
            table_box.show_all()

    # Following 3 functions send requests to Pi-Hole API and return the response received

    def get_status_and_statistics(self, base_url):
        url = base_url + "api.php?summary"
        result = urlopen(url, timeout=15).read()
        json_obj = json.loads(result)
        # print(json_obj)

        status = str(json_obj['status'])
        del json_obj['status']  # we only want the statistics

        return status, json_obj

    def get_top_items(self, base_url, web_password):
        url = base_url + "api.php?topItems&auth=" + web_password
        results = urlopen(url, timeout=15).read()
        json_obj = json.loads(results)
        # print(json_obj)

        top_queries_dict = json_obj['top_queries']
        top_ads_dict = json_obj['top_ads']

        return top_queries_dict, top_ads_dict

    def draw_top_ads(self, grid, top_ads_dict):
        # Frame to contain the wrapper box
        frame_vert = Gtk.Frame(label='Top Ads')
        frame_vert.set_border_width(10)

        if top_ads_dict:
            table_box = self.create_table_box("Domain", "Hits", top_ads_dict)
            frame_vert.add(table_box)

        grid.attach(frame_vert, 2, 4, 1, 1)

    # Function that runs when the status button is clicked

    def on_status_switch_activated(self, switch, gparam):
        if switch.get_active():
            status = self.send_enable_request()
        else:
            status = self.send_disable_request()

        self.update_status_elements(status)

    # Following 2 functions sends requests to Pi-Hole API to enable/ disable it

    def send_enable_request(self):
        url = base_url + "api.php?enable&auth=" + web_password
        results = urlopen(url, timeout=15).read()
        json_obj = json.loads(results)
        # print(json_obj)
        return json_obj['status']

    def send_disable_request(self):
        url = base_url + "api.php?disable&auth=" + web_password
        results = urlopen(url, timeout=15).read()
        json_obj = json.loads(results)
        # print(json_obj)
        return json_obj['status']

    # This function creates a box that contains data in the 'items_dict' arranged as a 2-column table

    def create_table_box(self, left_heading, right_heading, items_dict):
        # First column box
        first_column_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=0)
        first_col_heading_label = Gtk.Label(margin=4, halign=Gtk.Align.START)
        first_col_heading_label.set_markup(
            '<u>' + left_heading + '</u>')   # Column heading label
        first_column_box.pack_start(first_col_heading_label, False, False, 4)

        # Second column box
        second_column_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=0)
        second_col_label = Gtk.Label(margin=4, halign=Gtk.Align.END)
        second_col_label.set_markup(
            '<u>' + right_heading + '</u>')  # Column heading label
        second_column_box.pack_start(second_col_label, False, False, 4)

        # Add rows to the two two columns
        for first, second in items_dict.items():
            first_col_label = Gtk.Label(
                label=str(first), margin=4, halign=Gtk.Align.START)
            first_column_box.pack_start(first_col_label, False, False, 0)

            second_col_label = Gtk.Label(
                label=str(second), margin=4, halign=Gtk.Align.END)
            second_column_box.pack_start(second_col_label, False, False, 0)

        # Include the two boxes in one wrapper box (table box)
        table_box = Gtk.Box(spacing=8)
        table_box.pack_start(first_column_box, True, True, 0)
        table_box.pack_start(second_column_box, True, True, 0)

        return table_box


# This function makes the keys in the dictionary human-readable
def make_dictionary_keys_readable(dict):
    new_dict = {}
    for key, val in dict.items():
        # Replace underscores with spaces and convert to Title Case
        new_key = key.replace('_', ' ').title()
        new_dict[new_key] = val
        # print('{} --> {}'.format(key, new_key))

    return new_dict


if wc.is_config_file_exist(config_directory, config_filename) == True:
    configs = wc.load_configs(config_directory, config_filename)

    base_url = configs['ip_address']
    web_password = configs['key_code']

    update_interval_seconds = 3  # Time interval between updates

    win = GridWindow()
    win.set_icon_from_file("pihole-panel.png")
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

Gtk.main()
