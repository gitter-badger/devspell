import os
import yaml

SECTIONS = [
  '_GLOBAL'
]

class Dictionary(object):
  def __init__(self, path=None):
    self.path = path
    self.dictionary = {}
    print("my dict {}".format(self.dictionary))
    self.setup()

  def setup(self):
    if not self.dictionary:
      self.dictionary = {}
    print("dict: {}".format(self.dictionary))
    # Make sure lists exists for global sections
    for item in SECTIONS:
      if self.dictionary.get(item) is None:
        self.dictionary[item] = []

  def parse(self, path=None, strict=True):
    if path:
      self.path = path
    if not self.path:
      print("Error: No path set in the dictionary")
      return

    # Read in the current dictionary if it exists
    dictionary = None
    if os.path.exists(self.path):
      with open(self.path, 'r') as fp:
        self.dictionary = yaml.load(fp.read())
        print("result: {}".format(self.dictionary))
    elif strict:
      print("Error: Dictionary does not exist")
      return False
    if not self.dictionary:
      self.setup()
    return True

  def save(self):
    with open(self.path, 'w') as fp:
      fp.write(yaml.dump(self.dictionary, default_flow_style=False))
    print("Wrote the dictionary to {}".format(self.path))

  def add_global(self, word):
    self.dictionary['_GLOBAL'].append(word)

  def has_word(self, word):
    if word in self.dictionary['_GLOBAL']:
      return True
    return False
