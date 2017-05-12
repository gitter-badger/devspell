from lang_parser import LangParser

class PyParser(LangParser):

  def parse(self):
    self.parse_block_comments()
    self.parse_string_literals()
    self.parse_shell_comments()

  def _parse_block_comments_pattern(self, pattern):
    """Parse a block comment based on a pattern

    :param pattern: What to search for
    """
    cur = 0
    end = len(self.content)
    while cur < end:
      sloc = self.content.find(pattern, cur)
      if sloc < 0:
        break
      eloc = self.content.find(pattern, sloc + len(pattern))
      if eloc < 0:
        break
      blob = self.content[sloc+len(pattern):eloc]
      cur = eloc + len(pattern)
      self.sections.add(blob, sloc, eloc + len(pattern))

  def parse_block_comments(self):
    """Parse a block comment"""
    self._parse_block_comments_pattern('"""')
    self._parse_block_comments_pattern("'''")
