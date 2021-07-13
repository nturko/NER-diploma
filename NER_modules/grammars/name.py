# coding: utf-8
from __future__ import unicode_literals

from earley_parser import (
    rule,
    and_, or_, not_,
)
from earley_parser.interpretation import fact
from earley_parser.predicates import (
    gram, tag,
    is_capitalized, vesum_tag
)
from earley_parser.predicates.bank import DictionaryPredicate as dictionary
from earley_parser.relations import gnc_relation

from NER_modules.data import load_dict

from earley_parser.rule.transformators import RuleTransformator
from earley_parser.rule.constructors import Rule
from earley_parser.predicates.constructors import AndPredicate


Name = fact(
    'Name',
    ['first', 'middle', 'last', 'nick']
)


FIRST_DICT = set(load_dict('first_uk.txt'))
LAST_DICT = set(load_dict('last_uk.txt'))


##########
#
#  COMPONENTS
#
###########


IN_FIRST = dictionary(FIRST_DICT)
IN_LAST = dictionary(LAST_DICT)

gnc = gnc_relation()


########
#
#   FIRST
#
########


TITLE = is_capitalized()

NOUN = or_(
    gram('NOUN'),
    vesum_tag('noun')
)
NAME_CRF = tag('I')

ABBR = or_(
    gram('Abbr'),
    vesum_tag('abbr')
)

NAME = and_(
    or_(
        gram('Name'),
        vesum_tag('fname')
    ),
    not_(ABBR)
)

VESUM_LAST_NAME = vesum_tag('lname')

PATR = and_(
    or_(
        gram('Patr'),
        vesum_tag('pname')
    ),
    not_(ABBR)
)

FIRST = or_(
    NAME_CRF,
    NAME,
    IN_FIRST
).interpretation(
    Name.first.inflected()
)

FIRST_ABBR = and_(
    ABBR,
    TITLE
).interpretation(
    Name.first
)


##########
#
#   LAST
#
#########


LAST = or_(
    IN_LAST,
    VESUM_LAST_NAME
).interpretation(
    Name.last.inflected()
)


########
#
#   MIDDLE
#
#########


MIDDLE = PATR.interpretation(
    Name.middle.inflected()
)

MIDDLE_ABBR = and_(
    ABBR,
    TITLE
).interpretation(
    Name.middle
)


#########
#
#  FI IF
#
#########


FIRST_LAST = rule(
    FIRST,
    LAST
)

LAST_FIRST = rule(
    LAST,
    FIRST
)


###########
#
#  ABBR
#
###########


ABBR_FIRST_LAST = rule(
    FIRST_ABBR,
    '.',
    LAST
)

LAST_ABBR_FIRST = rule(
    LAST,
    FIRST_ABBR,
    '.',
)

ABBR_FIRST_MIDDLE_LAST = rule(
    FIRST_ABBR,
    '.',
    MIDDLE_ABBR,
    '.',
    LAST
)

LAST_ABBR_FIRST_MIDDLE = rule(
    LAST,
    FIRST_ABBR,
    '.',
    MIDDLE_ABBR,
    '.'
)


##############
#
#  MIDDLE
#
#############


FIRST_MIDDLE = rule(
    FIRST,
    MIDDLE
)

FIRST_MIDDLE_LAST = rule(
    FIRST,
    MIDDLE,
    LAST
)

LAST_FIRST_MIDDLE = rule(
    LAST,
    FIRST,
    MIDDLE
)


##############
#
#  SINGLE
#
#############


JUST_FIRST = FIRST

JUST_LAST = LAST


########
#
#    FULL
#
########


NAME = or_(
    FIRST_LAST,
    LAST_FIRST,

    ABBR_FIRST_LAST,
    LAST_ABBR_FIRST,
    ABBR_FIRST_MIDDLE_LAST,
    LAST_ABBR_FIRST_MIDDLE,

    FIRST_MIDDLE,
    FIRST_MIDDLE_LAST,
    LAST_FIRST_MIDDLE,

    JUST_FIRST,
    JUST_LAST,
).interpretation(
    Name
)


class StripCrfTransformator(RuleTransformator):
    def visit_term(self, item):
        if isinstance(item, Rule):
            return self.visit(item)
        elif isinstance(item, AndPredicate):
            predicates = [_ for _ in item.predicates if _ != NAME_CRF]
            return AndPredicate(predicates)
        else:
            return item


SIMPLE_NAME = NAME.transform(
    StripCrfTransformator
)
