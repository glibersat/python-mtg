import re

import BeautifulSoup

from .gatherer_request import CardRequest

__all__ = ['CardExtractor', 'SingleCardExtractor']

class CardExtractor(object):
    """Extracts card information from Gatherer HTML."""

    def __init__(self, html):
        self.html = html
        self.fields_per_card = 6

    def _group(self, lst, n):
        newlist = []
        for i in range(0, len(lst), n):
            val = lst[i:i+n]
            if len(val) == n:
                newlist.append(tuple(val))
        return newlist

    def extract(self, get_card_urls=False):
        #if not self.html:
        #    return False

        soup = BeautifulSoup.BeautifulSoup(self.html)

        #if not soup.table:
        #    return []

        #for tag in soup.findAll('br'):
        #    tag.replaceWith('||')

        # Find all properties of the cards
        tr_tags = soup.table.findAll('tr')

        current_card_info = {}

        for tr in tr_tags:
            rows = tr.findAll('td')

            # If this is a separator, yield the card
            # Then, start to fill the next one
            if (u'colspan', u'2') in rows[0].attrs:
                yield current_card_info
                current_card_info = {}
                continue

            prop = rows[0].renderContents().lower().strip().rstrip(':') #replace('\r\n', '').strip()
            value = rows[1].renderContents().strip() #replace('\r\n', '').strip()

            current_card[prop] = value


        # td_tags = soup.table.findAll('td')
        
        # # Get rulings hrefs here.
        # if get_card_urls:
        #     a_tags = soup.table.findAll('a')
        #     card_urls = [tag['href'] for tag in a_tags]
            
        # content_lists = [tag.contents for tag in td_tags]
        
        # unified_content = []
        # cards = []
        # for lst in content_lists:
        #     unified_content.append(''.join([item.string.strip('\r\n').strip(' ').strip('\r\n') or u'' for item in lst]))

        # unified_content = [item for item in unified_content if item != u'||']
        # unified_content = self._group(unified_content, 2)
        # data_fields = self.fields_per_card
        # unified_content = self._group(unified_content, data_fields)
        
        # for block in unified_content:
        #     #card = Card.from_block(block)
        #     print block
        #     print "-----------------"
        #     if get_card_urls:
        #         card.url = card_urls.pop(0)
        #     #cards.append(card)
        # #return cards


class SingleCardExtractor(object):

    def __init__(self, html):
        self.html = html

    def _parse_html(self):
        if not self.html:
            return False
                
    def extract_flavor(self):
        if not self.html:
            return False
        soup = BeautifulSoup.BeautifulSoup(self.html)
        flavor_text = soup.findAll(attrs={'id': re.compile('FlavorText$')})
        if flavor_text:
            flavor_text = flavor_text[0].findAll('i')[0].contents[0]
        else:
            flavor_text = ''
        return flavor_text        

    def extract(self):
        if not self.html:
            return False
        soup = BeautifulSoup.BeautifulSoup(self.html)
        for tag in soup.findAll('autocard'):
            tag.replaceWith(tag.string)
        rulings_text = soup.findAll(attrs={'id' : re.compile('rulingText$')})
        rulings_date = soup.findAll(attrs={'id' : re.compile('rulingDate$')})
        rulings_text = [''.join(tag.contents) for tag in rulings_text]
        rulings_date = [''.join(tag.contents) for tag in rulings_date]
        return zip(rulings_date, rulings_text)


