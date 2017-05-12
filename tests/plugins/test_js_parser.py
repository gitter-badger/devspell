import os
import sys
import pytest
import context

from context import devspell
JSParser = devspell.plugins.JSParser

def test_js_basic():
  """Test the basic operation of the JS parser"""

  content = """
  /* This is a single line comment */
  /* This is a multi line
     comment */
  var data = "Hi this is a string.";
  """
  parser = JSParser("path", content)
  assert parser.sections.has_section("This is a single line comment")
  assert parser.sections.has_section("This is a multi line")
  assert parser.sections.has_section("comment")
  assert parser.sections.has_section("Hi this is a string.")
