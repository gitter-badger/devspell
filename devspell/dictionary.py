import os
import yaml

SECTIONS = [
  '_GLOBAL'
]

class Dictionary(object):
  def __init__(self, path=None):
    """Initialize the dictionary

    :param path: An optional path to load a dictionary from
    """
    self.path = path
    self.dictionary = {}
    print("my dict {}".format(self.dictionary))
    self.setup()

  def setup(self):
    """Setup the dictionary

    This will ensure that the dictionary always has the
    correct sections in place
    """
    if not self.dictionary:
      self.dictionary = {}

    # Make sure lists exists for global sections
    for item in SECTIONS:
      if self.dictionary.get(item) is None:
        self.dictionary[item] = []

  def parse(self, path=None, strict=True):
    """Parse a dictionary from a path

    :param path: The path to parse
    :param strict: Whether to error if we can't parse the path
    :return: True if either strict is False or if we parsed the path
             successfully, otherwise False.
    """
    if path:
      self.path = path
    if not self.path:
      if strict:
        print("Error: No path set in the dictionary")
        return False
      print("Warning: No path set in the dictionary")
      return True

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
    """Save the dictionary to the path of the object"""
    with open(self.path, 'w') as fp:
      fp.write(yaml.dump(self.dictionary, default_flow_style=False))
    print("Wrote the dictionary to {}".format(self.path))

  def add_global(self, word):
    """Add a word to the global dictonary

    :param word: The word to add
    """
    self.dictionary['_GLOBAL'].append(word)

  def has_word(self, word):
    """Check if a word exists in the global dictionary

    :param word: The word to check
    :return: True if the word exists otherwise False
    """
    if word in self.dictionary['_GLOBAL']:
      return True
    return False
