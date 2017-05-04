import os
import sys
import pytest

from context import devspell
from context import get_path
from context import get_dict

def test_parser_setup():
  """Test the basic functionality of a parser"""

  # Parser without a path
  parser = devspell.parser.Parser(None)
  assert not parser.path
  assert parser.enchant
  assert not parser.parse()

  # Parser with a path which doesn't exist
  parser = devspell.parser.Parser("._does_not_exist_")
  assert not parser.parse()

  # Parser with a path
  parser = devspell.parser.Parser(get_path("empty.txt"))
  assert parser.path
  assert parser.enchant
  assert parser.parse()

  # Parser with a symlink
  parser = devspell.parser.Parser(get_path("symlink"))
  assert parser.parse()

  # Parser with a dictionary set
  parser = devspell.parser.Parser(
    get_path("empty.txt"),
    dictionary=get_dict("empty"))
  assert parser.path
  assert parser.enchant

  # Add a word
  parser.words.words["bob"] = devspell.parser.Word("bob", "some-path", 30)
  parser.words.words["jim"] = devspell.parser.Word("jim", "some-path", 50)
  parser.words.words["jim"].ok = False
  parser.show()
  parser.show(quiet=True)

def test_parser_file():
  """Parse a file"""
  parser = devspell.parser.Parser(get_path("test_file1.txt"))
  assert parser.parse()
  assert parser.words.has_invalid("wong")
  assert parser.words.has_invalid("wvord")
  assert not parser.words.has_valid("wvord")
  assert parser.words.has_valid("sample")
  assert parser.words.has_valid("file")

  parser.only = ["py"]
  assert not parser.parse()

def test_parser_dir():
  """Parse a directory"""
  parser = devspell.parser.Parser(get_path("test_dir1"))
  assert parser.parse()

  assert parser.words.has_invalid("wong")
  assert parser.words.has_invalid("vord")
  assert parser.words.has_valid("file")
  assert parser.words.has_valid("which")

def test_parser_create_dict():
  """Create a dictionary based on the current words"""
  parser = devspell.parser.Parser(get_path("test_dir1"))
  assert parser.parse()
  dict_path = "/tmp/.test_parser_create_dict"
  parser.create_dictionary(dict_path)
  assert os.path.exists(dict_path)
