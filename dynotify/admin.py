from django.contrib import admin

# Register your models here.
from .models import Post, Subscriber

class PostAdmin(admin.ModelAdmin):
    list_display = ["title","timestamp","status"]
    # list_display = ("title","datetime","Status")
    # list_filter = ('is_active', 'venue')
admin.site.register(Post, PostAdmin)

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["email","is_active"]
# list_filter = ('is_active', 'venue')
admin.site.register(Subscriber, SubscriberAdmin)
