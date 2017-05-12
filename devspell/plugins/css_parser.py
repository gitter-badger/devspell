from cpp_parser import CppParser

class CSSParser(CppParser):

  def parse(self):
    """Parse comments within CSS

    Comments in CSS only support the /* */ format
    """
    self.parse_multi_comments()
