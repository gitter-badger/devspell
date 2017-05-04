from lang_parser import LangParser

class ZSHParser(LangParser):

  def parse(self):
    self.parse_shell_comments()
    self.parse_string_literals()
