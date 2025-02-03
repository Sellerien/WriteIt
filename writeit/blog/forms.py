from django import forms

from .models import Category, Post, PostComment


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    error_messages = {
        'title': {
            'required': 'Пожалуйста, введите название поста.'
        },}
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'cat']
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Пожалуйста, введите название поста.')
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['text']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }