from django.shortcuts import render, get_object_or_404
from .models import Article, Category

# Create your views here.
def new(request, category_slug=None):
    categories = None
    articles = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        articles = Article.objects.filter(category=categories).order_by('title')
        acticle_count = Article.objects.filter(category=categories).count()
 
    else:
        articles = Article.objects.all().order_by('category')
        acticle_count = Article.objects.all().count()
        
    context = {
        'articles':articles,
        'acticle_count':acticle_count,
    }
    
    return render(request,'news/new.html', context)

def article_detail(request, category_slug, article_slug):
    try:
        single_article = Article.objects.get(category__slug=category_slug, slug=article_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_article':single_article,
    }
    
    return render(request,'news/article_detail.html', context)