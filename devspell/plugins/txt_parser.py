from lang_parser import LangParser

class TextParser(LangParser):

  def parse(self):
    """Parse text"""
    self.set_title("txt")
    self.sections.add_simple(self.content)
