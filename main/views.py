from django.shortcuts import render
from .models import NewsItem
from django.views import generic


class NewsItemListView(generic.ListView):
    model = NewsItem
    template_name = "news_item_list.html"
