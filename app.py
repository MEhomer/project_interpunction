"""Interpunction Application."""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty
from kivy.factory import Factory


import process_text


class TextHandler(BoxLayout):
    """View for parsing the text."""

    text_input = ObjectProperty()

    def process_text(self, pattern_list):
        """`on_press` handler for button."""
        text = self.text_input.text
        processor = process_text.ProcessText(text, pattern_list)

        self.text_input.text = processor.process()


class EditInterpunctionHandler(BoxLayout):
    """View for editing interpunction signs."""

    pass


class InterpunctionButton(ListItemButton):
    """Interpunction button."""

    interpunction_sign = ListProperty()


class MainMenu(BoxLayout):
    """Main menu for the application."""

    pattern_list = ObjectProperty()
    text_input = ObjectProperty()

    def __init__(self, **kwargs):
        """Initalize the main menu."""
        super(MainMenu, self).__init__(**kwargs)

        self.pattern_list = process_text.PATTERN_LIST
        self.selected_interpunction_sign = None

    def change_interpunction(self):
        """`on_press` handler for button."""
        self.clear_widgets()

        edit_interpunction_handler = Factory.EditInterpunctionHandler()

        del edit_interpunction_handler.interpunction_signs.adapter.data[:]
        edit_interpunction_handler.interpunction_signs.adapter.data.extend(self.pattern_list)

        self.add_widget(edit_interpunction_handler)

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

            self.change_interpunction()

    def add_interpunction_sing(self, text):
        """`on_press` handler for adding interpunction sign button is pressed."""
        self.pattern_list.insert(0, text)

        self.change_interpunction()

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
