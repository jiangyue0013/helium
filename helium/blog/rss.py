from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handlder, item):
        super(ExtendedRSSFeed, self).add_item_elements(handlder, item)
        handlder.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    feed_type = Rss201rev2Feed  # 可以不写，默认是 Rss201revFeed
    title = "Helium 博客系统"
    link = "/rss/"
    description = "Helium is a blog system powered by django inspired by the5fire"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.desc
    
    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])
    
    def item_extra_kwargs(self, item):
        return {"content_html": self.item_content_html(item)}