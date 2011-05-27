#!/usr/bin/python

from elixir import *

from mtg.card import Card
from mtg.set import Set
from mtg.deck import Deck

from mtg.gatherer.card_extractor import CardExtractor, SingleCardExtractor
from mtg.gatherer.gatherer_request import SearchRequest

metadata.bind = "sqlite:///mtg.db"
metadata.bind.echo = True

setup_all(True)
create_all()

s = SearchRequest(options={'name': "howl from beyond"})

print s.url
r = s.send()

for card in CardExtractor(r).extract():
    print card
