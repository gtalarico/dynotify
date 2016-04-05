import sys
import logging

import requests
import bs4

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import Post, Subscriber
# allows unicode printing
# reload(sys)
# sys.setdefaultencoding('utf8')

logger = logging.getLogger()

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

        # Post does not exists:
        # if not Post.objects.filter(url=url).exists():
        post, created = Post.objects.update_or_create(title=title,
                                                      op=op,
                                                      activity=activity,
                                                      url=url,
                                                      status='new')
        post.save()


# This is called by a manager.py command notify, set on a 10 min schedule
def send_dynotify():
    posts = Post.objects.filter(status='new')

    if posts:
        plaintext = get_template('email.txt')
        htmly    = get_template('email.html')

        context = Context()
        context['posts'] = posts

        subject = 'Dynotify: Posts'
        from_email = 'Dynotify <gtalarico@gmail.com>'
        to = Subscriber.objects.filter(is_active=True).values_list('email',
                                                                   flat=True)
        headers = {"Reply-To": "gtalarico+dynotify@gmail.com"}

        text_content = plaintext.render(context)
        html_content = htmly.render(context)
        mail = EmailMultiAlternatives(
            subject=subject, body=text_content, from_email=from_email,
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
    body="Your email has been added to dynotify.herokuapps.com",
    from_email="Dynotify <gtalarico@gmail.com>",
    to=[email],
    headers={"Reply-To": "gtalarico+dynotify@gmail.com"}
)
    mail.attach_alternative("<p>Your email has been subscribed to \
                            dynotify.herokuapps.com</p>", "text/html")

    print mail.send()
    logger.info('Email Sent.')


def send_email_unsubscribed(email):
    mail = EmailMultiAlternatives(
    subject="Dynotify: Unsubsribed",
    body="Your email has been remved from dynotify.herokuapps.com",
    from_email="Dynotify <gtalarico@gmail.com>",
    to=[email],
    headers={"Reply-To": "gtalarico+dynotify@gmail.com"}
)
    mail.attach_alternative("<p>Your email has been subscribed to \
                            dynotify.herokuapps.com</p>", "text/html")

    print mail.send()
    logger.info('Email Sent.')
