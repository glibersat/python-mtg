from elixir import Entity, Field, ManyToMany
from elixir import Unicode

class Deck(Entity):
    name = Field(Unicode(50))
    cards = ManyToMany('Card')

