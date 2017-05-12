from lang_parser import LangParser
import requests
import bs4

IGNORE_TAGS = [
  "html",
  "head",
  "script",
  "body",
  "meta",
  "table",
]

HTML_ATTRS = [
  "tooltip",
  "title",
]

class HTMLParser(LangParser):

  def parse(self):
    self.parse_html_text()
    self.parse_html_comments()

  def parse_html_text(self):
    soup = bs4.BeautifulSoup(self.content, 'html.parser')
    for item in soup.descendants:
      if not item.name:
        continue
      if item.name in IGNORE_TAGS:
        print("IGNORED item.name: {}".format(item.name))
        continue
      print("ALLOWED item.name: {}".format(item.name))

      # Parse the text if available
      data = item.get_text()
      if data is not None:
        self.set_title("html text")
        print("Adding text: [{}]".format(data))
        self.sections.add_simple(data)

      # Go through attribute if available on the item
      for attr in HTML_ATTRS:
        data = item.attrs.get(attr)
        if data is not None:
          self.set_title("html attr {}".format(attr))
          self.sections.add_simple(data)

  def parse_html_comments(self):
    self.set_title("html comments")
    soup = bs4.BeautifulSoup(self.content, 'html.parser')
    for comments in soup.findAll(text=lambda text:isinstance(text, bs4.Comment)):
      print("HTML comment: {}".format(comments.extract()))
      self.sections.add_simple(comments.extract())
