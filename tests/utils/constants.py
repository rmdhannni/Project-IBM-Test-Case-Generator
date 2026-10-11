# Constants for Registration & OTP
OTP_EXPIRY_SECONDS = 120
LOCKOUT_DURATION_SECONDS = 900  # 15 minutes
MAX_FAILED_OTP_ATTEMPTS = 3
DEFAULT_COUNTRY_CODE = "+62"

# Error Messages
ERR_INVALID_PHONE = "Nomor HP tidak valid"
ERR_PHONE_REGISTERED = "Nomor HP sudah terdaftar, silakan login"
ERR_INVALID_OTP = "Kode OTP salah"
ERR_EXPIRED_OTP = "Kode OTP telah kedaluwarsa"
ERR_EMPTY_OTP = "Kode OTP tidak boleh kosong"
ERR_LOCKOUT = "Akun diblokir sementara karena terlalu banyak percobaan salah. Coba lagi dalam 15 menit."
ERR_NETWORK = "Tidak ada koneksi internet, silakan coba lagi"