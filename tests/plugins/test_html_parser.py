import os
import sys
import pytest
import context

from context import devspell
HTMLParser = devspell.plugins.HTMLParser

def test_html_basic():
  """Test the basic operation of the HTML parser"""

  content = """
  <!-- This is a comment -->
  <html>
    <head>
      <title>This is a title</title>
      <script>
        var my_func = function () {
          var test = "This is a script";
        };
      </script>
    </head>
    <body>
      <p tooltip="This is a tooltip"
         title="This is an attr">
        Paragraph content
      </p>
      <p/>
    </body>
  </html>
  """
  parser = HTMLParser("path", content)
  print(parser.sections.sections)
  assert not parser.sections.has_section("This is a script")
  assert parser.sections.has_section("This is a comment")
  assert parser.sections.has_section("This is a title")
  assert parser.sections.has_section("This is a tooltip")
  assert parser.sections.has_section("This is an attr")
  assert parser.sections.has_section("Paragraph content")
