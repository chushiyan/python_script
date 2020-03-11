# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class TournamentItem(scrapy.Item):
    url = Field()

    tournament_id = Field()
    skill_level = Field()
    date = Field()
    divisions = Field()



    section = Field()
    district = Field()
    surface_type = Field()
    draws_posted = Field()
    last_updated = Field()

    org_name = Field()
    org_phone = Field()
    org_fax = Field()
    org_website = Field()
    org_address = Field()
    '''
    Street/PO Box, City, State, Zip code
    '''
    org_street_or_pobox = Field()
    org_city = Field()
    org_state = Field()
    org_zip_code = Field()



    director = Field()
    director_phone = Field()
    director_cell = Field()
    director_fax = Field()
    director_email = Field()
    referee = Field()
    referee_phone = Field()
    referee_email = Field()



    entries_closed = Field()
    entry_information = Field()
    checks_payable_to = Field()
    send_checks_to = Field()
    tournament_website = Field()
