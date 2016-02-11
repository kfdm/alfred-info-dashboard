import datetime
import logging
import sys

import workflow
from workflow import web

logger = logging.getLogger(__name__)
today = datetime.datetime.today()

class Workflow(workflow.Workflow):
    def cached_link(self, key, url):
        def fetch():
            return web.get(url).json()
        return self.cached_data(key, fetch)

def main(wf):
    wk = wf.cached_link('wanikani', 'https://www.wanikani.com/api/user/{0}/study-queue'.format(
        wf.settings['wanikani_api']
    ))
    wf.add_item(
        'WaniKani',
        'Reviews: {reviews_available} Lessons: {lessons_available} '.format(**wk['requested_information']),
        arg='https://www.wanikani.com',
        icon='wk.png',
        valid=True,
    )

    for countdown in wf.cached_link('countdowns', 'https://tsundere.co/api/countdown.json').get('results', []):
        created = datetime.datetime.strptime(countdown['created'], "%Y-%m-%dT%H:%M:%SZ")
        delta = created - today
        wf.add_item(
            countdown['label'],
            str(delta),
            icon=workflow.ICON_CLOCK,
        )

    issues = wf.cached_link('issues', 'https://api.github.com/repos/kfdm/alfred-info-dashboard/issues')
    wf.add_item(
        'Issues',
        '{} issues'.format(len(issues)),
        arg='https://github.com/kfdm/alfred-info-dashboard/issues',
        icon=workflow.ICON_WARNING,
        valid=True,
    )

    wf.send_feedback()

if __name__ == '__main__':
    sys.exit(main(Workflow()))
