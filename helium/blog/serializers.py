from rest_framework import serializers, pagination

from .models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    """
    SlugRelatedField 用来配置外键数据。
    read_only 来定义外键是否可写
    many 多对多关系要设置为 True
    slug_filed 用来指定要展示的字段是什么
    """
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'created_time']


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content', 'created_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time']


class CategoryDetailSerializer(CategorySerializer):
    """
    SerializerMethodField 的作用是把 posts 字段获取的内容映射到 paginated_posts 方法上
    """
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'rquest':self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'precious': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'posts']