# encoding: utf-8
"""Module that will hold the code for processing text."""
from knuth_moriss_pratt import knp_iterator


PATTERN_LIST = [u'.', u'?', u'!', u',', u';', u':', u'...', u'(', u')', u' − ', u' - ', u'„', u'“', u'’',
                u'‘', u'/', u'*', u' ', u'−', u'–', u'¹', u'²', u'³', u'⁴', u'⁵', u'⁶', u'⁷',
                u'⁸', u'\u2079', u'⁰', u'=', u'+', u'-', u'\u00D7', u'>', u'<', u'\u2264',
                u'\u2265', u'%', u'\u00B0', u'~', u'§', u'@']


WORD_TOKEN = u'_'


class ProcessText(object):
    """Process text by removing characters."""

    def __init__(self, text, pattern_list, word_token):
        """
        Initialize ProcessText.

        :param text: The text to be processed.
        :type text: unicode
        """
        super(ProcessText, self).__init__()

        self.text = text
        self.pattern_list = pattern_list
        self.word_token = word_token
        self.matches = []

    def process(self):
        """Process the text."""
        text_lines = self.text.split(u'\n')

        for line_index in range(len(text_lines)):
            matches = MatchWarehouse()
            for pattern in self.pattern_list:
                for start_index in knp_iterator(text_lines[line_index], pattern):
                    matches.add_match(Match(start_index, start_index + len(pattern), pattern))

            new_list_text = []
            chars_to_delete = 0
            list_text = list(text_lines[line_index])
            for index in range(len(list_text)):
                if not matches.in_range(index):
                    chars_to_delete += 1
                else:
                    if chars_to_delete > 0:
                        chars_to_delete = 0
                        new_list_text.append(self.word_token)

                    new_list_text.append(list_text[index])

            if chars_to_delete > 0:
                new_list_text.append(self.word_token)

            text_lines[line_index] = ''.join(new_list_text)

        return '\n'.join(text_lines)


class MatchWarehouse(object):
    """A warehouse of match objects."""

    def __init__(self, matches=None):
        """Initialize a warehouse of match objects."""
        super(MatchWarehouse, self).__init__()

        if matches is None:
            matches = []

        self.matches = matches

    def add_match(self, match):
        """Add match to the warehouse."""
        self.matches.append(match)

    def in_range(self, index):
        """Check if index is in range."""
        for match in self.matches:
            if match.start_pos <= index < match.end_pos:
                return True

        return False


class Match(object):
    """A match class."""

    def __init__(self, start_pos, end_pos, pattern):
        """Initialize Match."""
        super(Match, self).__init__()

        self.start_pos = start_pos
        self.end_pos = end_pos
        self.pattern = pattern

    def __repr__(self):
        """Override __repr__ method."""
        return '<Match (start_pos={0}, end_pos={1}, pattern="{2}")>'.format(self.start_pos, self.end_pos,
                                                                            self.pattern)
