import os
import sys
import pytest
import context

from context import devspell
PyParser = devspell.plugins.PyParser

def test_python_basic():
  """Test the basic operation of the Python parser"""

  content = """
  # This is a single comment
  def test():
    my_life = "This is my life"

  class Bob:
    def bob_life(self):
      print "Bob's life"
  """
  parser = PyParser("path", content)
  assert len(parser.lines.lines) == 9
  assert parser.sections.has_section("This is a single comment")
  assert parser.sections.has_section("This is my life")
  assert parser.sections.has_section("Bob's life")

def test_python_block_comment():
  """Test a python comment block"""

  content1 = '''
  """
  This is a multi-line
  comment, thanks
  """
  """This is a failure
  '''

  content2 = """
  '''
  This is a multi-line
  comment, thanks
  '''
  '''This is a failure
  """
  parser = PyParser("path", content1)
  assert len(parser.lines.lines) == 7
  assert parser.sections.has_section("This is a multi-line")
  assert parser.sections.has_section("comment, thanks")
  assert not parser.sections.has_section("This is a failure")

  parser = PyParser("path", content2)
  assert len(parser.lines.lines) == 7
  assert parser.sections.has_section("This is a multi-line")
  assert parser.sections.has_section("comment, thanks")
  assert not parser.sections.has_section("This is a failure")
