from lang_parser import LangParser

class BashParser(LangParser):

  def parse(self):
    self.parse_shell_comments()
    self.parse_string_literals()
