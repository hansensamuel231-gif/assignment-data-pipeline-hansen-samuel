
# Data Engineering: Pipeline & Preparation

## 1. Deskripsi & Sumber Dataset
* **Deskripsi Singkat Dataset**: Dataset ini berisi informasi spesifik mengenai spesifikasi kendaraan mobil (*automobile*), termasuk atribut teknis, ukuran, dan harga pasar kendaraan.
* **Sumber Dataset**: File data mentah diperoleh dari direktori project pada file `automobileEDA_dirty_training.csv` di dalam folder `data/raw/`.



## 2. Struktur Folder Project
Struktur direktori penyimpanan project ini disusun secara rapi dan terorganisir sebagai berikut:
```text
project-folder/
│
├── data/
│   ├── raw/
│   │   └── automobileEDA_dirty_training.csv
│   └── processed/
│       └── automobileEDA_processed.csv
│
├── documentation/
│   └── data-flow-diagram.png
│
├── pipeline.py
└── README.md

```

---

## 3. Pemahaman & Pemeriksaan Awal Dataset (Data Inspection)

Pada tahap awal ini, dataset mentah (`automobileEDA_dirty_training.csv`) dimuat menggunakan Pandas di dalam script `pipeline.py` untuk dianalisis struktur dan kualitasnya.

### **A. Ringkasan Ukuran & Struktur Data**

* **Ukuran Dataset**: Terdiri dari **205 baris** dan **30 kolom**.
* **Struktur Tipe Data**: Terdiri dari 11 kolom bertipe desimal (`float64`), 8 kolom bertipe angka bulat (`int64`), dan 11 kolom bertipe teks/string (`str`).
* **Contoh Kolom Penting**: `transaction_date`, `make`, `body-style`, `horsepower`, `price`, dan lain-lain.

### **B. Identifikasi Permasalahan Kualitas Data (Data Quality Issues)**

Berdasarkan hasil eksekusi terminal, ditemukan beberapa masalah krusial yang wajib dibersihkan:

1. **Missing Values (Data Kosong):**
* Ditemukan beberapa kolom yang memiliki data bolong/kosong, yaitu pada kolom `transaction_date` (2 baris), `make` (2 baris), `num-of-doors` (2 baris), `stroke` (4 baris), `horsepower` (3 baris), `price` (3 baris), dan `horsepower-binned` (1 baris).


2. **Baris Terduplikasi (Duplicate Records):**
* Ditemukan **4 baris data ganda (duplikat)** secara keseluruhan yang dapat mendistorsi (membiaskan) hasil analisis statistik jika tidak dihapus.


3. **Tipe Data yang Belum Sesuai:**
* Kolom `transaction_date` terbaca sebagai teks biasa (`str`), padahal seharusnya bertipe format waktu (*datetime*) agar valid diolah secara kronologis.


4. **Inkonsistensi Penulisan Kategori:**
* Pada kolom kategorikal (seperti merek mobil/`make`), ditemukan variasi penulisan huruf besar dan kecil yang tidak seragam, sehingga komputer membacanya sebagai entitas/kategori yang berbeda.



---

## 4. Tahap Pembersihan Data (Data Cleaning) & Alasannya

Pada tahap ini, script `pipeline.py` mengeksekusi proses pembersihan data (*data cleaning*) untuk mengatasi berbagai permasalahan kualitas data.

### **A. Ringkasan Perubahan Jumlah Data**

* **Jumlah data sebelum *cleaning***: 205 baris dan 30 kolom.
* **Jumlah baris duplikat yang dihapus**: 4 baris.
* **Jumlah data sesudah *cleaning***: 201 baris dan 30 kolom (setelah baris duplikat dibuang dan data kosong ditangani).

### **B. Rincian Permasalahan, Kolom, Metode, dan Alasannya**

| Permasalahan yang Ditemukan | Kolom yang Dibersihkan | Metode Cleaning yang Digunakan | Alasan Pemilihan Metode Tersebut |
| --- | --- | --- | --- |
| **Baris Duplikat** | Seluruh kolom tabel | Menghapus baris kembar menggunakan fungsi `drop_duplicates()` | Baris duplikat yang identik secara keseluruhan dapat mendistorsi (*biasing*) hasil analisis statistik maupun pemodelan data. |
| **Missing Values (Kolom Numerik)** | `stroke`, `horsepower`, `price` | Melakukan imputasi dengan nilai rata-rata (*mean*) menggunakan `fillna()` | Nilai rata-rata menjaga agar distribusi angka numerik tidak mengalami pergeseran drastis dibandingkan jika baris datanya langsung dihapus (*drop*). |
| **Missing Values (Kolom Kategorikal)** | `transaction_date`, `make`, `num-of-doors`, `horsepower-binned` | Melakukan imputasi dengan nilai modus (*mode* / nilai yang paling sering muncul) | Karena kolom berupa teks/kategori, modus adalah representasi paling logis untuk mengisi bagian data yang kosong. |
| **Inkonsistensi Teks Kategori** | `make` (merek mobil) | Menyeragamkan huruf kecil (*lowercase*) dan menghapus spasi tepi (*strip*) | Mencegah komputer memperlakukan merek yang sama sebagai kategori yang berbeda akibat perbedaan pengetikan. |

---

## 5. Tahap Transformasi Data (Data Transformation)

Pada tahap ini, script `pipeline.py` melakukan penyesuaian format dan nilai data agar siap digunakan untuk analisis lanjutan maupun pemodelan *machine learning*.

### **A. Rincian Kolom, Metode, dan Alasan Transformasi**

1. **Transformasi Kolom Numerik (`price`)**
* **Nama Kolom**: `price`
* **Metode Transformasi**: *Min-Max Scaling* (meratakan rentang nilai numerik menjadi antara 0.0 sampai 1.0)
* **Alasan Pemilihan Kolom**: Kolom harga memiliki rentang nilai angka yang sangat besar. Penskalaan ini diperlukan agar algoritma komputer tidak berat sebelah terhadap angka yang besar.
* **Kolom Baru yang Dihasilkan**: Menghasilkan kolom baru `price_scaled` dan menyimpan kolom asli sebagai `price_original`.


2. **Transformasi Kolom Kategorikal (`body-style`)**
* **Nama Kolom**: `body-style`
* **Metode Transformasi**: *Encoding* (mengubah teks kategori menjadi kode angka berurutan menggunakan Pandas `factorize`)
* **Alasan Pemilihan Kolom**: Komputer dan model matematika memerlukan data dalam bentuk angka, sehingga tipe data teks pada bentuk bodi mobil perlu diterjemahkan.
* **Kolom Baru yang Dihasilkan**: Menghasilkan kolom baru `body_style_encoded` dan menyimpan kolom teks asli sebagai `body_style_original`.



### **B. Tabel Perbandingan Nilai Sebelum dan Sesudah Transformasi**

| No | Nama Kolom Asli | Nilai Sebelum (Original) | Metode Transformasi | Nilai Sesudah (Hasil Transformasi) | Kolom Baru di Dataset |
| --- | --- | --- | --- | --- | --- |
| 1 | `price` | $13,495 | *Min-Max Scaling* | 0.2079 (Desimal 0.0 s.d 1.0) | `price_scaled` |
| 2 | `body-style` | `"sedan"` / `"hatchback"` | *Encoding* | `0`, `1`, `2`, dst. (Kode Angka) | `body_style_encoded` |

---

## 6. Penjelasan Singkat Alur ETL & Lokasi Processed Dataset

* **Alur ETL (Extract, Transform, Load)**:
Script utama `pipeline.py` berjalan secara otomatis untuk mengekstrak data mentah (*Extract*), melakukan pembersihan serta transformasi data agar bersih dan konsisten (*Transform*), lalu memuat hasil akhirnya ke dalam direktori penyimpanan (*Load*).
* **Lokasi Processed Dataset**:
File data akhir yang telah melalui seluruh proses pembersihan dan transformasi tersimpan secara otomatis ke dalam direktori **`../data/processed/automobileEDA_processed.csv`** (atau di dalam folder `data/processed/automobileEDA_processed.csv` tergantung direktori eksekusi script). File inilah yang siap digunakan untuk tahap analisis lanjutan maupun pemodelan.
* **Diagram Alur (Data Flow Diagram)**:
Visualisasi lengkap dari seluruh tahapan alur di atas dapat dilihat pada file gambar **`documentation/data-flow-diagram.png`**.

---

## 7. Cara Instalasi & Menjalankan Pipeline

1. **Instalasi Dependency**: Pastikan library Pandas dan Numpy sudah terinstal di dalam *environment* Python Anda dengan menjalankan perintah berikut di terminal:
```bash
pip install pandas numpy (atau pip install -r requirements.txt)

```


2. **Menjalankan Script**: Eksekusi file utama project melalui terminal komputer Anda:
```bash
python pipeline.py

```



