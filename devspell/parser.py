import os
import plugins
import enchant
import time
import yaml
from dictionary import Dictionary

class Parser(object):
  def __init__(self, path, dictionary=None):
    """Create a parser

    :param path: The path to parse
    :param dictionary: If provided will read in the current dictionary
    """
    self.path = path
    self.enchant = enchant.Dict("en_US")
    self.docs = []
    self.only = []
    self.words = Words()
    self.dictionary = Dictionary()
    if dictionary:
      self.dictionary.parse(dictionary)

  def show(self, quiet=False):
    """Show the results of the parsing

    :param quiet: If True then this will only print out the words
                  otherwise this will show the words, suggestions, as well as
                  what files have the misspelled words
    """
    if not quiet:
      self.words.get_suggestions(self)
    for word in self.words.words.values():
      if not word.ok:
        if quiet:
          word.show_quiet()
        else:
          word.show_verbose()

  def parse(self):
    """The main parsing work

    :return: True on succes. False otherwise
    """
    ret = False
    if not self.path:
      return False
    elif not os.path.exists(self.path):
      return False
    elif os.path.isfile(self.path):
      ret = self.parse_file(self.path)
    else:
      ret = self.parse_dir(self.path)

    print("Finished processing files")
    print("=" * 80)
    return ret

  def parse_file(self, path):
    """Parse a single file

    :param path: The path to parse
    """
    doc = Document(self, path)
    if self.only:
      if doc.exten not in self.only:
        return False
    doc.parse()
    self.docs.append(doc)
    return True

  def parse_dir(self, path):
    """Parse a directory

    :param path: The directory to parse
    """
    for root, dirs, files in os.walk(path):
      for item in files:
        fname = os.path.join(root, item)
        self.parse_file(fname)
    return True

  def create_dictionary(self, path):
    """Create a dictionary from the misspelled words found

    :param path: The path of the dictionary to read/write to
    """
    spelldict = Dictionary(path)
    spelldict.parse(strict=False)
    for word in self.words.invalid:
      spelldict.add_global(word.word)
    spelldict.save()

class Document(object):
  def __init__(self, parser, path):
    """Initialize a Document object

    :param parser: The parser object
    :param path: The path of the document
    """
    self.parser = parser
    self.path = path
    self.exten = os.path.splitext(path)[1]
    self.content = None
    if self.exten not in plugins.PLUGINS.keys():
      return
    if os.path.exists(self.path):
      with open(self.path, 'r') as fp:
        self.content = fp.read()

  def __repr__(self):
    return "Document {}".format(self.path)

  def parse(self):
    """Parse the document path"""
    if not self.content:
      return False
    plugin = plugins.get_parser(self.exten)
    if not plugin:
      print("{}: No plugin to handle extension {}".format(
        self.path, self.exten))
      return False
    print("Processing {}".format(self.path))
    stime = time.time()
    obj = plugin(self.path, self.content)
    for section in obj.sections.sections:
      for word in section.content.split():
        self.check_word(word.strip().lower(), section.line)
    diff = time.time() - stime
    print("Processing {} took {:.4f}s".format(self.path, diff))
    return True

  def check_word(self, word, line):
    """Check if a word is valid

    :param word: The word to check
    :param line: The line this word was on in the document
    """
    obj = self.parser.words.words.get(word)
    if obj:
      if not obj.ok:
        # If it exists and its a failure then add our current info to it
        obj.num += 1
        obj.places.append(WordLocation(self.path, line))
    else:
      self.parser.words.words[word] = Word(word, self.path, line)
      if len(word) < 2:
        return
      if not word.isalpha():
        return
      # If its in the dictionary then its fine.
      # We go through here so that its a quick
      # one stop lookup at the top
      if self.parser.dictionary.has_word(word):
        return
      # Spellcheck the word
      if not self.parser.enchant.check(word):
        self.parser.words.words[word].ok = False

class WordLocation(object):
  def __init__(self, path, line):
    self.path = path
    self.line = line

  def __repr__(self):
    if self.line is not None:
      return "{}:{}".format(self.path, self.line)
    return "{}".format(self.path)

class Word(object):
  def __init__(self, word, path, line):
    self.word = word
    self.num = 1
    self.places = [WordLocation(path, line)]
    self.ok = True
    self.suggestions = []

  def show_quiet(self):
    print("{} places {}".format(self.word, len(self.places)))

  def show_verbose(self):
    print('=' * 80)
    print('word: {}'.format(self.word))
    if self.suggestions:
      print('--------- Suggestions ------------')
      for item in self.suggestions:
        print(item)
    print('--------- Places ------------')
    places = set(self.places)
    for place in places:
      print(place)

class Words(object):
  def __init__(self):
    self.words = {}

  @property
  def invalid(self):
    """Get the list of invalid

    :return: List of invalid words
    """
    result = []
    for item in self.words.values():
      if not item.ok:
        result.append(item)
    return result

  def get(self, word):
    """Get the word object by the word passed in

    :param word: The word to search for
    :return: The found word or None
    """
    return self.words.get(word)

  def has(self, word, valid=True):
    """Return if the word exists and is valid/invalid

    :param word: The word to search for
    :param valid: Whether to find the word that is valid or invalid
    :return: If the word exists and it matches the valid arg then return
             True, otherwise False.
    """
    obj = self.get(word)
    if obj:
      if obj.ok == valid:
        return True
    return False

  def has_valid(self, word):
    """Return if the word exists and is valid

    :param word: The word to search for
    :return: True if the word exists and its valid, otherwise return False
    """
    return self.has(word)

  def has_invalid(self, word):
    """Return if the word exists and is invalid

    :param word: The word to search for
    :return: True if the word exists and its invalid, otherwise return False
    """
    return self.has(word, valid=False)

  def get_suggestions(self, parser):
    """Get the suggestions for a word

    :param parser: The parser object
    """
    for word in self.words.values():
      if not word.ok:
        word.suggestions = parser.enchant.suggest(word.word)
