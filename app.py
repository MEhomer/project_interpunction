"""Interpunction Application."""
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty
from kivy.factory import Factory
from kivy import Config

import process_text


Config.set('graphics', 'multisamples', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class TextHandler(BoxLayout):
    """View for parsing the text."""

    text_input = ObjectProperty()

    def process_text(self, pattern_list, word_token):
        """`on_press` handler for button."""
        text = self.text_input.text
        processor = process_text.ProcessText(text, pattern_list, word_token)

        self.text_input.text = processor.process()


class ConfigurationHandler(BoxLayout):
    """View for editing interpunction signs."""

    pass


class InterpunctionButton(ListItemButton):
    """Interpunction button."""

    interpunction_sign = ListProperty()


class CopyPastePopup(Popup):
    """Copy Paste Popup."""

    def __init__(self, text_input, **kwargs):
        """Initialize the CopyPastePopup."""
        super(CopyPastePopup, self).__init__(**kwargs)

        self.text_input = text_input

    def copy_press(self):
        """Event when the copy button is pressed."""
        print self.text_input.selection_text
        self.text_input.copy(data=self.text_input.selection_text)

        self.dismiss()

    def paste_press(self):
        """Event when the paste button is pressed."""
        self.text_input.paste()

        self.dismiss()


class RightClickFunctionalityTextBox(TextInput):
    """Special text input for handling mouse right click."""

    def on_touch_down(self, touch):
        """On touch down event for every text input."""
        if touch.button == 'right':
            popup = CopyPastePopup(self)
            popup.open()
        else:
            super(RightClickFunctionalityTextBox, self).on_touch_down(touch)


class MainMenu(BoxLayout):
    """Main menu for the application."""

    pattern_list = ObjectProperty()
    text_input = ObjectProperty()

    def __init__(self, **kwargs):
        """Initalize the main menu."""
        super(MainMenu, self).__init__(**kwargs)

        self.pattern_list = process_text.PATTERN_LIST
        self.word_token = process_text.WORD_TOKEN
        self.selected_interpunction_sign = None

    def change_configuration(self):
        """`on_press` handler for button."""
        self.clear_widgets()

        configuration_handler = Factory.ConfigurationHandler()

        del configuration_handler.interpunction_signs.adapter.data[:]
        configuration_handler.interpunction_signs.adapter.data.extend(self.pattern_list)
        configuration_handler.text_box.text = self.word_token

        self.add_widget(configuration_handler)

    def change_word_token(self, word_token):
        """`on_press` handler for changing word token."""
        self.word_token = word_token

        self.change_configuration()

    def open_text_handler(self):
        """`on_press` handler for button."""
        self.clear_widgets()

        self.add_widget(Factory.TextHandler())

    def select_interpunction_sign(self, interpunction_sign):
        """`on_press` handler when interpunction sign is pressed."""
        if self.selected_interpunction_sign is None:
            self.selected_interpunction_sign = interpunction_sign
        elif self.selected_interpunction_sign[0] == interpunction_sign[0]:
            self.selected_interpunction_sign = None
        else:
            self.selected_interpunction_sign = interpunction_sign

    def delete_interpunction_sing(self):
        """`on_press` handler when delete interpunction sign button is pressed."""
        if self.selected_interpunction_sign is not None and \
                len(self.pattern_list) > self.selected_interpunction_sign[0]:
            del self.pattern_list[self.selected_interpunction_sign[0]]
            self.selected_interpunction_sign = None

            self.change_configuration()

    def add_interpunction_sing(self, text):
        """`on_press` handler for adding interpunction sign button is pressed."""
        self.pattern_list.insert(0, text)

        self.change_configuration()

    def args_converter(self, index, data_item):
        """Convert the data that it is coming in the ListViewAdapter."""
        interpunction_sign = data_item

        return {'interpunction_sign': (index, interpunction_sign)}


class InterpunctionApp(App):
    """Interpunction Application."""

    pass


def main():
    """Main entry."""
    InterpunctionApp().run()


if __name__ == '__main__':
    main()
