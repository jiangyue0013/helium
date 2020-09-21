from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Category, Post, Tag


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label=("摘要"), required=False)
    content = forms.CharField(widget=CKEditorUploadingWidget(), label="正文", required=False)

    class Meta:
        model = Post
        fields = (
            'category', 'tag', 'desc', 'title',
            'content', 'status',
        )

    class Media:
        # js = ('js/post_editor.js', 'js/jquery.min.js', )  # 最后要 , 结束
        pass
