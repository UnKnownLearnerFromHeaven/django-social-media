from django.contrib import admin
from .models import Post, Bids, Category, Comment

admin.site.register(Post)
admin.site.register(Bids)
admin.site.register(Category)
admin.site.register(Comment)

