"""helium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .custom_site import custom_site
from blog.apis import PostViewSet, CategoryViewSet
from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView
)
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from comment.views import CommentView
from config.views import LinkListView


router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')


urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name="index"),
    re_path(r'^links/$', LinkListView.as_view(), name="links"),
    re_path(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name="author"),
    re_path(r'^search/$', SearchView.as_view(), name="search"),
    re_path(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name="category-list"),
    re_path(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name="tag-list"),
    re_path(r'^post/(?P<post_id>\d+)/$', PostDetailView.as_view(), name="post-detail"),
    re_path(r'^comment/$', CommentView.as_view(), name="comment"),
    re_path(r'^rss|feed/$', LatestPostFeed(), name="rss"),
    re_path(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # re_path(r'^api/post/', post_list, name="post-list"),
    # re_path(r'^api/post/', PostList.as_view(), name="post-list"),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^super_admin/', admin.site.urls, name="super-admin"),
    re_path(r'^admin/', custom_site.urls, name="admin"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^silk/', include('silk.urls', namespace='silk')),
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
