from django.shortcuts import render
from book.models import *

# Create your views here.
def HomeView(request, category_slug = None):
    books = Book.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        books = Book.objects.filter(category  = category)
    categories = Category.objects.all()
    return render(request, 'home.html', {'books' : books, 'category' : categories})