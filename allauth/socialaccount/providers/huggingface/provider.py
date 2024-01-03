from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class HuggingFaceAccount(ProviderAccount):
    def get_profile_url(self):
        # "https://huggingface.co/oauth/userinfo" ?
        return self.account.extra_data.get("html_url")

    def get_avatar_url(self):
        # Assuming Hugging Face provides avatar URL in the user data
        return self.account.extra_data.get("avatar_url")

    def to_str(self):
        dflt = super(HuggingFaceAccount, self).to_str()
        # Adapt according to the data provided by Hugging Face
        return next(
            value
            for value in (
                self.account.extra_data.get("name", None),
                self.account.extra_data.get("username", None),
                dflt,
            )
            if value is not None
        )


class HuggingFaceProvider(OAuth2Provider):
    id = "huggingface"
    name = "Hugging Face"
    account_class = HuggingFaceAccount

    def get_default_scope(self):
        # Set the default scope as needed, starting with openid and profile
        scope = ["openid", "profile"]
        if app_settings.QUERY_EMAIL:
            scope.append("email")
        return scope

    def extract_uid(self, data):
        # Extract UID from the Hugging Face user data
        return str(data["id"])

    def extract_common_fields(self, data):
        # Extract fields from the Hugging Face user data
        return dict(
            email=data.get("email"),
            username=data.get("username"),
            name=data.get("name"),
        )


provider_classes = [HuggingFaceProvider]
