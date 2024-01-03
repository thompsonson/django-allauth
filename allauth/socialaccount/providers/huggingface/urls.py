from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import HuggingFaceProvider


urlpatterns = default_urlpatterns(HuggingFaceProvider)
