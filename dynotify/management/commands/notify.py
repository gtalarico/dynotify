import logging

from django.core.management.base import BaseCommand, CommandError
from dynotify.models import Subscriber, Post
from dynotify.services import update_posts_db, send_dynotify

logger = logging.getLogger()

class Command(BaseCommand):
    help = 'Sends Email Notification to Subscribers'

    # def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Dynotification Started.'))

        update_posts_db()
        result = send_dynotify()

        self.stdout.write(self.style.SUCCESS('Dynotification Ended: %s' % result ))
