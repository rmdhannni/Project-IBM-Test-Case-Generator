import pytest
from tests.utils.constants import (
    ERR_INVALID_PHONE,
    ERR_PHONE_REGISTERED,
    ERR_EMPTY_OTP,
    ERR_INVALID_OTP,
    ERR_EXPIRED_OTP,
    ERR_LOCKOUT,
    ERR_NETWORK
)

def test_tc_reg_004_already_registered_number(otp_service):
    with pytest.raises(ValueError, match=ERR_PHONE_REGISTERED):
        otp_service.send_otp("081234567890")

def test_tc_reg_025_empty_otp_submission(otp_service):
    phone = "081211112222"
    otp_service.send_otp(phone)
    with pytest.raises(ValueError, match=ERR_EMPTY_OTP):
        otp_service.verify_otp(phone, "")

def test_tc_reg_028_network_disconnected_send_otp(otp_service):
    with pytest.raises(ConnectionError, match=ERR_NETWORK):
        otp_service.send_otp("081211113333", network_online=False)

def test_tc_reg_029_network_disconnected_verify_otp(otp_service):
    phone = "081211114444"
    otp_service.send_otp(phone)
    with pytest.raises(ConnectionError, match=ERR_NETWORK):
        otp_service.verify_otp(phone, "123456", network_online=False)

def test_tc_reg_030_phone_number_all_zeros(otp_service):
    with pytest.raises(ValueError, match=ERR_INVALID_PHONE):
        otp_service.send_otp("000000000000")

def test_tc_reg_expired_otp(otp_service, monkeypatch):
    phone = "081255556666"
    otp_service.send_otp(phone)
    
    # Simulasi waktu berjalan melampaui batas expired (120 detik)
    import time
    current_time = time.time()
    monkeypatch.setattr(time, "time", lambda: current_time + 150)
    
    with pytest.raises(ValueError, match=ERR_EXPIRED_OTP):
        otp_service.verify_otp(phone, "123456")

def test_tc_reg_lockout_trigger(otp_service):
    phone = "081277778888"
    otp_service.send_otp(phone)
    
    # Percobaan salah ke-1 & 2
    with pytest.raises(ValueError, match=ERR_INVALID_OTP):
        otp_service.verify_otp(phone, "000000")
    with pytest.raises(ValueError, match=ERR_INVALID_OTP):
        otp_service.verify_otp(phone, "000000")
        
    # Percobaan salah ke-3 memicu lockout
    with pytest.raises(PermissionError, match=ERR_LOCKOUT):
        otp_service.verify_otp(phone, "000000")

    # Upaya pengiriman & verifikasi baru saat masih ter-lockout
    with pytest.raises(PermissionError, match=ERR_LOCKOUT):
        otp_service.send_otp(phone)
    with pytest.raises(PermissionError, match=ERR_LOCKOUT):
        otp_service.verify_otp(phone, "123456")