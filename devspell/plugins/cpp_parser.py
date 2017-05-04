from lang_parser import LangParser

class CppParser(LangParser):

  def parse(self):
    self.parse_comments()
    self.parse_string_literals_double()

  def parse_comments(self):
    """Parse CPP comments

    /* - Start of comment (potentially multi-line)
    */ - End of comment (potentially multi-line)
    // - One line comment
    """
    self.set_title("comments")
    start_tag_ml = "/*"
    end_tag_ml = "*/"
    single_line = "//"
    cur = 0
    end = len(self.content)
    in_multi_line = False
    ml_start_loc = 0
    while cur < end:
      if in_multi_line:
        # Search for the end of the multi-line
        loc = self.content.find(end_tag_ml, cur)
        if loc < 0:
          print("Did not find end of tag for multi-line. cur {}".format(cur))
          return
        blob = self.content[ml_start_loc:loc]
        blob = blob.strip().lstrip('*').strip()
        self.sections.add(blob, ml_start_loc, loc)
        cur = loc
        in_multi_line = False
        continue
      else:
        do_multi_line = False
        do_single_line = False

        loc1 = self.content.find(start_tag_ml, cur)
        loc2 = self.content.find(single_line, cur)
        if loc1 >= 0 and loc2 >= 0:
          if loc1 < loc2:
            do_multi_line = True
          else:
            do_single_line = True
        elif loc1 >= 0:
          do_multi_line = True
        elif loc2 >= 0:
          do_single_line = True
        else:
          break

        if do_multi_line:
          cur = loc1 + len(start_tag_ml)
          ml_start_loc = cur
          in_multi_line = True
        elif do_single_line:
          cur = loc2 + len(single_line)
          loc = self.content.find('\n', loc2)
          if loc < 0:
            print("Did not find newline for single line comment")
          else:
            blob = self.content[cur:loc].strip()
            if blob:
              self.sections.add(blob, cur, loc)
            cur = loc
