from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import HuggingFaceProvider


class HuggingFaceOAuth2Adapter(OAuth2Adapter):
    provider_id = HuggingFaceProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {})

    # Set Hugging Face's endpoints
    access_token_url = "https://huggingface.co/oauth/token"
    authorize_url = "https://huggingface.co/oauth/authorize"
    profile_url = "https://huggingface.co/oauth/userinfo"  # User info endpoint

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": f"Bearer {token.token}"}
        resp = (
            get_adapter().get_requests_session().get(self.profile_url, headers=headers)
        )
        resp.raise_for_status()
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(HuggingFaceOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(HuggingFaceOAuth2Adapter)
