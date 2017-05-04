import os
import sys
import pytest
import context

from context import devspell
LangParser = devspell.plugins.lang_parser.LangParser

def test_lang_basic():
  """Test the basic operation of the lang parser"""

  # Nothing passed in
  parser = LangParser(None, None, parse=False)
  assert not parser.content
  assert not parser.lines.lines

  # Should get an exception trying to call parse since
  # it should be subclassed
  try:
    parser.parse()
  except:
    print("Good")
    pass
  else:
    print("Bad")
    assert 0

class TestParseStringLiterals():

  def _test_even_quotes(self, content):
    parser = LangParser("path", content, parse=False)
    parser.parse_string_literals()
    assert len(parser.lines.lines) == 3
    assert len(parser.sections.sections) == 1
    assert parser.sections.sections[0].content == "equali"

  def test_even_quotes(self):
    """Test a string which has equal number of quotes"""
    even = """
    This is a short "equali" string
    """
    even_single = even.replace('"', "'")
    self._test_even_quotes(even)
    self._test_even_quotes(even_single)

  def _test_odd_quotes(self, content):
    parser = LangParser("path", content, parse=False)
    parser.parse_string_literals()
    assert len(parser.lines.lines) == 6
    assert len(parser.sections.sections) == 3
    assert parser.sections.sections[0].content == "errori"
    assert parser.sections.sections[1].content == "quote"

  def test_odd_quotes(self):
    """Test a string which has an odd number of quotes"""
    odd = """
    There is an "errori" in the quote
    Another "quote" which is write
    "A large quote which contans an error"
    Not "ending a quote
    """
    odd_single = odd.replace('"', "'")
    self._test_odd_quotes(odd)
    self._test_odd_quotes(odd_single)
