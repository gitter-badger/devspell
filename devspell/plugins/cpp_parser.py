from lang_parser import LangParser

class CppParser(LangParser):

  def parse(self):
    self.parse_comments()
    self.parse_string_literals_double()

  def parse_comments(self):
    """Parse all C style comments"""
    self.parse_single_comments()
    self.parse_multi_comments()

  def parse_single_comments(self):
    """Parse C single line comments //"""
    self.set_title("single line comments")
    single_line = "//"
    cur = 0
    end = len(self.content)
    while cur < end:
      loc = self.content.find(single_line, cur)
      if loc <= 0:
        break
      cur = loc + len(single_line)
      end_loc = self.content.find('\n', loc)
      if end_loc < 0:
        end_loc = end

      blob = self.content[cur:end_loc].strip()
      if blob:
        self.sections.add(blob, cur, end_loc)
      cur = end_loc

  def parse_multi_comments(self):
    """Parse CPP multi-line comments

    /* - Start of comment (potentially multi-line)
    */ - End of comment (potentially multi-line)
    """
    self.set_title("multi line comments")
    start_tag = "/*"
    end_tag = "*/"
    cur = 0
    end = len(self.content)
    in_multi_line = False
    start_loc = 0
    while cur < end:
      if in_multi_line:
        # Search for the end of the multi-line
        loc = self.content.find(end_tag, cur)
        if loc < 0:
          print("Did not find end of tag for multi-line. cur {}".format(cur))
          return
        blob = self.content[start_loc + len(start_tag):loc]
        for line in blob.splitlines():
          data = line.strip().lstrip('*').strip()
          self.sections.add(data, start_loc, loc + 1)
        cur = loc
        in_multi_line = False
        continue
      else:
        do_multi_line = False
        do_single_line = False
        loc = self.content.find(start_tag, cur)
        if loc < 0:
          break

        cur = loc + len(start_tag)
        start_loc = loc
        in_multi_line = True
