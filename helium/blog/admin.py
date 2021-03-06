from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .adminforms import PostAdminForm
from .models import Category, Post, Tag
from helium.custom_site import custom_site
from helium.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 2
    model = Post

@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    
    def post_count(self, obj):
        return obj.post_set.count()
    
    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator', 'uv',
        'pv'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    save_on_top = True

    actions_on_top = True
    actions_on_bottom = True

    fieldsets = (
        ('基础配置', {
            'description': '设置文章的标题、分类和状态。',
            'fields': (
                ('title', 'category'),
                ('status',),
            ),
        }),
        ('内容', {
            'description': '设置文章的摘要和内容。',
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'description': '设置文章的标签',
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )
    filter_horizontal = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'
    
    class Media:
        # # 引入自定义的 css 和 js 文件
        # css = {
        #     'all':('URI')
        # }
        # js = ('URI')
        # js=('js/jquery.min.js',)
        pass