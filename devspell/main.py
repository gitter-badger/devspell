#!/usr/bin/python

"""Spell check Development files"""

from __future__ import print_function
import os, sys, argparse, textwrap
from parser import Parser
from dictionary import Dictionary

__author__ = "Nodar Nutsubidze"

def ap_check(args):
  """Check a file or directory for spelling

  :param args: The command line arguments
  """
  if not os.path.exists(args.path):
    print("No such path {}".format(args.path))
    return
  obj = Parser(args.path, dictionary=args.dictionary)
  obj.only = args.only
  obj.parse()
  obj.show()
  if args.save_dictionary:
    obj.create_dictonary(args.save_dictionary)

def ap_dict(args):
  """Interact with the dictionary provided

  :param args: The command line arguments
  """
  if not os.path.exists(args.path):
    print("No such path {}".format(args.path))
    return
  obj = Dictionary(args.path)
  if obj.parse():
    obj.show()

if __name__ == "__main__":
  def add_sp(sub_p, action, func=None, help=None):
    """Add an action to the main parser

    :param sub_p: The sub parser
    :param action: The action name
    :param func: The function to perform for this action
    :param help: The help to show for this action
    :rtype: The parser that is generated
    """
    p = sub_p.add_parser(action, help=help)
    if func:
      p.set_defaults(func=func)
    p.add_argument('-v', '--verbose', action='store_true',
             help='Show verbose logging')
    return p

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description = 'Spell check anything')
  sub_p = parser.add_subparsers(title='Actions',
                                help='%(prog)s <action> -h for more info')
  p_check = add_sp(sub_p, "check", ap_check,
    help="Check files/directories/...")
  p_check.add_argument("path",
    help="What to spell check")
  p_check.add_argument('-d', '--dictionary',
    help='Path to a dictionary with valid word')
  p_check.add_argument('-o', '--only',
    default=[], action='append',
    help='Extensions to only parse')
  p_check.add_argument('--save-dictionary',
    help=('If this option is passed in then it will write '
         'the words found to a dictionary'))

  p_dict = add_sp(sub_p, "dictionary", ap_dict,
    help="Interact with the dictionary")
  p_dict.add_argument("path",
    help="Path of the dictionary")
  args = parser.parse_args()
  args.func(args)
