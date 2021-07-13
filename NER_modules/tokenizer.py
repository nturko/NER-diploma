# coding: utf-8
from __future__ import unicode_literals

from earley_parser.tokenizer import MorphTokenizer


TOKENIZER = MorphTokenizer().remove_types('EOL')
