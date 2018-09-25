from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from qr_code import views

from apps.organisation.views import RegistraterView, serve_qr_code_image

urlpatterns = [
    url(r'^$', login_required(RegistraterView.as_view()), name='organisation-index'),
    url(r'^qr/$', serve_qr_code_image, name='serve_qr_code_image')
    # url(r'^change-password/$',
    #     login_required(self.change_password_view.as_view()),
    #     name='change-password'),
]