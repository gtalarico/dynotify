from django.core.management.base import BaseCommand, CommandError
from dynotify.models import Subscriber, Post
from dynotify.service import update_posts_db

class Command(BaseCommand):
    help = 'Sends Email Notification to Subscribers'

    # def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        update_posts_db()

        subscribers = Subscriber.objects.filter(is_active=True)
        for subscriber in subscribers:
            self.stdout.write(self.style.NOTICE('Sent to "%s"' % subscriber.email))

        self.stdout.write(self.style.SUCCESS('Successfully Notified'))
