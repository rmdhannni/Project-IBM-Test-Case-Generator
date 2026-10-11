# Test Suite — Registrasi Akun Baru (Phone Number + OTP)

Automated test suite untuk fitur **Registrasi Akun Baru** menggunakan nomor HP Indonesia.
Ditulis dengan **Python + pytest**, tanpa dependency eksternal selain pytest.

---

## Struktur Project

```
tests/
├── conftest.py                          # Fixtures & shared test data
├── utils/
│   └── phone_validator.py               # Validasi format nomor HP & OTP
├── mocks/
│   └── otp_service.py                   # In-memory mock OTP service
└── registration/
    ├── test_registration_positive.py    # TC_REG_001–003, 022–023
    ├── test_registration_negative.py    # TC_REG_004–012, 024–030
    └── test_registration_edge.py        # TC_REG_013–020, 031–038
```

---

## Cara Menjalankan

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan semua test

```bash
pytest
```

### 3. Jalankan per kategori

```bash
# Hanya positive cases
pytest tests/registration/test_registration_positive.py

# Hanya negative cases
pytest tests/registration/test_registration_negative.py

# Hanya edge cases
pytest tests/registration/test_registration_edge.py
```

### 4. Jalankan dengan coverage report

```bash
pytest --cov=tests --cov-report=term-missing
```

### 5. Jalankan test case tertentu berdasarkan nama

```bash
# Contoh: jalankan semua test yang mengandung kata "lockout"
pytest -k "lockout"

# Contoh: jalankan class test tertentu
pytest tests/registration/test_registration_negative.py::TestTC_REG_008
```

---

## Ringkasan Coverage

| File | Cakupan TC | Jumlah Test |
|---|---|---|
| `test_registration_positive.py` | TC_REG_001–003, 022–023 | Positive / Happy Path |
| `test_registration_negative.py` | TC_REG_004–012, 024–030 | Negative / Error Handling |
| `test_registration_edge.py`     | TC_REG_013–020, 031–038 | Edge Case / BVA / Security |

---

## Desain Arsitektur Mock

```
┌─────────────────────┐     ┌──────────────────────────┐
│   Test File         │────▶│   MockOTPService          │
│ (pytest class)      │     │  - send_otp()             │
└─────────────────────┘     │  - verify_otp()           │
                            │  - is_registered()        │
         ┌──────────────────┤  - force_lock() [helper]  │
         │                  └──────────┬───────────────┘
    FakeClock                          │
  (kontrol waktu)             phone_validator.py
  fake_clock.advance(n)       (validasi format & OTP)
```

- **`MockOTPService`** — menggantikan gateway WhatsApp/SMS dan database. Semua state disimpan in-memory per test.
- **`FakeClock`** — memungkinkan simulasi waktu berlalu (expiry OTP, lockout expire) tanpa `time.sleep()`.
- **`phone_validator.py`** — berisi logika validasi yang sama dengan yang ada di layer production (controller/service).

---

## Asumsi Implementasi

| Kode | Asumsi |
|---|---|
| A1 | Boundary OTP expiry bersifat **inklusif** — OTP di detik ke-120 masih valid; detik ke-121 sudah expired. |
| A2 | Format `+62xxx` dan `08xxx` dinormalisasi ke `08xxx` secara kanonik. |
| A3 | Lockout berlaku per nomor HP (canonical), bukan per device/IP. |
| A4 | Resend OTP **menimpa** OTP sebelumnya (old OTP langsung tidak berlaku). |
| A5 | Counter gagal OTP di-reset ketika OTP baru diterbitkan (bukan hanya saat berhasil). |
