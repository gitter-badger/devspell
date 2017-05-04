import os
import sys
import pytest

from context import devspell
from context import get_path
from context import get_dict

def test_doc_setup():
  """Test the basic functionality of a document"""

  parser = devspell.parser.Parser(get_path("test_dir1"))
  path = get_path("test_file1.txt")

  # Initialize a doc with an extension which is not valid
  doc = devspell.parser.Document(parser, "JIM.JIM")
  assert doc.content is None
  assert doc.exten == '.JIM'

  # Work with a document
  doc = devspell.parser.Document(parser, path)
  assert doc.path == path
  assert doc.content is not None
  assert doc.exten == '.txt'
  print(doc)
  assert doc.parse()
  doc.exten = '_NOT_VALID'
  assert not doc.parse()

  # Parse a known dictonary for this file
  parser = devspell.parser.Parser(get_path("test_dir1"))
  doc = devspell.parser.Document(parser, path)
  doc.parser.dictionary.parse(
    path=get_dict("simple.yaml"))
  assert doc.parser.dictionary.has_word('wong')
  assert doc.parse()

  # Check a word with a line number
  doc.check_word('testword', 300)
  doc.check_word('anotherword', None)
  parser.words.get('testword').show_verbose()
  parser.words.get('anotherword').show_verbose()
