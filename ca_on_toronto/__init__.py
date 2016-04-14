from __future__ import unicode_literals
from .jurisdiction import TorontoJurisdiction

import lxml.html
import requests


class Toronto(TorontoJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3520005'
    division_name = 'Toronto'
    name = 'Toronto City Council'
    url = 'http://www.toronto.ca'
    check_sessions = True
    legislative_sessions = []

    def __init__(self):
        super(Toronto, self).__init__()
        # TODO: Accommodate legacy format pages. (bad old PDF days)
        # {'identifier': '1998-2000'},
        # {'identifier': '2000-2003'},
        # {'identifier': '2003-2006'},
        self.legislative_sessions = [self.leg_session(session) for session in self.sessions()]

    def get_session_list(self):
        return [session['term_name'] for session in self.sessions()]

    def leg_session(self, session):
        leg_session = {}
        start_year, end_year = session['term_name'].split('-')
        leg_session['identifier'] = session['term_name']
        leg_session['name'] = session['term_name']
        leg_session['start_date'] = '{}-12-01'.format(start_year)
        leg_session['end_date'] = '{}-11-30'.format(end_year)
        leg_session['classification'] = 'primary'

        return leg_session

    def sessions(self):
        response = requests.get('http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare')
        page = lxml.html.fromstring(response.text)
        # Remove the blank option label and sort chronologically
        for option in reversed(page.xpath('//select[@name="termId"][1]/option')[1:]):
            session = {}
            session['termId'] = option.attrib['value']
            session['term_name'] = option.text
            yield session
