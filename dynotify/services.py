import sys
import re
import logging

import requests
import bs4

from .models import Post
# allows unicode printing
# reload(sys)
# sys.setdefaultencoding('utf8')

FORUM_URL = 'http://dynamobim.org/forums/forum/dyn/'
POST_CONTAINERS_CLASS = 'bbp-topic bbp-custom-topics-container'
POST_TITLE_CLASS = 'bbp-topic-permalink topic-title-bbpn'
ACTIVITY_CLASS = 'topic-reply-count-area'
OP_CLASS = 'bbp-author-name'

def update_posts_db():
    r = requests.get(FORUM_URL)
    print 'STATUS:', r.status_code
    page = r.content

    soup = bs4.BeautifulSoup(page, 'html.parser')
    posts_containers = soup.find_all(name='ul', attrs={
                       'id': POST_CONTAINERS_CLASS})

    posts = []
    post_dict = {}
    for post in posts_containers:
        activity = post.find(name='div',
                             attrs={'class': ACTIVITY_CLASS}).text.strip()
        op = post.find(name='a',
                       attrs={'class': OP_CLASS}).text.strip()
        title = post.find(name='a',
                          attrs={'class': POST_TITLE_CLASS}).text.strip()
        url = post.find(name='a',
                        attrs={'class': POST_TITLE_CLASS}).get('href')

        if not Post.objects.filter(url=url).exists():
            post = Post(title=title, op=op, activity=activity,url=url,
                        status='new')
            post.save()
        # print post.text.encode('utf-8')


def check_if_already_sent():

    pass

def send_mass_emails():
    pass
