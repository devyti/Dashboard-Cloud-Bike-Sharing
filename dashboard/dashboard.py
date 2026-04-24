import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#helper function

def create_daily_orders_df(df):
    df['date'] = pd.to_datetime(df['date'])
    order_df = df.resample('MS', on='date').sum()
    return order_df

def create_sum_casual_df(df):
    sum_casual_df = df.groupby("weekday").casual.sum().sort_values(ascending=False).reset_index()
    return sum_casual_df

def create_sum_registered_df(df):
    sum_registered_df = df.groupby("weekday").registered.sum().sort_values(ascending=False).reset_index()
    return sum_registered_df

def create_sum_byweather_df(df):
    sum_byweather_df = df.groupby("weather")['count'].sum().sort_values(ascending=False).reset_index()
    return sum_byweather_df

def create_sum_byseason_df(df):
    sum_byseason_df = df.groupby("season")['count'].sum().sort_values(ascending=False).reset_index()
    return sum_byseason_df

def create_rfm_df(df):
    rfm_df = day_df.groupby(by="weekday", as_index=False).agg ({
        "date": "max",
        "id": "nunique",
        "count": "sum"
    })
    rfm_df.columns = ["weekday", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = day_df["date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df

#load berkas sebagai data frame
day_df = pd.read_csv(r"D:/MBKM/DICODING/submission/dashboard/main_data.csv")

#memastikan kolom date bertipe datetime
datetime_colomns = ["date"]
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)
for column in datetime_colomns:
    day_df[column] = pd.to_datetime(day_df[column])

#membuat komponen filter
min_date = day_df["date"].min()
max_date = day_df["date"].max()

with st.sidebar:
    #menambahkan logo perusahaan
    st.image("D:/MBKM/DICODING/submission/dashboard/logo.jpg")

    #mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        format="YYYY/MM/DD"
    )
    #menyimpan date time
    main_df = day_df[(day_df["date"] >= pd.to_datetime(start_date)) & 
                     (day_df["date"] <= pd.to_datetime(end_date))]
    
#memanggil helper function yang telah kita buat sebelumnya
daily_orders_df = create_daily_orders_df(main_df)
sum_casual_df = create_sum_casual_df(main_df)
sum_registered_df = create_sum_registered_df(main_df)
byweather = create_sum_byweather_df(main_df)
byseason = create_sum_byseason_df(main_df)
rfm_df = create_rfm_df(main_df)

#membuat dashboard
st.header('Cloud Bike Share Dashboard :sparkles:')

#penyewa harian
st.subheader('Penyewa Harian')
col1, col2, col3 = st.columns(3)

with col1:
    total_casual = daily_orders_df.casual.sum()
    st.metric("Total Penyewa Casual", value=f'{total_casual:,}')

with col2:
    total_registered = daily_orders_df.registered.sum()
    st.metric("Total Penyewa Registered/Terdaftar", value=f'{total_registered:,}')

with col3:
    total_users = daily_orders_df['count'].sum()
    st.metric("Total Penyewa", value=f'{total_users:,}')

plt.figure(figsize=(16, 8))
plt.plot(daily_orders_df.index, daily_orders_df['count'], 
         marker='o', 
         linewidth=2,
         color="#90CAF9")
plt.xlabel(None)
plt.ylabel(None)
plt.title('Jumlah Penyewa')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#jumlah penyewa casual dan registered berdasarkan hari
st.subheader("Jumlah Penyewa Casual dan Registered  Per Hari")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#6897C9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="casual", y="weekday", data=sum_casual_df, palette=colors, hue="weekday", legend=False, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Casual User", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="registered", y="weekday", data=sum_registered_df, hue="weekday", legend=False, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Registered User", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=25)

st.pyplot(fig)

#pengaruh faktor eksternal (kondisi cuaca dan musim) terhadap jumlah penyewaan sepeda
st.subheader("Jumlah Penyewa Berdasarkan Cuaca dan Musim")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
color_weather = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
color_season =  ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(y="count", x="weather", data=byweather.sort_values(by="count", ascending=False), palette=color_weather, hue="weather", legend=False, ax=ax[0])
ax[0].set_title("Jumlah penyewa berdasarkan Cuaca", loc="center", fontsize=50)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30)
ax[0].ticklabel_format(style='plain', axis='y')

sns.barplot(y="count", x="season", data=byseason.sort_values(by="count", ascending=False), palette=color_season, hue="season", legend=False, ax=ax[1])
ax[1].set_title("Jumlah penyewa berdasarkan Musim", loc="center", fontsize=50)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30)
ax[1].ticklabel_format(style='plain', axis='y')

st.pyplot(fig)

#RFM Analisis
st.subheader("Best Customer Based on RFM Parameters (weekday)")
col1, col2, col3 =st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("By Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 1)
    st.metric("By Frequency (days)", value=avg_frequency)

with col3:
    avg_monetary = round(rfm_df.monetary.mean(), 1)
    st.metric("By Monetary (days)", value=avg_monetary)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(40, 20))
 
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
 
sns.barplot(y="recency", x="weekday", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, hue="weekday", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="frequency", x="weekday", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, hue="weekday", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency (days)", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="monetary", x="weekday", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, hue="weekday", ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary (days)", loc="center", fontsize=30)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)
 
st.caption('Copyright (c) 2026 All Rights Reserved [Devi Ema Dewiyanti](github)')
