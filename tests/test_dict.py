import os
import sys
import pytest

from context import devspell
from context import get_path
from context import get_dict

def test_dict_parse_checks():
  """Test a basic dictionary"""

  # No path provided
  obj = devspell.dictionary.Dictionary()
  assert not obj.path
  assert '_GLOBAL' in obj.dictionary

  # Parsing without a path provided should fail
  assert not obj.parse()
  assert '_GLOBAL' in obj.dictionary

  # Same parsing with strict disabled should pass
  assert obj.parse(strict=False)
  assert '_GLOBAL' in obj.dictionary

  # Parsing with a path provided which does not exist
  # should fail when strict is True
  assert not obj.parse(path="_this_does_not_exist")
  assert obj.parse(path="_this_does_not_exist", strict=False)
