from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = 'polls'
urlpatterns = [
    path('', login_required(views.IndexView.as_view()), name='index'),
    # ex: /polls/5/
    path('<int:pk>/', login_required(views.DetailView.as_view()), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results/', login_required(views.ResultsView.as_view()), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', login_required(views.vote), name='vote'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', login_required(views.profile), name='profile'),
    path('address_book/personal', login_required(views.PersonalAddressBookView.as_view()), name='personal_address_book'),
    path('address_book/work', login_required(views.WorkAddressBookView.as_view()), name='work_address_book'),
    path('contact/<int:contact_id>', login_required(views.contact), name='contact'),
    path('contact/delete/<int:contact_id>', login_required(views.contact_delete), name='contact_delete'),
    ] 

