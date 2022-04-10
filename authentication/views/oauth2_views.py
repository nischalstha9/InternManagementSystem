from django.conf import settings

from rest_framework import serializers
from rest_framework import status
from rest_framework_simplejwt.tokens import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from requests.exceptions import HTTPError

from social_django.utils import psa

from authentication.views import CustomerObtainTokenView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )

class MySocialTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def getToken(self, user):
        refresh = super().get_token(user)

        data = dict()

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.
    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.
    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'
    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.
    ## Request format
    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        # try:
        #     nfe = settings.NON_FIELD_ERRORS_KEY
        # except AttributeError:
        #     nfe = 'email'

        try:
            # this line, plus the psa decorator above, are all that's necessary to
            # get and populate a user object for any properly enabled/configured backend
            # which python-social-auth can handle.
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as exp:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            print(exp)
            return Response(
                {'detail':'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active and user.role == 2:
                refresh = MySocialTokenObtainPairSerializer().getToken(user)
                if request.data.get('request_id', None):
                    merge_cart(request, user.customer)
                return Response(
                    refresh,
                    status=status.HTTP_200_OK,
                )
            else:
                # user is not active; at some point they deleted their account,
                # or were banned by a superuser. They can't just log in with their
                # normal credentials anymore, so they can't log in with social
                # credentials either.
                return Response(
                    {'detail': 'This user account is inactive/invalid'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.
            return Response(
                {'detail': "Authentication Failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )