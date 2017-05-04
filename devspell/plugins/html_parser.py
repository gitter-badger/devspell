from lang_parser import LangParser
import requests
import bs4

IGNORE_TAGS = [
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
        continue
      # Parse the text if available
      try:
        data = item.get_text()
        self.set_title("html text")
        self.sections.add_simple(data)
      except:
        pass
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
      self.sections.add_simple(comments.extract())
