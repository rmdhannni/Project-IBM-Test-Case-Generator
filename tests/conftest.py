import pytest
from tests.mocks.otp_service import MockOTPService

@pytest.fixture
def otp_service():
    return MockOTPService()