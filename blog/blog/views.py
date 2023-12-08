from django.shortcuts import render
from new.models import Article
def home(request):
    articles = Article.objects.all()
    
    context={
        'articles': articles
    }
    return render(request, 'home.html', context)