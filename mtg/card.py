import tempfile
import urllib
import subprocess
from textwrap import wrap

from elixir import Entity, Field, ManyToMany
from elixir import Unicode, SmallInteger, Integer, UnicodeText, Enum, Binary

class CardType(Entity):
    name = Field(Unicode(30), primary_key=True)
    code = Field(Unicode(30), primary_key=True)

class Card(Entity):
    name = Field(Unicode(100), primary_key=True)

    # Should be in "sets" intermediate table
    number = Field(SmallInteger)
    sets = ManyToMany('Set')

    types = ManyToMany('CardType')

    # mana casting cost
    unco_cost = Field(SmallInteger)
    blue_cost = Field(SmallInteger)
    red_cost = Field(SmallInteger)
    green_cost = Field(SmallInteger)
    black_cost = Field(SmallInteger)
    white_cost = Field(SmallInteger)

    converted_cost = Field(SmallInteger)

    #power
    #toughness
    rarity = Field(Enum(enums=('C', 'U', 'R', 'M')))
    text = Field(UnicodeText)
    picture = Field(Binary)
    
    # FIXME: This sucks, it should depends on the set
    def get_picture(self):
        BASEURL = 'http://magiccards.info/scans/en/'
        if not self.picture:
            url = "%s/%s.jpg" % (BASEURL + self.set.code, self.number)
            # print url
            s = urllib.urlopen(url)
            if not s.getcode() == 200:
                return "Failed to retrieve image. (Error: %s)" % s.getcode()
            self.picture = s.read()

        return self.picture

    def info(self, **options):
        print
        print options
        print
        print "{0:40}{1:>20}".format(self.name, self.manacost)
        print "{0:40}{1:>20}".format(self.types, RARITYCODES.get(self.rarity))
        if self.power or self.toughness:
            print "{0:30}{1:>30}".format("%s %s / %s" % (self.color, self.power ,self.toughness),
                                         "%s #%s" % (self.set.title(), self.number),
                                         )
        else :
            print self.color
        if not "supress" in options:
            print "-" * 60
            print "\n".join(wrap(self.text, 60))
        print

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Card: %s (%s)" % (self.name, self.set)
