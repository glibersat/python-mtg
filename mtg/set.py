from elixir import Entity, Field
from elixir import Unicode

class Set(Entity):
    name = Field(Unicode(30), primary_key=True)


