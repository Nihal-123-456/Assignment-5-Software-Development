from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import FormView,ListView
from .forms import *
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from book.models import *
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

def send_mail(user,amount,subject,template):
    message = render_to_string(template,{
        'user': user,
        'amount': amount
    })
    send_mail = EmailMultiAlternatives(subject, '', to=[user.email])
    send_mail.attach_alternative(message, 'text/html')
    send_mail.send()

class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Signup Successful')
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'signup.html'
    def get_success_url(self):
        messages.success(self.request, 'Signin Successful')
        return reverse_lazy('home')

class UserLogoutView(LoginRequiredMixin, LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')

class UserUpdateView(LoginRequiredMixin, View):
    template_name = 'signup.html'

    def get(self, request):
        form = UpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Profile updated successfully')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

class DepositMoneyView(LoginRequiredMixin, FormView):
    template_name = 'signup.html'
    form_class = DepositForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        user_info = self.request.user.info

        user_info.balance += amount
        user_info.save()

        send_mail(self.request.user, amount, 'Deposit Money', 'deposit_mail.html')
        messages.success(self.request, f'Successfully deposited {amount} Taka.')
        return super().form_valid(form)
    
class BorrowBookView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        history = BorrowingHistory.objects.filter(user=request.user, book=book)
        if history.exists():
            messages.warning(request,"You have already borrowed this book")
            return redirect('book_detail',id=book.id)
        else:
            if request.user.info.balance >= book.borrowing_price:
                request.user.info.balance -= book.borrowing_price
                request.user.info.save()

                BorrowingHistory.objects.create(user=request.user, book=book, borrowed_amount=book.borrowing_price)

                messages.success(request, f'You have successfully borrowed "{book.title}".')

                subject = 'Borrowing Book'
                message = render_to_string('borrow_mail.html',{
                'user': request.user,
                'book': book,
                })
                send_mail = EmailMultiAlternatives(subject, '', to=[request.user.email])
                send_mail.attach_alternative(message, 'text/html')
                send_mail.send()

                return redirect('borrow_report')
            else:
                messages.warning(request, 'Not enough balance to borrow book.')
                return redirect('book_detail', id=book.id)

class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, borrowing_id):
        borrowing_history = get_object_or_404(BorrowingHistory, id=borrowing_id)

        request.user.info.balance += borrowing_history.borrowed_amount
        request.user.info.save()

        messages.success(request, f'You have successfully returned {borrowing_history.book.title}.')
        borrowing_history.delete()
        return redirect('borrow_report')

class BorrowReport(LoginRequiredMixin, ListView):
    template_name = 'borrow_report.html'
    model = BorrowingHistory
    context_object_name = 'BorrowingReport'
    def get_queryset(self):
        user = self.request.user
        queryset = BorrowingHistory.objects.filter(user=user)
        return queryset