# Application: PiHole-Panel
# Author: Dale Osm (https://github.com/daleosm/)
# GNU GENERAL PUBLIC LICENSE
# PIPELINE TEST
from pathlib import Path
from urllib.request import urlopen  # tidy
import xml.etree.ElementTree as ET
from gi.repository import Gtk, GLib, Gio
from gi.repository import GLib as glib
from gtk_assistant import AssistantApp

import urllib.request
import urllib.error

import json
import gi
import sys
import os
import hashlib


gi.require_version("Gtk", "3.0")


# AssistantApp window class

wc = AssistantApp()

# Configuration variables of the app

update_interval_seconds = 3  # Time interval between updates
version_number = "2.0"
config_directory = str(Path.home()) + "/.config"
config_filename = "pihole_panel_configs.xml"


class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="PiHole Panel")
        self.assistant = Gtk.Assistant()
        grid = Gtk.Grid(margin=4)
        grid.set_column_homogeneous(True)
        self.add(grid)

        self.grid = grid

        self.status_label, self.status_button = self.draw_status_elements()
        self.statistics_frame = self.draw_statistics_frame()
        self.top_queries_frame = self.draw_top_queries_frame()
        self.top_ads_frame = self.draw_top_ads_frame()
        self.updates_frame = self.draw_updates_frame()
        self.header_bar = self.draw_header_bar()
        self.hosts_combo = self.draw_hosts_combo()
        # Initial data fetch-and-display
        self.fetch_data_and_update_display(
            "http://pi.hole/admin/", web_password)

        # Create a timer --> self.on_timer will be called periodically

        glib.timeout_add_seconds(update_interval_seconds, self.on_timer)

    def on_timer(self):
        # This function is called periodically
        print("Timer running...")

        index = hosts_combo.get_active()
        model = hosts_combo.get_model()
        item = model[index]

        try:
            urllib.request.urlopen(item[1], timeout=5).read()

        except urllib.error.URLError as e:
            dialog = Gtk.MessageDialog(self.assistant, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CANCEL, "Invalid combination of Pi Address and Password")

            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.set_position(Gtk.WindowPosition.CENTER)
            dialog.run()
            restart_program()
            return False

        except urllib.error.HTTPError as e:
            dialog = Gtk.MessageDialog(self.assistant, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CANCEL, "Invalid combination of Pi Address and Password")

            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.set_position(Gtk.WindowPosition.CENTER)
            dialog.run()
            restart_program()
            return False

        else:
            # Decide what host id has been selected
            if item[0] == 1:
                self.fetch_data_and_update_display(base_url, web_password)
            if item[0] == 2:
                self.fetch_data_and_update_display(
                    configs["two_ip_address"], configs["two_key_code"])

            return True

    def version_check(self):
        # Fetch version number from GitHub repo

        get_version = urlopen(
            "https://raw.githubusercontent.com/daleosm/PiHole-Panel/master/VERSION").read()
        version_decoded = get_version.decode("utf-8")
        latest_version = version_decoded.strip("\n")

        if latest_version > version_number:
            return True
        else:
            return False

    def fetch_data_and_update_display(self, host_url, web_password):
        # Fetch required data from the Pi-Hole API, and update the window elements using responses received

        # Fetch data

        status, statistics_dict = self.get_status_and_statistics(host_url)
        readable_statistics_dict = make_dictionary_keys_readable(
            statistics_dict)
        top_queries_dict, top_ads_dict = self.get_top_items(
            host_url, web_password)

        # Update frames

        self.update_status_elements(status)
        self.update_statistics_frame(readable_statistics_dict)
        self.update_top_queries_frame(top_queries_dict)
        self.update_top_ads_frame(top_ads_dict)

    # Following 6 functions draw the elements of the window (labels, combobox, buttons and 3 frames for statistics, top queries and top ads)

    def draw_status_elements(self):
        button1 = Gtk.Switch(halign=Gtk.Align.CENTER)
        button1.connect("notify::active", self.on_status_switch_activated)

        status_label = Gtk.Label(halign=Gtk.Align.END)
        status_label.set_markup("<b>%s</b>" % "Status:")

        box = Gtk.Box(spacing=3)
        box.pack_start(status_label, True, True, 4)
        box.pack_start(button1, True, True, 4)

        # To add space between elements

        empty_label_1 = Gtk.Label(label="", margin=1)
        self.grid.attach(empty_label_1, 2, 1, 1, 1)
        self.grid.attach(box, 2, 2, 1, 1)

        # To add space between elements

        empty_label_2 = Gtk.Label(label="", margin=1)
        self.grid.attach(empty_label_2, 2, 3, 1, 1)

        return status_label, button1

    def open_sub_window(self, button):
        self.popup = Gtk.Window()
        self.popup.set_title("Settings")
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.popup.add(page_box)
        self.popup.set_size_request(100, 250)

        # Create IP Address box

        ip_address_box = Gtk.HBox(homogeneous=False, spacing=12)

        ip_address_label = Gtk.Label(label="Pi Address:                ")
        ip_address_box.pack_start(ip_address_label, False, False, 6)

        ip_address_entry = Gtk.Entry()
        ip_address_entry.set_text(configs["ip_address"])
        ip_address_box.pack_start(ip_address_entry, False, False, 6)

        # Pack IP Address box
        page_box.pack_start(ip_address_box, False, False, 6)

        # Create key code box

        key_code_box = Gtk.HBox(homogeneous=False, spacing=12)

        key_code_label = Gtk.Label(label="Pi Password:             ")
        key_code_box.pack_start(key_code_label, False, False, 6)

        key_code_entry = Gtk.Entry()
        key_code_entry.set_text(configs["key_code"])
        key_code_box.pack_start(key_code_entry, False, False, 6)

        # Pack key code box
        page_box.pack_start(key_code_box, False, False, 6)

        # Create 2IP Address box
        two_ip_address_box = Gtk.HBox(homogeneous=False, spacing=12)

        ip_address_label = Gtk.Label(label="Two Pi Address:      ")
        two_ip_address_box.pack_start(ip_address_label, False, False, 6)

        two_ip_address_entry = Gtk.Entry()

        if "two_ip_address" in configs:
            if configs["two_ip_address"] is not None:
                two_ip_address_entry.set_text(configs["two_ip_address"])

        two_ip_address_box.pack_start(two_ip_address_entry, False, False, 6)

        # Pack 2IP Address box
        page_box.pack_start(two_ip_address_box, False, False, 6)

        # Create key code box

        two_key_code_box = Gtk.HBox(homogeneous=False, spacing=6)

        two_key_code_label = Gtk.Label(label="Two Pi Password:     ")
        two_key_code_box.pack_start(two_key_code_label, False, False, 6)

        two_key_code_entry = Gtk.Entry()

        if "two_key_code" in configs:
            if configs["two_key_code"] is not None:
                two_key_code_entry.set_text(configs["two_key_code"])

        two_key_code_box.pack_start(two_key_code_entry, False, False, 6)

        # Pack key code box
        page_box.pack_start(two_key_code_box, False, False, 6)

        # Create save button box
        button_box = Gtk.HBox(homogeneous=False, spacing=12)
        button = Gtk.Button.new_with_label("Save")

        button.connect("clicked", self.on_settings_save,
                       ip_address_entry, key_code_entry, two_ip_address_entry, two_key_code_entry)
        button_box.pack_end(button, False, False, 4)

        # Pack save button box
        page_box.pack_start(button_box, False, False, 12)

        self.popup.show_all()

    def on_settings_save(self, button, ip_address_entry, key_code_entry, two_ip_address_entry, two_key_code_entry):

        # Make sure config has new entries
        if "two_ip_address" not in configs:
            configs["two_ip_address"] = ""
            wc.save_configs(config_directory, config_filename, configs)

        if "two_key_code" not in configs:
            configs["two_key_code"] = ""
            wc.save_configs(config_directory, config_filename, configs)

        configs["ip_address"] = ip_address_entry.get_text()
        configs["two_ip_address"] = two_ip_address_entry.get_text()
        configs2 = {}
        configs3 = {}

        if key_code_entry.get_text() != configs["key_code"]:
            configs2["key_code"] = key_code_entry.get_text()

            configs["key_code"] = hashlib.sha256(
                configs2["key_code"].encode("utf-8")).hexdigest()
            configs["key_code"] = hashlib.sha256(
                configs["key_code"].encode("utf-8")).hexdigest()

        if two_key_code_entry.get_text() != configs["two_key_code"]:
            configs3["two_key_code"] = two_key_code_entry.get_text()

            
            configs["two_key_code"] = hashlib.sha256(
                configs3["two_key_code"].encode("utf-8")).hexdigest()
            configs["two_key_code"] = hashlib.sha256(
                configs["two_key_code"].encode("utf-8")).hexdigest()

        # Check updated settings for Pi1
        url = configs["ip_address"] + "api.php?topItems&auth=" + configs["key_code"]

        try: 
            urllib.request.urlopen(url, timeout=15).read()

        except urllib.error.URLError as e:
            dialog = Gtk.MessageDialog(self.assistant, 0, Gtk.MessageType.ERROR,
                                    Gtk.ButtonsType.CANCEL, "Invalid combination of Pi Address and Password")

            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.set_position(Gtk.WindowPosition.CENTER)
            dialog.run()
                
            

        except urllib.error.HTTPError as e:
            dialog = Gtk.MessageDialog(self.assistant, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CANCEL, "Invalid combination of Pi Address and Password")

            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.set_position(Gtk.WindowPosition.CENTER)
            dialog.run()

        results = urllib.request.urlopen(url, timeout=15).read()
        json_obj = json.loads(results)
           
        if "top_queries" not in json_obj:
            dialog = Gtk.MessageDialog(self.assistant, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL, "Invalid combination of Pi Address and Password")

            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.set_position(Gtk.WindowPosition.CENTER)
            dialog.run()

        # Check updated settings for Pi2
        if two_ip_address_entry.get_text():
            url = configs["two_ip_address"] + "api.php?topItems&auth=" + configs["two_key_code"]

            try: 
                urllib.request.urlopen(url, timeout=15).read()

            except urllib.error.URLError as e:
                dialog = Gtk.MessageDialog(self.assistant, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CANCEL, "Invalid combination of Pi Address and Password")

                dialog.connect("response", lambda *a: dialog.destroy())
                dialog.set_position(Gtk.WindowPosition.CENTER)
                dialog.run()
                
            

            except urllib.error.HTTPError as e:
                dialog = Gtk.MessageDialog(self.assistant, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CANCEL, "Invalid combination of Pi Address and Password")

                dialog.connect("response", lambda *a: dialog.destroy())
                dialog.set_position(Gtk.WindowPosition.CENTER)
                dialog.run()
                

            results = urllib.request.urlopen(url, timeout=15).read()
            json_obj = json.loads(results)
            
            if "top_queries" not in json_obj:
                    dialog = Gtk.MessageDialog(self.assistant, 0, Gtk.MessageType.ERROR,
                        Gtk.ButtonsType.CANCEL, "Invalid combination of Pi Address and Password")

                    dialog.connect("response", lambda *a: dialog.destroy())
                    dialog.set_position(Gtk.WindowPosition.CENTER)
                    dialog.run()
        else:
            if configs["two_ip_address"] == "":
                configs["two_key_code"] = None

        result = wc.validate_configs(configs)

        if result:
            wc.save_configs(config_directory, config_filename, configs)

            restart_program()

    def draw_header_bar(self):

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)

        button.connect("clicked", self.open_sub_window)

        return button

    def draw_hosts_combo(self):

        name_store = Gtk.ListStore(int, str)
        name_store.append([1, configs["ip_address"]])

        if "two_ip_address" in configs:
            if configs["two_ip_address"] != None:
                name_store.append([2, configs["two_ip_address"]])

        global hosts_combo

        hosts_combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
        hosts_combo.set_entry_text_column(1)
        hosts_combo.set_active(0)

        hosts_combo.connect("changed", self.on_hosts_combo_changed)

        self.grid.attach(hosts_combo, 1, 2, 1, 1)
        return hosts_combo

    def draw_statistics_frame(self):
        frame_vert = Gtk.Frame(label="Statistics")
        frame_vert.set_border_width(10)
        frame_vert.table_box = None

        self.grid.attach(frame_vert, 0, 4, 1, 1)
        return frame_vert

    def draw_top_queries_frame(self):
        frame_vert = Gtk.Frame(label="Top Queries")
        frame_vert.set_border_width(10)
        frame_vert.table_box = None

        self.grid.attach(frame_vert, 1, 4, 1, 1)
        return frame_vert

    def draw_top_ads_frame(self):
        frame_vert = Gtk.Frame(label="Top Ads")
        frame_vert.set_border_width(10)
        frame_vert.table_box = None

        self.grid.attach(frame_vert, 2, 4, 1, 1)
        return frame_vert

    def draw_updates_frame(self):

        if self.version_check() == True:
            label = Gtk.Label()
            label.set_markup("There is a new version <a href=\"https://github.com/daleosm/PiHole-Panel\" "
                             "title=\"Click to find out more\">update available</a>.")
            label.set_line_wrap(True)
            label.set_justify(Gtk.Justification.FILL)

            self.grid.attach(label, 2, 5, 1, 1)
            return label

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

        status = str(json_obj["status"])
        del json_obj["status"]  # We only want the statistics

        if "gravity_last_updated" in json_obj:
            del json_obj["gravity_last_updated"]  # This needs more work

        if "dns_queries_all_types" in json_obj:
            del json_obj["dns_queries_all_types"]  # Useless

        if "reply_NODATA" in json_obj:
            del json_obj["reply_NODATA"]  # Useless

        if "reply_NXDOMAIN" in json_obj:
            del json_obj["reply_NXDOMAIN"]  # Useless

        if "reply_CNAME" in json_obj:
            del json_obj["reply_CNAME"]  # Useless

        if "reply_IP" in json_obj:
            del json_obj["reply_IP"]  # Useless

        return status, json_obj

    def get_top_items(self, base_url, web_password):
        url = base_url + "api.php?topItems&auth=" + web_password
        results = urlopen(url, timeout=15).read()
        json_obj = json.loads(results)

        top_queries_dict = json_obj["top_queries"]
        top_ads_dict = json_obj["top_ads"]

        return top_queries_dict, top_ads_dict

    def draw_top_ads(self, grid, top_ads_dict):

        # Frame to contain the wrapper box

        frame_vert = Gtk.Frame(label="Top Ads")
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
        return json_obj["status"]

    def send_disable_request(self):
        url = base_url + "api.php?disable&auth=" + web_password
        results = urlopen(url, timeout=15).read()
        json_obj = json.loads(results)
        return json_obj["status"]

    # This function creates a box that contains data in the "items_dict" arranged as a 2-column table

    def create_table_box(self, left_heading, right_heading, items_dict):

        # First column box

        first_column_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=0)
        first_col_heading_label = Gtk.Label(margin=4, halign=Gtk.Align.START)
        first_col_heading_label.set_markup(
            "<u>" + left_heading + "</u>")   # Column heading label
        first_column_box.pack_start(first_col_heading_label, False, False, 4)

        # Second column box

        second_column_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=0)
        second_col_label = Gtk.Label(margin=4, halign=Gtk.Align.END)
        second_col_label.set_markup(
            "<u>" + right_heading + "</u>")  # Column heading label
        second_column_box.pack_start(second_col_label, False, False, 4)

        # Add rows to the two two columns

        for first, second in items_dict.items():
            info = (first[:36] + "..") if len(first) > 36 else first
            first_col_label = Gtk.Label(
                label=str(info), margin=4, halign=Gtk.Align.START)
            first_column_box.pack_start(first_col_label, False, False, 0)

            second_col_label = Gtk.Label(
                label=str(second), margin=4, halign=Gtk.Align.END)
            second_column_box.pack_start(second_col_label, False, False, 0)

        # Include the two boxes in one wrapper box (table box)

        table_box = Gtk.Box(spacing=8)
        table_box.pack_start(first_column_box, True, True, 0)
        table_box.pack_start(second_column_box, True, True, 0)

        return table_box

    def on_hosts_combo_changed(self, combo):
        text = combo.get_active()
        index = combo.get_active()
        model = combo.get_model()
        item = model[index]

        if text is not None:
            print("Selected: host=%s" % item[1])


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

# This function makes the keys in the dictionary human-readable


def make_dictionary_keys_readable(dict):
    new_dict = {}
    for key, val in dict.items():
        # Replace underscores with spaces and convert to Title Case
        new_key = key.replace("_", " ").title()
        new_dict[new_key] = val
        # print("{} --> {}".format(key, new_key))

    return new_dict


if wc.is_config_file_exist(config_directory, config_filename) == True:
    configs = wc.load_configs(config_directory, config_filename)

    base_url = configs["ip_address"]
    web_password = configs["key_code"]
    wc.validate_configs(configs)
    win = GridWindow()
    win.set_icon_from_file("/usr/lib/pihole-panel/pihole-panel.png")
    win.connect("destroy", Gtk.main_quit)
    win.set_wmclass("PiHole Panel", "PiHole Panel")
    win.set_title("PiHole Panel")
    win.set_position(Gtk.WindowPosition.CENTER)
    win.show_all()

Gtk.main()
