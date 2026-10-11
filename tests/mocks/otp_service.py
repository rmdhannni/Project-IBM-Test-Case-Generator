import time
from typing import Dict, Tuple
from tests.utils.constants import (
    OTP_EXPIRY_SECONDS,
    LOCKOUT_DURATION_SECONDS,
    MAX_FAILED_OTP_ATTEMPTS,
    ERR_INVALID_OTP,
    ERR_EXPIRED_OTP,
    ERR_EMPTY_OTP,
    ERR_LOCKOUT,
    ERR_PHONE_REGISTERED,
    ERR_NETWORK
)
from tests.utils.phone_validator import normalize_phone_number

class MockOTPService:
    def __init__(self):
        self.registered_users = {"+6281234567890"}
        self.otp_store: Dict[str, Tuple[str, float]] = {}
        self.failed_attempts: Dict[str, int] = {}
        self.lockout_until: Dict[str, float] = {}

    def send_otp(self, phone_number: str, network_online: bool = True) -> Dict[str, str]:
        if not network_online:
            raise ConnectionError(ERR_NETWORK)

        normalized = normalize_phone_number(phone_number)

        current_time = time.time()
        if normalized in self.lockout_until:
            if current_time < self.lockout_until[normalized]:
                raise PermissionError(ERR_LOCKOUT)
            else:
                del self.lockout_until[normalized]
                self.failed_attempts[normalized] = 0

        if normalized in self.registered_users:
            raise ValueError(ERR_PHONE_REGISTERED)

        generated_otp = "123456"
        self.otp_store[normalized] = (generated_otp, current_time + OTP_EXPIRY_SECONDS)
        return {"status": "SUCCESS", "message": "OTP berhasil dikirim", "otp": generated_otp}

    def verify_otp(self, phone_number: str, otp: str, network_online: bool = True) -> bool:
        if not network_online:
            raise ConnectionError(ERR_NETWORK)

        if not otp or otp.strip() == "":
            raise ValueError(ERR_EMPTY_OTP)

        if not otp.isdigit() or len(otp) != 6:
            raise ValueError(ERR_INVALID_OTP)

        normalized = normalize_phone_number(phone_number)
        current_time = time.time()

        if normalized in self.lockout_until and current_time < self.lockout_until[normalized]:
            raise PermissionError(ERR_LOCKOUT)

        if normalized not in self.otp_store:
            raise ValueError(ERR_EXPIRED_OTP)

        stored_otp, expiry_time = self.otp_store[normalized]

        if current_time > expiry_time:
            del self.otp_store[normalized]
            raise ValueError(ERR_EXPIRED_OTP)

        if otp != stored_otp:
            attempts = self.failed_attempts.get(normalized, 0) + 1
            self.failed_attempts[normalized] = attempts
            if attempts >= MAX_FAILED_OTP_ATTEMPTS:
                self.lockout_until[normalized] = current_time + LOCKOUT_DURATION_SECONDS
                raise PermissionError(ERR_LOCKOUT)
            raise ValueError(ERR_INVALID_OTP)

        # Successful verification resets state & registers user
        del self.otp_store[normalized]
        self.failed_attempts[normalized] = 0
        self.registered_users.add(normalized)
        return True