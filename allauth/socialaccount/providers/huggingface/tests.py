from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import HuggingFaceProvider


class HuggingFaceTests(OAuth2TestsMixin, TestCase):
    provider_id = HuggingFaceProvider.id

    def get_mocked_response(self):
        # Replace with Hugging Face's user data format
        return [
            MockedResponse(
                200,
                """
                {
                    "id": "1234567890",
                    "sub": "1234567890",
                    "name": "John Doe",
                    "username": "johndoe",
                    "picture": "https://huggingface.co/avatar.jpg",
                    "updated_at": "2021-01-01T00:00:00.000Z",
                    "email": "johndoe@example.com",
                    "email_verified": true
                }""",
            ),
        ]

    def test_account_name_null(self):
        # Test for null name in Hugging Face's user data
        mocks = [
            MockedResponse(
                200,
                """
                {
                    "id": "1234567890",
                    "sub": "1234567890",
                    "name": null,
                    "username": "johndoe",
                    "picture": "https://huggingface.co/avatar.jpg",
                    "updated_at": "2021-01-01T00:00:00.000Z",
                    "email": "johndoe@example.com",
                    "email_verified": true
                }""",
            ),
        ]
        self.login(mocks)
        socialaccount = SocialAccount.objects.get(uid="1234567890")
        self.assertIsNone(socialaccount.extra_data.get("name"))
        account = socialaccount.get_provider_account()
        self.assertIsNotNone(account.to_str())
        self.assertEqual(account.to_str(), "johndoe")
        self.assertEqual(socialaccount.user.email, "johndoe@example.com")
