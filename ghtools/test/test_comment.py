#!/usr/bin/env python

"""Unit tests for Comment class
"""

import unittest
import datetime
from ghtools.comment import Comment, CommentType

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestComment(unittest.TestCase):
    """Tests of Comment class"""

    @staticmethod
    def _create_comment(content=None):
        """Returns a basic Comment object

        If content isn't specified, use some hard-coded content
        """
        if content is None:
            content = "My content"
        return Comment(comment_type=CommentType.PR_LINE_COMMENT,
                       username="me",
                       creation_date=datetime.datetime(2020, 1, 1),
                       url="https://github.com/org/repo/1#issuecomment-2",
                       content=content)

    def test_repr_resultsInEqualObject(self):
        """The repr of a Comment object should result in an equivalent object"""
        # This ability to recreate the object isn't a strict requirement, so if it gets
        # hard to maintain, we can drop it.
        c = self._create_comment()
        # pylint: disable=eval-used
        c2 = eval(repr(c))
        self.assertEqual(c2, c)

    def test_str_works(self):
        """Just make sure that the str method runs successfully"""
        c = self._create_comment()
        _ = str(c)

    def test_getTodos_emptyComment(self):
        """Test the get_todos method on an empty comment"""
        content = ""
        c = self._create_comment(content=content)
        todos = c.get_todos()
        self.assertEqual(len(todos), 0)

    def test_getTodos_none(self):
        """Test the get_todos method when there are no todos"""
        content = """\
Some
Content"""
        c = self._create_comment(content=content)
        todos = c.get_todos()
        self.assertEqual(len(todos), 0)

    def test_getTodos_one(self):
        """Test the get_todos method when there is one todo"""
        content = """\
Some
Content
- [ ] My task
with a task"""
        c = self._create_comment(content=content)
        todos = c.get_todos()
        self.assertEqual(len(todos), 1)
        self.assertEqual("My task", todos[0].get_text())

    def test_getTodos_oneSingleLine(self):
        """Test the get_todos method when there is one todo in a single-line comment"""
        content = "- [ ] This is a task"
        c = self._create_comment(content=content)
        todos = c.get_todos()
        self.assertEqual(len(todos), 1)
        self.assertEqual("This is a task", todos[0].get_text())

    def test_getTodos_multiple(self):
        """Test the get_todos method when there are multiple todos"""
        # In the following, there is a comment on the first line, the last line, and in
        # the middle, as well as a completed task that should NOT be picked up.
        content = """\
- [ ] Task 1
Some text
- [ ] Task 2
More text
- [x] Completed task
More text
- [ ] Task 3"""
        c = self._create_comment(content=content)
        todos = c.get_todos()
        self.assertEqual(len(todos), 3)
        self.assertEqual("Task 1", todos[0].get_text())
        self.assertEqual("Task 2", todos[1].get_text())
        self.assertEqual("Task 3", todos[2].get_text())

if __name__ == '__main__':
    unittest.main()
