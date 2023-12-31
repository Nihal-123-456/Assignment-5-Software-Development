from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
# Create your views here.

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object 
        comments = book.reviews.all()
        
        context['comments'] = comments
        return context
    
class UserReview(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'review.html'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        comment_form = ReviewForm(data=request.POST)
        book = self.get_object()

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = self.request.user
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = ReviewForm()
        
        context['comment_form'] = comment_form
        return context