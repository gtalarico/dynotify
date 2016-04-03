import re
import bs4

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib import messages

from .forms import SubscriberForm
from .services import update_posts_db
from .models import Subscriber, Post

def index(request):
    context = RequestContext(request)
    form = SubscriberForm()

    if request.method == 'POST':
        form = SubscriberForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            if not Subscriber.objects.filter(email=email).exists():
                subscriber = form.save(commit=False)
                subscriber.save()
                messages.success(request, 'New Subscriber Added.')
                form = SubscriberForm()
            else:
                subscriber = Subscriber.objects.filter(email=email).first()
                subscriber.is_active = not subscriber.is_active
                subscriber.save()

                if subscriber.is_active:
                    messages.success(request, 'Subscriber Reactivated.')
                else:
                    messages.success(request, 'Subscriber Deactivated.')


        else:
            message = 'Something went wrong. Check the form for errors.'
            messages.warning(request, message)

    update_posts_db()

    context['form'] = form
    context['posts'] = Post.objects.all()

    return render(request, 'index.html', context=context)
