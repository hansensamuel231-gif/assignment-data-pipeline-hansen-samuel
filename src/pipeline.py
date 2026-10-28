import os
import pandas as pd

def load_data(filepath):
    """1. Membaca dataset mentah dari folder data/raw/"""
    df = pd.read_csv(filepath)
    print("=== DATA BERHASIL DIMUAT ===")
    return df

def inspect_data(df):
    """2. Memeriksa kondisi awal dataset"""
    print("\n=== 1. LIMA BARIS PERTAMA DATASET ===")
    print(df.head())
    
    print("\n=== 2. UKURAN DATASET (Baris, Kolom) ===")
    print(df.shape)
    
    print("\n=== 3. INFORMASI TIPE DATA & INFO KOLOM ===")
    print(df.info())
    
    print("\n=== 4. JUMLAH MISSING VALUES PER KOLOM ===")
    print(df.isnull().sum())
    
    print("\n=== 5. JUMLAH BARIS DUPLIKAT ===")
    print(df.duplicated().sum())

def clean_data(df):
    """3. Melakukan pembersihan data (cleaning)"""
    print("\n--- MEMULAI PROSES DATA CLEANING ---")
    
    # A. Menghapus baris duplikat
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"-> Berhasil menghapus {initial_rows - len(df)} baris data duplikat.")
    
    # B. Menangani Missing Values (Data Kosong)
    numeric_cols = ['stroke', 'horsepower', 'price']
    for col in numeric_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mean())
            
    cat_cols = ['transaction_date', 'make', 'num-of-doors', 'horsepower-binned']
    for col in cat_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])
            
    print("-> Berhasil menangani seluruh missing values.")

    # C. Menyeragamkan penulisan data kategorikal
    if 'make' in df.columns:
        df['make'] = df['make'].str.strip().str.lower()
    print("-> Berhasil menyeragamkan teks pada kolom kategorikal.")

    return df

def transform_data(df):
    """4. Melakukan transformasi data (Min-Max Scaling & Encoding)"""
    print("\n--- MEMULAI PROSES DATA TRANSFORMATION ---")
    
    # A. Mengubah tipe data 'transaction_date' menjadi datetime
    if 'transaction_date' in df.columns:
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
        print("-> Berhasil mengubah tipe data 'transaction_date' menjadi datetime.")

    # B. Min-Max Scaling pada kolom numerik 'price'
    if 'price' in df.columns:
        df['price_original'] = df['price']
        min_val = df['price'].min()
        max_val = df['price'].max()
        df['price_scaled'] = (df['price'] - min_val) / (max_val - min_val)
        print("-> Berhasil melakukan Min-Max Scaling pada kolom 'price' (rentang 0.0 s.d 1.0).")

    # C. Encoding pada kolom kategorikal 'body-style'
    if 'body-style' in df.columns:
        # Menyimpan nilai asli teks bodi mobil
        df['body_style_original'] = df['body-style']
        
        # Menggunakan pandas factorize untuk mengubah teks kategori menjadi kode angka (0, 1, 2, dst.)
        df['body_style_encoded'], _ = pd.factorize(df['body-style'])
        print("-> Berhasil melakukan Encoding pada kolom 'body-style' menjadi nilai numerik.")
        
    return df

def save_data(df, output_filepath):
    """5. Menyimpan hasil akhir ke folder data/processed/"""
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    df.to_csv(output_filepath, index=False)
    print(f"\n=== DATA BERHASIL DISIMPAN KE: {output_filepath} ===")

# --- EKSEKUSI UTAMA PIPELINE (ETL) ---
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    path_raw = "../data/raw/automobileEDA_dirty_training.csv"
    path_processed = "../data/processed/automobileEDA_processed.csvv"
    
    raw_df = load_data(path_raw)
    inspect_data(raw_df)
    
    cleaned_df = clean_data(raw_df)
    transformed_df = transform_data(cleaned_df)
    
    save_data(transformed_df, path_processed)