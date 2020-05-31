from .models import NewsItem, ScrapeRecord

from django.contrib import admin


class NewsItemAdmin(admin.ModelAdmin):
    list_display = [
        'source',
        'link',
        'title',
        'publish_date'
    ]


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(ScrapeRecord)
