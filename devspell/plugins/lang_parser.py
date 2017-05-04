class LangParser(object):
  """This is the base class for all the parser plugins"""

  def __init__(self, path, content, parse=True):
    """Initialize the language parser plugin

    :param path: The path of the file that is being parsed
    :param content: The content of the file
    :param parse: Whether to parse the content
    """
    self.path = path
    self.content = content
    self.sections = Sections(self)
    self.processed = []
    self.lines = Lines(content)
    self.title = "Generic"
    if parse:
      self.parse()

  def set_title(self, title):
    """Set the title to show when showing log output

    :param title: The title to show
    """
    self.title = title

  def parse(self):
    raise NotImplemented("This must be sub-classed")

  def parse_string_literals_type(self, char):
    """Parse string literals

    Valid:
      "<DATA>" - On the same line
      "Data \
       More data" - Multi-line

    Note: A single quote in C is not valid for a string literal thus
    we do not check for it

    :param char: What to search for
    """
    cur = 0
    end = len(self.content)
    while cur < end:
      sloc = self.content.find(char, cur)
      if sloc < 0:
        break
      eloc = self.content.find(char, sloc + 1)
      if eloc < 0:
        break
      blob = self.content[sloc+1:eloc]
      cur = eloc + 1
      self.sections.add(blob, sloc, eloc + 1)
    print("New content")
    print(self.content)

  def parse_string_literals_double(self):
    self.set_title("string_literals - double")
    self.parse_string_literals_type('"')

  def parse_string_literals_single(self):
    self.set_title("string_literals - single")
    self.parse_string_literals_type("'")

  def parse_string_literals(self):
    self.parse_string_literals_double()
    self.parse_string_literals_single()

  def parse_shell_comments(self):
    """Parse comments which have #

    When a # is found a section will be added with the content
    starting after the # to the end of the line
    """
    self.set_title("shell_comments")
    cur = 0
    end = len(self.content)
    while cur < end:
      loc = self.content.find('#', cur)
      if loc < 0:
        return
      eloc = self.content.find('\n', loc + 1)
      if eloc < 0:
        eloc = end
      blob = self.content[loc+1:eloc]
      cur = eloc + 1
      self.sections.add(blob, loc, eloc)

class Line(object):
  def __init__(self, num, start, end):
    self.num = num
    self.start = start
    self.end = end

class Lines(object):
  def __init__(self, content):
    self.lines = []
    self.content = content
    self.parse()

  def parse(self):
    cur = 0
    end = 0
    if not self.content:
      return
    end = len(self.content)
    line_ix = 1
    while cur < end:
      loc = self.content.find('\n', cur)
      if loc >= 0:
        self.lines.append(Line(line_ix, cur, loc))
        cur = loc + 1
        line_ix += 1
      else:
        self.lines.append(Line(line_ix, cur, end))
        break

  def get_line_number(self, loc):
    for line in self.lines:
      if loc >= line.start and loc <= line.end:
        return line.num
    return -1

class Section(object):
  def __init__(self, parser, content):
    self.parser = parser
    self.content = content
    self.start = None
    self.end = None
    self.line = None

  def parse_words(self):
    for word in self.content.split():
      self.check_word(word.strip().lower())

  def check_word(self, word):
    if word in self.parser.processed:
      return
    self.parser.processed.append(word)
    if len(word) < 2:
      return
    if not word.isalpha():
      return
    if not self.parser.enchant.check(word):
      self.parser.errors.add(word, self.line)

class Sections(object):
  def __init__(self, parser):
    self.parser = parser
    self.sections = []

  def add(self, content, start, end):
    line = self.parser.lines.get_line_number(start)
    lines = content.split('\n')
    for data in lines:
      item = Section(self.parser, data.strip())
      item.start = start
      item.end = end
      item.line = line
      line += 1
      self.sections.append(item)
      self.clear_content(item)

  def clear_content(self, section):
    if (not section or
        section.start is None or
        section.end is None):
      return
    blank = ' ' * (section.end - section.start + 1)
    content = self.parser.content
    self.parser.content = content[:section.start] + blank + content[section.end + 1:]

  def add_simple(self, content):
      item = Section(self.parser, content.strip())
      self.sections.append(item)

  def check_word(self, word):
    if word in self.parser.processed:
      return
    if len(word) < 2:
      return
    if not word.isalpha():
      return
    if not self.parser.enchant.check(word):
      print("Word {} is not valid".format(word))
    self.parser.processed.append(word)
