from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.organisation.views import CreateOrganisationView, serve_qr_code_image, CreateLoginView, LoginInfoView, \
    LoginDisallowView, LoginAllowView, EditOrganisationView

urlpatterns = [
    url(r'^$', login_required(CreateOrganisationView.as_view()), name='organisation-index'),
    url(r'^edit/(?P<id>\w[-\w]*)/$', EditOrganisationView.as_view(), name='organisation-edit-item'),
    url(r'^qr/$', serve_qr_code_image, name='serve_qr_code_image'),
    url(r'^create_login/$', CreateLoginView.as_view(), name='create_login'),
    url(r'^login/info/$', LoginInfoView.as_view(), name='login_info'),
    url(r'^login/allow/$', LoginAllowView.as_view(), name='login_allow'),
    url(r'^login/disallow/$', LoginDisallowView.as_view(), name='login_disallow'),
    # url(r'^change-password/$',
    #     login_required(self.change_password_view.as_view()),
    #     name='change-password'),
]