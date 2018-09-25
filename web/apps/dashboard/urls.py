from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.dashboard.views import IndexView

urlpatterns = [
    url(r'^', login_required(IndexView.as_view()), name='index'),
    # url(r'^change-password/$',
    #     login_required(self.change_password_view.as_view()),
    #     name='change-password'),
]