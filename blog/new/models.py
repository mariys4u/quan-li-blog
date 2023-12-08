from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
import re

def remove_vi_accent(s):
    s = re.sub(r'à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ','a', s, flags = re.MULTILINE)
    s = re.sub(r'è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ','e', s, flags = re.MULTILINE)
    s = re.sub(r'ì|í|ị|ỉ|ĩ','i', s, flags = re.MULTILINE)
    s = re.sub(r'ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ','o', s, flags = re.MULTILINE)
    s = re.sub(r'ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ','u', s, flags = re.MULTILINE)
    s = re.sub(r'ỳ|ý|ỵ|ỷ|ỹ','y', s, flags = re.MULTILINE)
    s = re.sub(r'đ','d', s, flags = re.MULTILINE)
    s = re.sub(r'À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ','A', s, flags = re.MULTILINE)
    s = re.sub(r'È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ','E', s, flags = re.MULTILINE)
    s = re.sub(r'Ì|Í|Ị|Ỉ|Ĩ','I', s, flags = re.MULTILINE)
    s = re.sub(r'Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ','O', s, flags = re.MULTILINE)
    s = re.sub(r'Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ','U', s, flags = re.MULTILINE)
    s = re.sub(r'Ỳ|Ý|Ỵ|Ỷ|Ỹ','Y', s, flags = re.MULTILINE)
    s = re.sub(r'Đ', 'D', s, flags = re.MULTILINE)
    
    return s

def get_slug(s, split_char='-'):
    s = s.strip()
    s = re.sub(r' ', split_char, s, flags=re.MULTILINE)
    return s


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    quotation = models.TextField()
    content = models.TextField()
    images = models.ImageField(upload_to='photos/articles/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        self.slug = get_slug(remove_vi_accent(self.title))
        super(Article, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse('article_detail', args=[self.category.slug, self.slug])