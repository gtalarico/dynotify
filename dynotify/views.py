import re
import bs4

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib import messages

from .forms import SubscriberForm
from .services import get_posts
from .models import Subscriber

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
                messages.success(request, 'Subscriber Added.')
            else:
                subscriber = Subscriber.objects.filter(email=email)
                subscriber.delete()
                messages.success(request, 'Subscriber Deleted.')


        else:
            message = 'Something went wrong. Check the form for errors.'
            messages.warning(request, message)


    context['form'] = form
    context['subscribers'] = Subscriber.objects.all()
    context['posts'] = get_posts()

    return render(request, 'index.html', context=context)
