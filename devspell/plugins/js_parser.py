from cpp_parser import CppParser

class JSParser(CppParser):

  def parse(self):
    self.parse_comments()

    # This is more complex since you will have code in the strings
    self.parse_string_literals()
