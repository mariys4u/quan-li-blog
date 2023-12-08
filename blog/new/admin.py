from django.contrib import admin
from .models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('title', 'slug', 'category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Article, ArticleAdmin)

