from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition
from qr_code.qrcode.image import PNG_FORMAT_NAME, PilImageOrFallback, SVG_FORMAT_NAME, SvgPathImage
from qr_code.qrcode.maker import make_qr_code_image
from qr_code.qrcode.serve import qr_code_etag, \
    qr_code_last_modified
from qr_code.views import get_qr_code_option_from_request, cache_qr_code
from rest_framework import status, permissions
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.organisation import serializers
from apps.organisation.decorators import allow_user_organisations
from apps.organisation.forms import OrganisationRegisterForm, OrganisationEditForm
from apps.organisation.mixins import RegisterOrganisationMixin, LoginMixin, LoginError, \
    CsrfExemptSessionAuthentication
from apps.organisation.models import OrganisationItem


class CreateOrganisationView(RegisterOrganisationMixin, generic.FormView):
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
        ctx['organisations'] = OrganisationItem.objects.get_user_organisations(self.request.user)
        # ctx['cancel_url'] = safe_referrer(self.request, '')
        return ctx

    def form_valid(self, form):
        self.register_organisation(form)
        return redirect(self.get_redirect())


def get_redirect():
    return reverse('organisation:organisation-index')


@method_decorator(allow_user_organisations, name='dispatch')
class EditOrganisationView(RegisterOrganisationMixin, generic.UpdateView):
    form_class = OrganisationEditForm
    template_name = 'organisation/edit.html'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super(EditOrganisationView, self).get_context_data(**kwargs)

        context['organisation'] = self.request.organisation

        return context

    def get_object(self, queryset=None):
        return self.request.organisation


class CreateLoginView(LoginMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = serializers.CreateLoginSerializer

    def get(self, request, format=None):
        raise MethodNotAllowed('GET')

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            result = self.create_login(ser.public_key)
            return Response({'token': result}, status=status.HTTP_200_OK)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginInfoView(LoginMixin, APIView):
    serializer_class = serializers.CreateLoginSerializer

    def get(self, request, format=None):
        key = self.request.GET.get('key', None)
        if key is None:
            return Response("key required", status=status.HTTP_400_BAD_REQUEST)

        try:
            result = self.get_info(key)
            return Response(result, status=status.HTTP_200_OK)
        except LoginError as e:
            return Response({'message': e.message}, status=e.http_status)

    def post(self, request):
        raise MethodNotAllowed('POST')


class LoginAllowView(LoginMixin, APIView):
    serializer_class = serializers.LoginAllowSerializer

    def get(self, request, format=None):
        raise MethodNotAllowed('GET')

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            try:
                result = self.allow(ser.public_key, ser.auth_token, ser.is_subscribe)
                return Response({'status': result}, status=status.HTTP_200_OK)
            except LoginError as e:
                return Response({'message': e.message}, status=e.http_status)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginDisallowView(LoginMixin, APIView):
    serializer_class = serializers.LoginDisallowSerializer

    def get(self, request, format=None):
        raise MethodNotAllowed('GET')

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            try:
                result = self.disallow(ser.public_key)
                return Response({'status': result}, status=status.HTTP_200_OK)
            except LoginError as e:
                return Response({'message': e.message}, status=e.http_status)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@condition(etag_func=qr_code_etag, last_modified_func=qr_code_last_modified)
@cache_qr_code()
def serve_qr_code_image(request):
    """Serve an image that represents the requested QR code."""
    qr_code_options = get_qr_code_option_from_request(request)
    text = request.GET.get('text', '')

    text = "{'type': 'login', value: '" + text + "'}"
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
