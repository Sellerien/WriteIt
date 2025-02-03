from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.db.models import Q

from .utils import DataMixin
from .models import Post, Category, PostComment
from .forms import AddPostForm, CommentForm


class BlogHome(DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Post.objects.all()


class ShowPost(DetailView):
    template_name = 'blog/post.html'
    id_url_kwarg = 'post_pk'
    context_object_name = 'post'
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()  
        context['form'] = CommentForm() 
        context['is_moderator'] = self.request.user.groups.filter(name="Moderator").exists()
   
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return redirect(self.object.get_absolute_url())
        return self.get(request, *args, **kwargs)
    
    def get_object(self, queryset = None):
        return get_object_or_404(Post.objects, pk=self.kwargs.get(self.pk_url_kwarg))
    
   
class AddPost(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/addpage.html'
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

   
        
class CategoryView(DataMixin, ListView):
    template_name = 'blog/index.html'    
    context_object_name = 'posts'
    allow_empty = False
    
    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, cat_selected=cat.pk)
    

class UpdatePost(UpdateView):
    model = Post
    form_class = AddPostForm
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')
    
    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionError('Вы не автор данной статьи')
        return obj
    

class DeletePost(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')
    
    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.author == self.request.user or self.request.user.is_superuser or self.request.user.groups.filter(name='Moderator').exists():
            return obj
        raise PermissionError('Вы не автор данной статьи')
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Moderator').exists():
            return True
        return self.request.user == comment.author
    

class DeleteComment(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = PostComment
    template_name = 'blog/comment_delete.html'
    
    def get_success_url(self):
        return self.get_object().post.get_absolute_url()
    
    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.author == self.request.user or self.request.user.is_superuser or self.request.user.groups.filter(name='Moderator').exists():
            return obj
        raise PermissionError('Вы не автор данного комментария')
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Moderator').exists():
            return True
        return self.request.user == comment.author
    

class MyPosts(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
    

class ArticleSearchView(DataMixin, ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return Post.objects.all()
