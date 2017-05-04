from lang_parser import LangParser

class PyParser(LangParser):

  def parse(self):
    self.parse_block_comments()
    self.parse_string_literals()
    self.parse_shell_comments()

  def parse_block_comments(self):
    char = '"""'
    cur = 0
    end = len(self.content)
    while cur < end:
      sloc = self.content.find(char, cur)
      if sloc < 0:
        break
      eloc = self.content.find(char, sloc + len(char))
      if eloc < 0:
        break
      blob = self.content[sloc+len(char):eloc]
      cur = eloc + len(char)
      print("Found blob: [{}]".format(blob))
      self.sections.add(blob, sloc, eloc + len(char))
