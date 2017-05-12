import os
import sys
import pytest
import context

from context import devspell
CppParser = devspell.plugins.CppParser

def test_cpp_basic():
  """Test the basic operation of the CPP parser"""

  content = """
  /* This is a single line comment */
  /* This is a multi line
     comment */
  int main(int argc, char **argv) {
    char *s = strdup("Hi tis is a stingr");
  }
  """
  parser = CppParser("path", content)
  assert len(parser.lines.lines) == 8
  assert parser.sections.has_section("This is a single line comment")
  assert parser.sections.has_section("This is a multi line")
  assert parser.sections.has_section("comment")
  assert parser.sections.has_section("Hi tis is a stingr")

def test_cpp_single_line_no_end():
  """Test a single line comment without an end"""
  content = "A line with a //comment"

  parser = CppParser("path", content)
  assert len(parser.lines.lines) == 1
  assert parser.sections.has_section("comment")

def test_cpp_multi_line_no_end():
  """Test a multi line based comment w/o an end tag"""
  content = "A line with a /* comment"
  content = """
  /**
   * A good comment
   */
  /****
   * Lots of *s are valid
   */
  /***
   * This should fail
  """

  parser = CppParser("path", content)
  assert len(parser.lines.lines) == 10
  assert parser.sections.has_section("A good comment")
  assert parser.sections.has_section("Lots of *s are valid")
  assert not parser.sections.has_section("This should fail")
