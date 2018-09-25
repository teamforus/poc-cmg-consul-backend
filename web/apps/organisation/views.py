import base64
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import condition
from qr_code.qrcode.image import PNG_FORMAT_NAME, PilImageOrFallback, SVG_FORMAT_NAME, SvgPathImage
from qr_code.qrcode.maker import make_qr_code_image
from qr_code.qrcode.serve import qr_code_etag, \
    qr_code_last_modified
from qr_code.views import get_qr_code_option_from_request, cache_qr_code

from apps.organisation.forms import OrganisationRegisterForm
from apps.organisation.mixins import RegisterOrganisationMixin
from apps.organisation.models import Organisation


class RegistraterView(RegisterOrganisationMixin, generic.FormView):
    form_class = OrganisationRegisterForm
    template_name = 'organisation/index.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        return super().get(
            request, *args, **kwargs)

    def get_redirect(self):
        return reverse('organisation:organisation-index')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        ctx['organisations'] = Organisation.objects.get_user_organisations(self.request.user)
        # ctx['cancel_url'] = safe_referrer(self.request, '')
        return ctx

    def form_valid(self, form):
        self.register_organisation(form)
        return redirect(self.get_redirect())


@condition(etag_func=qr_code_etag, last_modified_func=qr_code_last_modified)
@cache_qr_code()
def serve_qr_code_image(request):
    """Serve an image that represents the requested QR code."""
    qr_code_options = get_qr_code_option_from_request(request)
    text = request.GET.get('text', '')

    text = "{'type': 'login', value: '"+ text + "'}"
    img = make_qr_code_image(text,
                             image_factory=SvgPathImage if qr_code_options.image_format == SVG_FORMAT_NAME else PilImageOrFallback,
                             qr_code_options=qr_code_options)

    # Warning: The largest QR codes, in version 40, with a border of 4 modules, and rendered in SVG format, are ~800
    # KB large. This can be handled in memory but could cause troubles if the server needs to generate thousands of
    # those QR codes within a short interval! Note that this would also be a problem for the CPU. Such QR codes needs
    # 0.7 second to be generated on a powerful machine (2017), and probably more than one second on a cheap hosting.
    stream = BytesIO()
    if qr_code_options.image_format == SVG_FORMAT_NAME:
        img.save(stream, kind=SVG_FORMAT_NAME.upper())
        mime_type = 'image/svg+xml'
    else:
        img.save(stream, format=PNG_FORMAT_NAME.upper())
        mime_type = 'image/png'

    # Go to the beginning of the stream.
    stream.seek(0)

    # Build the response.
    response = HttpResponse(content=stream, content_type=mime_type)
    return response
