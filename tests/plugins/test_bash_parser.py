import os
import sys
import pytest
import context

from context import devspell
BashParser = devspell.plugins.BashParser

def test_bash_basic():
  """Test the basic operation of the Bash parser"""

  content = """
  # This is a coment which is wong
  text="This is anoter comment which is vong"
  single='A single quote with suf'
  """
  parser = BashParser("path", content)
  assert len(parser.lines.lines) == 5
  assert len(parser.sections.sections) == 3
