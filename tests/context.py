import os
import sys
sys.path.append("../")

import devspell

def get_path(path):
  """Return the test path

  :param path: The path to join
  :return: The full test file path
  """
  full = os.path.join("tests/files", path)
  return full

def get_dict(path):
  """Return the test dictionary path

  :param path: The path to join
  :return: The full test dictionary path
  """
  return get_path("dicts/{}".format(path))
