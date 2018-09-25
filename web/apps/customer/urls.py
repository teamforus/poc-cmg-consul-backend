from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.customer.views import AccountRegistrationView, AccountAuthView, LogoutView

urlpatterns = [
    url(r'^register/$', (AccountRegistrationView.as_view()), name='register'),
    url(r'^login/$', (AccountAuthView.as_view()), name='login'),
    url(r'^logout/$', (LogoutView.as_view()), name='logout'),
    # url(r'^change-password/$',
    #     login_required(self.change_password_view.as_view()),
    #     name='change-password'),
]