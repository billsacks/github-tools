#!/usr/bin/env python

"""Unit tests for the comment_todo module
"""

import unittest
from ghtools.comment_todo import search_line_for_todo

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestCommentTodo(unittest.TestCase):
    """Tests of comment_todo module"""

    # ------------------------------------------------------------------------
    # Tests of search_line_for_todo: searches expected to find something
    # ------------------------------------------------------------------------

    def test_search_uldash(self):
        """Make sure we find a todo like '- [ ] todo'"""
        result = search_line_for_todo("- [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_ulplus(self):
        """Make sure we find a todo like '+ [ ] todo'"""
        result = search_line_for_todo("+ [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_ulstar(self):
        """Make sure we find a todo like '* [ ] todo'"""
        result = search_line_for_todo("* [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_ulMultipleSpaces(self):
        """Make sure we find a todo with multiple spaces after the unordered list indicator"""
        result = search_line_for_todo("-   [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_oldot(self):
        """Make sure we find a todo like '1. [ ] todo'"""
        result = search_line_for_todo("1. [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_olparen(self):
        """Make sure we find a todo like '1) [ ] todo'"""
        result = search_line_for_todo("1) [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_olMultipleDigits(self):
        """Make sure we find a todo with multiple digits in the list indicator"""
        result = search_line_for_todo("123. [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_olMultipleSpaces(self):
        """Make sure we find a todo with multiple spaces after the ordered list indicator"""
        result = search_line_for_todo("1.   [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_multipleSpacesAfterCheckbox(self):
        """Make sure we find a todo with multiple spaces after the checkbox"""
        result = search_line_for_todo("- [ ]   todo")
        self.assertEqual(result, "todo")

    def test_search_leadingSpaces(self):
        """Make sure we find a todo with leading spaces on the line"""
        result = search_line_for_todo("  - [ ] todo")
        self.assertEqual(result, "todo")

    # ------------------------------------------------------------------------
    # Tests of search_line_for_todo: searches NOT expected to find something
    # ------------------------------------------------------------------------

    def test_search_noWhitespaceAfterUL_fails(self):
        """If there is no whitespace after an unordered list marker, the search should fail"""
        result = search_line_for_todo("-[ ] todo")
        self.assertIsNone(result)

    def test_search_noWhitespaceAfterOL_fails(self):
        """If there is no whitespace after an ordered list marker, the search should fail"""
        result = search_line_for_todo("1.[ ] todo")
        self.assertIsNone(result)

    def test_search_noWhitespaceAfterCheckbox_fails(self):
        """If no whitespace between the checkbox and the following text, the search should fail"""
        result = search_line_for_todo("- [ ]todo")
        self.assertIsNone(result)

    def test_search_onlyWhitespaceAfterCheckbox_fails(self):
        """If there is only whitespace after the checkbox character, the search should fail"""
        result = search_line_for_todo("- [ ]  ")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()