import os
import sys
import pytest
import context

from context import devspell
CSSParser = devspell.plugins.CSSParser

def test_css_basic():
  """Test the basic operation of the CSS parser"""

  content = """
  /* This is a single line comment */
  /* This is a multi line
     comment */
  // This Should not be counted
  """
  parser = CSSParser("path", content)
  assert len(parser.lines.lines) == 6
  assert parser.sections.has_section("This is a single line comment")
  assert parser.sections.has_section("This is a multi line")
  assert parser.sections.has_section("comment")
  assert not parser.sections.has_section("This should not be counted")
