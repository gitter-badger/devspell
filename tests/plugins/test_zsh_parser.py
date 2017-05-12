import os
import sys
import pytest
import context

from context import devspell
ZSHParser = devspell.plugins.ZSHParser

def test_zsh_basic():
  """Test the basic operation of the ZSH parser"""

  content = """
  # This is a coment which is wong
  text="This is anoter comment which is vong"
  single='A single quote with suf'
  """
  parser = ZSHParser("path", content)
  assert len(parser.lines.lines) == 5
  assert len(parser.sections.sections) == 3

def test_zsh_comment_no_end():
  """Test ZSH comment without a newline"""
  content = "# A comment line"
  parser = ZSHParser("path", content)
  assert parser.sections.has_section("A comment line")
