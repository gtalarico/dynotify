import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib import messages
# from django.db.models import Q

from .forms import SubscriberForm
from .services import update_posts_db
from .services import send_email_subscribed, send_email_unsubscribed
from .models import Subscriber, Post

logger = logging.getLogger()


def posts(request):
    pass

def index(request):
    context = RequestContext(request)
    form = SubscriberForm()

    if request.method == 'POST':
        form = SubscriberForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            # Create new subscriber if email is new
            if not Subscriber.objects.filter(email=email).exists():
                subscriber = form.save(commit=False)
                subscriber.save()
                send_email_subscribed(subscriber.email)
                form = SubscriberForm()
                logger.info('New subscriber added.')
                messages.success(request, 'New Subscriber Added.')
            # Toggle is_active if email exists
            else:
                subscriber = Subscriber.objects.filter(email=email).first()
                subscriber.is_active = not subscriber.is_active
                subscriber.save()

                if subscriber.is_active:
                    messages.success(request, 'Subscriber Reactivated.')
                    send_email_subscribed(subscriber.email)

                else:
                    send_email_unsubscribed(subscriber.email)
                    messages.success(request, 'Subscriber Deactivated.')



        else:
            message = 'Something went wrong. Check the form for errors.'
            logger.info('Email parsing error: %s',
                        form.cleaned_data.get('email'))
            messages.warning(request, message)

    # update_posts_db()

    context['form'] = form
    context['posts'] = Post.objects.exclude(status='sent').order_by('-timestamp')
    if context['posts']:
        context['comment'] = '{} new or updated posts'.format(len(context['posts']))
    else:
        context['comment'] = 'Sweet. No new posts.'

    return render(request, 'index.html', context=context)
