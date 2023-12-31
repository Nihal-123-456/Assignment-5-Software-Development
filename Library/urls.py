from django.contrib import admin
from django.urls import path
from core.views import *
from book.views import *
from django.conf import settings
from django.conf.urls.static import static
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView, name='home'),
    path('category/<slug:category_slug>/', HomeView, name='category_book'),
    path('book_detail/<int:id>',BookDetailView.as_view(), name='book_detail'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='login'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('deposit_money/', DepositMoneyView.as_view(), name='deposit_money'),
    path('borrow_book/<int:book_id>/', BorrowBookView.as_view(), name='borrow_book'),
    path('borrow_report/', BorrowReport.as_view(), name='borrow_report'),
    path('review/<int:id>', UserReview.as_view(), name='review'),
    path('return_book/<int:borrowing_id>', ReturnBookView.as_view(), name='return_book'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)