from lang_parser import LangParser
from bash_parser import BashParser
from cpp_parser import CppParser
from css_parser import CSSParser
from html_parser import HTMLParser
from js_parser import JSParser
from py_parser import PyParser
from txt_parser import TextParser
from zsh_parser import ZSHParser

PLUGINS = {
  '.bash': BashParser,
  '.c': CppParser,
  '.css': CSSParser,
  '.cpp': CppParser,
  '.h': CppParser,
  '.html': HTMLParser,
  '.htm': HTMLParser,
  '.js': JSParser,
  '.py': PyParser,
  '.sh': BashParser,
  '.txt': TextParser,
  '.zsh': ZSHParser,
}

def get_parser(exten):
  return PLUGINS.get(exten)
