# Rancangan Struktur Aplikasi Finance & Journal Invest

## Gambaran Umum
Aplikasi ini terdiri dari dua modul utama:
1. **Finance** - Untuk tracking keuangan personal (wallet, transaksi, kategori)
2. **Journal** - Untuk mencatat dan memantau investasi serta trading (portfolio, asset, transaksi investasi)

Aplikasi dibuat dengan prioritas time-to-market, fokus pada fitur inti yang memberikan nilai langsung kepada pengguna.

## Struktur Menu

### 1. Authentication
- **Login** (`/`)
- **Register** (`/register`)
- **Forget Password** (`/forget-password`)
- **Logout** (`/sign-out`)

### 2. Dashboard (`/en/dashboard/`)
Menampilkan ringkasan dari keseluruhan data dari kedua modul:
- **Statistik Keuangan**
  - Total saldo semua wallet
  - Transaksi terakhir (pemasukan/pengeluaran)
  - Grafik tren pengeluaran per kategori

- **Statistik Investasi & Trading**
  - Jumlah portfolio
  - Performa portfolio (keuntungan/kerugian)
  - Asset allocation chart
  - Grafik nilai portfolio dari waktu ke waktu

- **Notifikasi & Alerts**
  - Dividen yang akan dibayarkan dalam 30 hari ke depan
  - Asset yang mendekati target price (90%+ dari target)
  - Asset yang mendekati stop loss (110%- dari stop loss)
  - Transaksi terbaru yang belum dikategorikan

### 3. Journal (Investasi & Trading)
- **Portfolio List** (`/portos`)
  - Daftar semua portfolio milik user
  - Informasi: Nama portfolio, Akun yang digunakan, Total investasi, P/L (Profit/Loss)
  - Filter berdasarkan: Jenis portfolio (investasi/trading), Sekuritas, Performance
  - Tombol "Tambah Portfolio"

- **Portfolio Detail** (`/porto/{id}`)
  - Nama, deskripsi, dan akun sekuritas
  - Performance metrics (ROI, Unrealized P/L, Realized P/L)
  - Daftar asset dalam portfolio dengan informasi:
    - Untuk Investasi: Nama asset, Jumlah, Avg price, Current price, Total value, Unrealized P/L
    - Untuk Trading: Nama asset, Entry price, Target price, Stop loss, Current price, P/L, Status
  - Timeline transaksi portfolio (buy, sell, dividend)
  - Grafik performa portfolio dari waktu ke waktu
  - Tombol "Tambah Transaksi", "Edit Portfolio", "Tutup Portfolio"

- **Transactions** (`/transactions`)
  - Daftar semua transaksi investasi/trading
  - Filter berdasarkan: Portfolio, Jenis transaksi (buy, sell, dividend), Range tanggal
  - Sorting berdasarkan tanggal, nilai, dll
  - Tombol "Tambah Transaksi"

### 4. Finance (Manajemen Keuangan)
- **Wallet List** (`/wallets`)
  - Daftar semua wallet milik user
  - Informasi: Nama wallet, Tipe wallet, Saldo saat ini, Currency
  - Filter berdasarkan: Tipe wallet, Status
  - Tombol "Tambah Wallet"

- **Wallet Detail** (`/wallet/{id}`)
  - Informasi: Nama, Tipe, Saldo, Mata uang
  - Timeline transaksi wallet
  - Grafik pemasukan vs pengeluaran per bulan/minggu
  - Breakdown pengeluaran berdasarkan kategori
  - Tombol "Tambah Transaksi", "Edit Wallet", "Nonaktifkan Wallet"

- **Transactions** (`/finance/transactions`)
  - Daftar semua transaksi keuangan
  - Filter berdasarkan: Wallet, Kategori, Jenis transaksi (income/expense/transfer), Range tanggal
  - Sorting berdasarkan tanggal, nilai, dll
  - Tombol "Tambah Transaksi"

- **Categories** (`/categories`)
  - Daftar kategori transaksi
  - Informasi: Nama, Jenis (income/expense), Jumlah transaksi, Total
  - Tombol "Tambah Kategori"

### 5. Data & Informasi
- **Asset List** (`/assets`)
  - Daftar semua asset yang tersedia
  - Informasi: Kode, Nama, Tipe asset, Sektor, Harga terkini, % perubahan
  - Filter berdasarkan: Tipe asset, Sektor
  - Detail asset menampilkan:
    - Info umum asset
    - Grafik pergerakan harga
    - Riwayat dividend (jika ada)

- **Sekuritas List** (`/sekuritas`)
  - Daftar semua sekuritas yang tersimpan
  - Informasi: Nama, Deskripsi
  - Detail sekuritas

### 6. Settings
- **Profile Settings** (`/settings/profile`)
  - Edit informasi pribadi
  - Ubah password

- **Notification Settings** (`/settings/notifications`)
  - Atur notifikasi untuk events seperti:
    - Transaksi baru
    - Perubahan harga asset
    - Dividend yang akan datang
    - Target price/stop loss tercapai

## Form & Modal

### Portfolio Forms
1. **Create/Edit Portfolio**
   - Nama portfolio
   - Deskripsi
   - Pilih akun sekuritas
   - Jenis portfolio (investasi/trading)

2. **Add Investment Transaction**
   - Pilih asset
   - Jenis transaksi (buy/sell/dividend)
   - Kuantitas
   - Harga
   - Tanggal transaksi
   - Biaya (fee)
   - Catatan

3. **Add Trading Position**
   - Pilih asset
   - Entry price
   - Target price
   - Stop loss
   - Alasan trading
   - Strategi

### Finance Forms
1. **Create/Edit Wallet**
   - Nama wallet
   - Tipe wallet
   - Saldo awal
   - Mata uang
   - Status

2. **Add Finance Transaction**
   - Pilih wallet
   - Jenis transaksi (income/expense/transfer)
   - Jumlah
   - Kategori
   - Tanggal transaksi
   - Deskripsi
   - Tags

3. **Create/Edit Category**
   - Nama kategori
   - Jenis (income/expense)
   - Icon
   - Warna

## Integrasi & Alur Data

1. **Asset Price Updates**
   - Integrasi dengan API pihak ketiga (jika tersedia)
   - Scheduled tasks untuk update harga asset
   - Flag untuk asset yang perlu diupdate manual

2. **Dividend Tracking**
   - Notifikasi untuk dividend yang akan datang
   - Auto-record dividend payments

3. **Wallet Balance Calculation**
   - Auto-update berdasarkan transaksi yang diinput

4. **Portfolio Valuation**
   - Calculate berdasarkan holding dan harga terkini asset

## Teknologi & Arsitektur

### Backend
- **Django** sebagai framework utama
- **Django REST Framework** untuk API
- Database: SQLite (development), PostgreSQL (production)
- Authentication: Django's built-in auth + JWT untuk API

### Frontend
- **Next.js** sebagai framework React
- State Management: Redux atau Context API
- UI Components: Tailwind CSS + shadcn/ui components
- Chart visualization: Recharts atau Chart.js

### Mobile Responsiveness
- **Adaptive Design** - Layout yang menyesuaikan dengan ukuran layar:
  - Tampilan dashboard yang dioptimalkan untuk mobile (satu kolom)
  - Menu navigasi yang collapse menjadi hamburger menu pada layar kecil
  - Tabel data dengan horizontal scroll atau tampilan kartu pada mobile
  - Form dengan layout adaptif (stacked pada mobile, side-by-side pada desktop)
  - Grafik dan visualisasi yang resize sesuai ukuran layar

- **Touch-Friendly UI**:
  - Button dan elemen interaktif dengan ukuran minimum 44px × 44px
  - Spacing yang cukup antara elemen yang dapat diklik
  - Implementasi swipe gestures untuk navigasi pada tampilan mobile (opsional)
  
- **Progressive Loading**:
  - Prioritaskan loading konten penting terlebih dahulu
  - Implementasi lazy loading untuk data tabel yang panjang
  - Pagination yang optimal untuk mobile view

## Prioritas Pengembangan (Time-to-Market Approach)

### Phase 1: Core Functionality ⚡
1. **Core Backend** (Django Models & Admin)
   - Complete model creation ✅
   - Setup admin interfaces ✅
   - Database migrations ✅
   - API endpoints untuk fitur penting

2. **Authentication System**
   - Login/Register ✅
   - User profile dasar

3. **MVP Frontend**
   - Setup Next.js structure
   - Authentication pages
   - Dashboard sederhana
   - Portfolio list dan detail (Journal)
   - Wallet list dan detail (Finance)
   - Mobile responsiveness dasar

### Phase 2: Feature Enhancement 🚀
1. **Finance Module Lengkap**
   - Transaction management lengkap
   - Categories & tags
   - Reporting dasar

2. **Journal Module Lengkap**
   - Investment & trading transactions lengkap
   - Asset tracking lengkap
   - Performance metrics dasar

3. **UI/UX Enhancements**
   - Dashboard lengkap dengan visualisasi
   - Filters dan sorting
   - Mobile responsiveness lengkap

### Phase 3: Advanced Features 🔮 (Post Time-to-Market)
1. **Analytics & Reports**
   - Financial reports mendalam
   - Investment performance metrics lanjutan
   - Data visualization lanjutan

2. **Notification System**
   - Alerts untuk dividen
   - Alerts untuk target price/stop loss
   - Email notifications

3. **Integrasi**
   - API pihak ketiga untuk harga real-time
   - Export data ke Excel/PDF
   - Backup dan restore data
