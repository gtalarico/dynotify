import re
import requests
import bs4

import sys
# allows unicode printing
# reload(sys)
# sys.setdefaultencoding('utf8')

FORUM_URL = 'http://dynamobim.org/forums/forum/dyn/'
POST_CONTAINERS_ID = 'bbp-topic bbp-custom-topics-container'
POST_TITLE_CLASS = 'bbp-topic-permalink topic-title-bbpn'

def get_posts():
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

    # for post_title in post_titles:
        # print post_title
        # print post.text.encode('utf-8')
    return post_titles

    # print soup.prettify()
