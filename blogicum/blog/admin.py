from django.contrib import admin
from .models import Post, Category, Location


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'pub_date',
        'is_published',
        'category',
        'location'
    )
    list_filter = ('is_published', 'pub_date', 'category')
    search_fields = ('title', 'text')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Location)
