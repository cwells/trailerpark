'''A plugin to display the most recent articles on the main page.
'''

url       = '^$'   # only display on /
action    = 'view' # only display on view request
depends   = ['blog','article']
templates = ['template']
views     = ['articles_by_date']
