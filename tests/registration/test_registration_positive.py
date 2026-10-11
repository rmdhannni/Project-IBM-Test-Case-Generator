import pytest

def test_tc_reg_001_positive_valid_registration(otp_service):
    phone = "081298765432"
    res = otp_service.send_otp(phone)
    assert res["status"] == "SUCCESS"
    assert otp_service.verify_otp(phone, res["otp"]) is True

def test_tc_reg_021_resend_otp_successfully(otp_service):
    phone = "081298765431"
    res1 = otp_service.send_otp(phone)
    res2 = otp_service.send_otp(phone)
    assert res1["otp"] == res2["otp"]  # Mock generated constant
    assert otp_service.verify_otp(phone, res2["otp"]) is True

def test_tc_reg_023_otp_counter_resets_on_success(otp_service):
    phone = "081298765430"
    res = otp_service.send_otp(phone)
    with pytest.raises(ValueError, match="Kode OTP salah"):
        otp_service.verify_otp(phone, "000000")
    with pytest.raises(ValueError, match="Kode OTP salah"):
        otp_service.verify_otp(phone, "000000")
    # 3rd attempt is correct -> Success
    assert otp_service.verify_otp(phone, res["otp"]) is True