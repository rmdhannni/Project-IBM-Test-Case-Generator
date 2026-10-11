# Arsitektur Prompt: Automated Test Case Generator (IBM watsonx / Bob)

Dokumen ini memuat struktur *Prompt Layering* yang dirancang untuk memastikan AI Agent mampu menganalisis kebutuhan perangkat lunak (*Software Requirement Specification*) dan menghasilkan *test case* terstruktur secara presisi dan konsisten.

---

## 1. Struktur Layer

Arsitektur prompt ini dibagi menjadi 5 layer utama:

### Layer 1: System & Role Definition Layer
* **Deskripsi:** Menetapkan peran AI sebagai *Senior Quality Assurance Engineer & Test Automation Specialist* yang mematuhi standar *software testing* (ISO/IEC/IEEE 29119).
* **Tujuan:** Membentuk cara berpikir agent agar bertindak dengan cara pandang QA profesional.

### Layer 2: Context & Domain Constraints Layer
* **Deskripsi:** Menetapkan cakupan wajib pengujian, yaitu *Positive Path*, *Negative Path*, serta *Edge Cases / Boundary Value Analysis (BVA)* dan *Equivalence Partitioning (EP)*.
* **Tujuan:** Mencegah jawaban yang terlalu umum dan memastikan seluruh kemungkinan skenario teruji tanpa ada asumsi yang tidak berdasar.

### Layer 3: Formatting & Output Structuring Layer
* **Deskripsi:** Mengunci format luaran dalam bentuk Markdown terstruktur yang memuat ringkasan kebutuhan serta tabel *test case*.
* **Tujuan:** Menjamin konsistensi format jawaban sehingga data mudah disalin atau diimpor ke sistem seperti Jira atau TestRail.

### Layer 4: Few-Shot Examples (Instruction by Example)
* **Deskripsi:** Memberikan contoh masukan (*input*) dan keluaran (*output*) acuan.
* **Tujuan:** Memberikan acuan konkret kepada AI mengenai gaya penulisan, detail *test step*, dan pemisahan jenis skenario.

### Layer 5: Task Execution & User Input Layer
* **Deskripsi:** Tempat menyisipkan spesifikasi kebutuhan (*User Story / Acceptance Criteria*) yang akan diproses oleh AI Agent.
* **Tujuan:** Mengarahkan Agent untuk mengeksekusi analisis terhadap data spesifik yang diberikan.

---

## 2. Diagram Alur Pemrosesan Prompt

```text
[ User Story / SRS Input ]
           │
           ▼
┌──────────────────────────────────────────┐
│ Layer 1: Role Definition (Senior QA)     │
├──────────────────────────────────────────┤
│ Layer 2: Constraints (Positive/Neg/Edge) │
├──────────────────────────────────────────┤
│ Layer 3: Output Formatting (Markdown)    │
├──────────────────────────────────────────┤
│ Layer 4: Few-Shot Examples               │
└──────────────────────────────────────────┘
           │
           ▼
[ Output: Markdown Test Cases Table ]