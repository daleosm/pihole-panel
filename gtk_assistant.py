import os
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Configuration variables of the app
config_directory = "~/.config"
config_filename = "gtk_assistant_configs.xml"
title = "GTK Assistant"


class AssistantApp:
    def __init__(self):
        self.assistant = Gtk.Assistant()
        self.assistant.set_default_size(-1, -1)

        self.create_config_dir(config_directory)

        self.create_preferences_page()
        self.create_about_page()

        if self.is_config_file_exist(config_directory, config_filename) is True:
            self.assistant.set_current_page(1)  # Don't display Preferences page at startup

        self.assistant.connect('cancel', self.on_close_cancel)
        self.assistant.connect('close', self.on_close_cancel)
        self.assistant.connect('apply', self.on_apply)
        self.assistant.connect('prepare', self.on_prepare)

        self.assistant.show()


    def create_config_dir(self, config_directory):
        if not os.path.exists(config_directory):
            os.makedirs(config_directory)

    def is_config_file_exist(self, config_directory, config_file):
        filename = config_directory + "/" + config_file
        return os.path.isfile(filename)

    def on_close_cancel(self, assistant):
        assistant.destroy()
        Gtk.main_quit()

    def on_apply(self, assistant):
        pass

    def on_prepare(self, assistant, page):
        current_page = assistant.get_current_page()
        n_pages = assistant.get_n_pages()
        title = 'GTK Assistant (%d of %d)' % (current_page + 1, n_pages)
        assistant.set_title(title)

    def save_configs(self, values_dict):
        pass


    def on_page_one_next(self, current_page, values_dict):
        self.save_configs(values_dict)
        next_page_index = 1
        return next_page_index


    def create_preferences_page(self):
        # Create IP Address box

        ip_address_box = Gtk.HBox(homogeneous=False, spacing=12)
        # ip_address_box.set_border_width(12)
        ip_address_label = Gtk.Label(label='IP Address: ')
        ip_address_box.pack_start(ip_address_label, False, False, 12)

        ip_address_entry = Gtk.Entry()
        ip_address_box.pack_start(ip_address_entry, False, False, 4)
        # ip_address_entry.connect('changed', self.on_entry_changed)

        # Create Key Code box

        key_code_box = Gtk.HBox(homogeneous=False, spacing=12)
        key_code_box.set_border_width(12)
        key_code_label = Gtk.Label(label='Key Code: ')
        key_code_box.pack_start(key_code_label, False, False, 12)

        key_code_entry = Gtk.Entry()
        key_code_box.pack_start(key_code_entry, False, False, 0)
        # key_code_entry.connect('changed', self.on_entry_changed)

        # Add above boxes to single box
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        page_box.pack_start(ip_address_box, False, False, 0)
        page_box.pack_start(key_code_box, False, False, 0)
        page_box.show_all()

        self.assistant.append_page(page_box)

        # Set other page properties
        self.assistant.set_page_title(page_box, 'Preferences')
        self.assistant.set_page_type(page_box, Gtk.AssistantPageType.INTRO)

        self.assistant.set_page_complete(page_box, True)

        pixbuf = self.assistant.render_icon(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG, None)

        self.assistant.set_page_header_image(page_box, pixbuf)

        # Get entered values
        values_dict = {}
        values_dict['ip_address'] = ip_address_entry.get_text()
        values_dict['key_code'] = key_code_entry.get_text()

        self.assistant.set_forward_page_func(self.on_page_one_next, values_dict)


    def on_edit_preferences_clicked(self, button):
        self.assistant.set_current_page(0)


    def create_about_page(self):
        label = Gtk.Label(label='Congratulations!')

        button = Gtk.Button.new_with_label("Edit Preferences")
        button.connect("clicked", self.on_edit_preferences_clicked)

        dummy_box_left = Gtk.VBox(spacing=6)
        dummy_box_right = Gtk.VBox(spacing=6)
        dummy_box_right.pack_start(button, False, False, 0)

        dummy_container_box = Gtk.HBox(spacing=6)
        dummy_container_box.pack_start(dummy_box_left, True, True, 0)
        dummy_container_box.pack_start(dummy_box_right, False, False, 0)

        page_box = Gtk.VBox(spacing=6)
        page_box.pack_start(label, True, True, 0)
        page_box.pack_start(dummy_container_box, False, False, 0)
        page_box.show_all()

        self.assistant.append_page(page_box)
        self.assistant.set_page_complete(page_box, True)
        self.assistant.set_page_title(page_box, 'About')
        self.assistant.set_page_type(page_box, Gtk.AssistantPageType.CONFIRM)

        pixbuf = self.assistant.render_icon(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG, None)
        self.assistant.set_page_header_image(page_box, pixbuf)



if __name__ == '__main__':
    AssistantApp()
    Gtk.main()
