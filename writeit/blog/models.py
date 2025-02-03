from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import get_user_model


class Post(models.Model):
    title = models.CharField(max_length=64, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Отредактировано")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None, verbose_name="Автор")
    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['time_create'])
        ]
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    
class Category(models.Model):
    name = models.CharField(max_length=32, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=32, unique=True, db_index=True)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class PostComment(models.Model):
    text = models.TextField(verbose_name="Комментарий", validators=[MaxLengthValidator(360)])
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        ordering = ['-time_create']