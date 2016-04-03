import re
import requests
import bs4

from .models import Post

import sys
# allows unicode printing
# reload(sys)
# sys.setdefaultencoding('utf8')

FORUM_URL = 'http://dynamobim.org/forums/forum/dyn/'
POST_CONTAINERS_ID = 'bbp-topic bbp-custom-topics-container'
POST_TITLE_CLASS = 'bbp-topic-permalink topic-title-bbpn'

def update_posts_db():
    r = requests.get(FORUM_URL)
    print 'STATUS:', r.status_code
    page = r.content

    soup = bs4.BeautifulSoup(page, 'html.parser')
    posts_containers = soup.find_all(name='ul', attrs={
                       'id': POST_CONTAINERS_ID})

    posts = []
    for post in posts_containers:
        posts.append(post.find(name='a', attrs={
                    'class': POST_TITLE_CLASS}))

    post_titles = [post.text.strip() for post in posts]

    for post_title in post_titles:
        if not Post.objects.filter(title=post_title).exists():
            post = Post(title=post_title)
            post.save()
        # print post.text.encode('utf-8')

def check_if_already_sent():
    pass

def send_mass_emails():
    pass
