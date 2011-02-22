'''A plugin to display the most recent articles on the main page.
'''

target    = 'content'
url       = '^$' # only display on /
depends   = ['blog','article']
templates = ['template']
views     = ['articles_by_date']
