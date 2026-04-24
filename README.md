# Proyek Analisis Data: Dashboard-Bike-Sharing

[**Bike Sharing Dataset**](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset) adalah dataset persewaan sepeda dengan nama perusahaan adalah Capital Bike Sharing. Data ini terjadi selama periode 2011 dan 2012. Berikut adalah informasi dari dataset tersebut:
- instan: nomor urut baris
- dteday: tanggal data tersebut diambil
- season: musim yang dimasukkan dalam bentuk angka (1. musim semi, 2. musim panas, 3. musim gugur, 4. musim dingin)
- yr: tahun data (0. tahun 2011 dan 1. tahun 2012)
- mnth: bulan (angka 1 untuk januari, dst hingga bulan ke 12)
- hr: jam (dalam 24 jam)
- holiday: hari libur (1: ya, 0: tidak)
- weekday: hari rentan seminggu (0. Senin, dst hingga 6. Minggu)
- workingday: hari kerja (1: ya, 0: tidak)
- weathersit: kondisi cuaca dalam bentuk angka (1. cerah, 2. berawan, 3. hujan)
- temp: suhu aktual (0 hingga 1)
- atemp: suhu yang sedang dirasakan
- hum: kelembapan (0 hingga 1)
- windspeed: kecepatan angin (0 hingga 1)
- casual: jumlah pengguna casual (tanpa registrasi)
- registered: jumlah pengguna terdaftar (sudah melakukan registrasi)
- cnt: jumlah total penyewa

## Setup Environment Terminal
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

## Run streamlit app
streamlit run dashboard.py

## Deploy streamlit
[Lihat disini](https://dashboardcloudbikesharing-deviema.streamlit.app/)
