import pytest
from tests.utils.constants import ERR_PHONE_REGISTERED, ERR_INVALID_PHONE, ERR_EXPIRED_OTP, ERR_LOCKOUT

def test_tc_reg_027_phone_number_leading_trailing_spaces(otp_service):
    res = otp_service.send_otp("  081299998888  ")
    assert res["status"] == "SUCCESS"

def test_tc_reg_031_plus62_and_08_equivalence(otp_service):
    with pytest.raises(ValueError, match=ERR_PHONE_REGISTERED):
        otp_service.send_otp("+6281234567890")

def test_tc_reg_038_sql_injection_input_handling(otp_service):
    with pytest.raises(ValueError, match=ERR_INVALID_PHONE):
        otp_service.send_otp("081234'; DROP TABLE users;--")

def test_tc_reg_invalid_phone_format_branches(otp_service):
    # String kosong / None
    with pytest.raises(ValueError, match=ERR_INVALID_PHONE):
        otp_service.send_otp("")

    # Digit kurang dari batas minimal
    with pytest.raises(ValueError, match=ERR_INVALID_PHONE):
        otp_service.send_otp("08123")

    # Format +62 dengan seluruh angka nol
    with pytest.raises(ValueError, match=ERR_INVALID_PHONE):
        otp_service.send_otp("+620000000000")

    # Prefix non-08 / non-+62
    with pytest.raises(ValueError, match=ERR_INVALID_PHONE):
        otp_service.send_otp("02112345678")

    # Verifikasi nomor yang belum minta OTP
    with pytest.raises(ValueError, match=ERR_EXPIRED_OTP):
        otp_service.verify_otp("081200001111", "123456")

def test_tc_reg_lockout_expiration_and_recovery(otp_service, monkeypatch):
    phone = "081288889999"
    otp_service.send_otp(phone)

    # Trigger lockout (3x salah)
    for _ in range(2):
        with pytest.raises(ValueError):
            otp_service.verify_otp(phone, "000000")
    with pytest.raises(PermissionError, match=ERR_LOCKOUT):
        otp_service.verify_otp(phone, "000000")

    # Simulasi waktu berjalan melewati 15 menit (900 detik) lockout
    import time
    current_time = time.time()
    monkeypatch.setattr(time, "time", lambda: current_time + 950)

    # Setelah lockout habis, user bisa kirim OTP baru lagi
    res = otp_service.send_otp(phone)
    assert res["status"] == "SUCCESS"