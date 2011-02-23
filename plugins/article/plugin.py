import re
from tornado.options import options
from datetime import datetime

url       = '.+'
action    = 'view'
templates = ['template']
depends   = ['blog']

class Slugify (object):
    '''on loan from Django
    '''
    removelist = [
        "a", "an", "as", "at", "before", "but", "by", "for","from",
        "is", "in", "into", "like", "of", "off", "on", "onto","per",
        "since", "than", "the", "this", "that", "to", "up", "via","with"
        ]

    def __call__ (self, s):
        for a in self.removelist:
            aslug = re.sub (r'\b' + a + r'\b', '', s)
            aslug = re.sub ('[^\w\s-]', '', aslug).strip ().lower ()
            aslug = re.sub ('\s+', '-', aslug)
        return aslug

slugify = Slugify ()

def createdoc (data):
    today = datetime.today ().strftime ('%Y/%m/%d')    
    data ['_id'] = "%s/%s" % (today, slugify ("%s" % data ['title']))
    data ['date'] = today
    return data

install  = {
    "docs": [
        createdoc ({ 
            "title": "Welcome!",
            "content": '.. format: rst\n\nWelcome to %s_. \n\n.. _%s: %s' % (options.title, options.title, options.url),
            "tags": "",
            "thumb": "",
            "category": "",
            # "featured": True,
            # "featured_image": "",
            "summary": "Welcome to Trailerpark!",
            "published": True 
        })
    ]
}
