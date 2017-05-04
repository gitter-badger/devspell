import bash_parser
import cpp_parser
import css_parser
import html_parser
import js_parser
import py_parser
import txt_parser
import zsh_parser

PLUGINS = {
  '.bash': bash_parser.BashParser,
  '.c': cpp_parser.CppParser,
  '.css': css_parser.CSSParser,
  '.cpp': cpp_parser.CppParser,
  '.h': cpp_parser.CppParser,
  '.html': html_parser.HTMLParser,
  '.htm': html_parser.HTMLParser,
  '.js': js_parser.JSParser,
  '.py': py_parser.PyParser,
  '.sh': bash_parser.BashParser,
  '.txt': txt_parser.TextParser,
  '.zsh': zsh_parser.ZSHParser,
}

def get_parser(exten):
  return PLUGINS.get(exten)
