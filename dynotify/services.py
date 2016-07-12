import sys
import logging

import requests
import requests.exceptions
import bs4

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
from django.db import IntegrityError

from django.db.models import Q

from .models import Post, Subscriber
# allows unicode printing
# reload(sys)
# sys.setdefaultencoding('utf8')

logger = logging.getLogger()

FORUM_URL = 'https://forum.dynamobim.com/latest?no_definitions=true&page={0}'
PAGES = 3
POST_CONTAINERS_CLASS = 'ember-view topic-list-item'
# POST_CONTAINERS_CLASS = 'ember-view topic-list-item category-python'
POST_TITLE_CLASS = 'title'
ACTIVITY_CLASS = 'num posts-map posts heatmap-low'
OP_CLASS = 'avatar'
# OP_CLASS = 'bbp-author-name'
# ADD REPLIES
# ADD ACTIVITY
# ADD LAST

FROM_EMAIL = 'Dynotify <notification@dynotify.com>'

HEADERS = {
    'Host': 'forum.dynamobim.com',
    # 'Host': 'forum.dynamobim.com:443',
    # 'Accept': 'application/json, text/javascript, */*; q=0.01',
    # 'Accept-Encoding': 'gzip, deflate, sdch, br',
    # 'Accept-Language': 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4,es;q=0.2',
    'Referer': 'https://forum.dynamobim.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
def update_posts_db():
    logger.info('Updating Posts DB...')
    page = ''
    for page_id in range(1, PAGES+1):
        try:
            print('Making request: ', FORUM_URL.format(page_id))
            s = requests.Session()
            s.headers.update(HEADERS)
            r = s.get(FORUM_URL.format(page_id), verify=False)
        except requests.exceptions.Timeout:
            logger.error('Could not get content from forum')
            return
        print 'STATUS:', r.status_code
        page += r.content

    soup = bs4.BeautifulSoup(page, 'html.parser')
    posts_containers = soup.find_all(name='tr', attrs={
                       'class': POST_CONTAINERS_CLASS})

    soup.find_all('span',attrs={'itemprop':'name'})[0].text.strip()
    import pdb; pdb.set_trace()
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
        import pdb; pdb.set_trace()

        # Post does not exists:
        existing_post = Post.objects.filter(url=url).first()
        if existing_post and (unicode(existing_post.activity) != activity):
            existing_post.activity = activity
            existing_post.timestamp = timezone.now()
            existing_post.status = 'updated'
            existing_post.save()

        elif not Post.objects.filter(url=url).exists():
            logger.info('Saving URL: %s', url)
            new_post = Post(url=url, title=title, op=op,
                            activity=activity, status='new')
            try:
                new_post.save()
            except IntegrityError:
                logger.error('Duplicate URL: %s', url)
                # import pdb; pdb.set_trace()

    logger.info('Posts Updated...')


# This is called by a manager.py command notify, set on a 10 min schedule
def send_dynotify():
    posts = Post.objects.exclude(status='sent')

    if posts:
        plaintext = get_template('email.txt')
        htmly = get_template('email.html')

        context = Context()
        context['posts'] = posts

        subject = 'Dynotify: Posts'
        to = Subscriber.objects.filter(is_active=True).values_list('email',
                                                                   flat=True)
        headers = {"Reply-To": "gtalarico+dynotify@gmail.com"}

        text_content = plaintext.render(context)
        html_content = htmly.render(context)
        mail = EmailMultiAlternatives(
            subject=subject, body=text_content, from_email=FROM_EMAIL,
            bcc=to, headers=headers)

        mail.attach_alternative(html_content, "text/html")
        mail.send()
        logger.info('Post Email Sent')

        for post in posts:
            post.status = 'sent'
            post.save()

        return len(posts)
    else:
        logger.info('No new Posts to notify.')


def send_email_subscribed(email):
    mail = EmailMultiAlternatives(
                        subject="Dynotify: Subscribed",
                        body="Your email has been added to dynotify.com",
                        to=[email],
                        from_email=FROM_EMAIL,
                        headers={"Reply-To": "gtalarico+dynotify@gmail.com"}
                        )

    mail.attach_alternative("<p>Your email has been subscribed to \
                            dynotify.com</p>", "text/html")

    print mail.send()
    logger.info('Email Sent.')


def send_email_unsubscribed(email):
    mail = EmailMultiAlternatives(
                        subject="Dynotify: Unsubsribed",
                        body="Your email has been remved from dynotify.com",
                        from_email=FROM_EMAIL,
                        to=[email],
                        headers={"Reply-To": "gtalarico+dynotify@gmail.com"}
                        )
    mail.attach_alternative("<p>Your email has been subscribed to \
                            dynotify.com</p>", "text/html")

    print mail.send()
    logger.info('Email Sent.')
