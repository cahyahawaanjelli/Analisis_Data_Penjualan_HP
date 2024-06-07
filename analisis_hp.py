import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data dari CSV
produksi = pd.read_csv('produksi.csv')
penjualan = pd.read_csv('penjualan.csv')
persediaan = pd.read_csv('persediaan.csv')
wilayah = pd.read_csv('wilayah.csv')

# Menggabungkan data produksi dan penjualan
data = pd.merge(produksi, penjualan, on=['Bulan', 'Merk HP', 'Model HP'], suffixes=('_produksi', '_penjualan'))

# Menggabungkan data persediaan
data = pd.merge(data, persediaan, on=['Bulan', 'Merk HP', 'Model HP'])

# Menggabungkan data wilayah
data = pd.merge(data, wilayah, on=['Merk HP', 'Model HP'])

# Analisis statistik dasar
stats = data.groupby('Merk HP').agg({
    'Jumlah Produksi': 'mean',
    'Jumlah Penjualan': 'mean',
    'Jumlah Persediaan Awal': 'mean',
    'Jumlah Persediaan Akhir': 'mean'
}).reset_index()

print(stats)

# Visualisasi 1: Produksi vs Penjualan
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
sns.scatterplot(data=data, x='Jumlah Produksi', y='Jumlah Penjualan', hue='Merk HP')
plt.title('Produksi vs Penjualan')
plt.xlabel('Jumlah Produksi')
plt.ylabel('Jumlah Penjualan')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Visualisasi 2: Persediaan Awal vs Persediaan Akhir
plt.subplot(1, 2, 2)
sns.scatterplot(data=data, x='Jumlah Persediaan Awal', y='Jumlah Persediaan Akhir', hue='Merk HP')
plt.title('Persediaan Awal vs Persediaan Akhir')
plt.xlabel('Jumlah Persediaan Awal')
plt.ylabel('Jumlah Persediaan Akhir')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Menampilkan plot
plt.tight_layout()
plt.show()

# Visualisasi 3: Penjualan Berdasarkan Wilayah
plt.figure(figsize=(12, 8))
sns.barplot(data=data, x='Wilayah', y='Penjualan Januari', hue='Merk HP')
plt.title('Penjualan Januari Berdasarkan Wilayah dan Merk HP')
plt.xlabel('Wilayah')
plt.ylabel('Penjualan Januari')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Histogram dari Jumlah Produksi, Penjualan, dan Persediaan
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
sns.histplot(data['Jumlah Produksi'], bins=10, kde=True)
plt.title('Distribusi Jumlah Produksi')
plt.xlabel('Jumlah Produksi')
plt.ylabel('Frekuensi')

plt.subplot(1, 3, 2)
sns.histplot(data['Jumlah Penjualan'], bins=10, kde=True)
plt.title('Distribusi Jumlah Penjualan')
plt.xlabel('Jumlah Penjualan')
plt.ylabel('Frekuensi')

plt.subplot(1, 3, 3)
sns.histplot(data['Jumlah Persediaan Akhir'], bins=10, kde=True)
plt.title('Distribusi Jumlah Persediaan Akhir')
plt.xlabel('Jumlah Persediaan Akhir')
plt.ylabel('Frekuensi')

plt.tight_layout()
plt.show()

# Bar Chart untuk Total Produksi, Penjualan, dan Persediaan per Merk HP
plt.figure(figsize=(12, 6))
total_stats = data.groupby('Merk HP').agg({
    'Jumlah Produksi': 'sum',
    'Jumlah Penjualan': 'sum',
    'Jumlah Persediaan Akhir': 'sum'
}).reset_index()
total_stats_melted = total_stats.melt(id_vars='Merk HP', var_name='Variable', value_name='Total')
sns.barplot(data=total_stats_melted, x='Merk HP', y='Total', hue='Variable')
plt.title('Total Produksi, Penjualan, dan Persediaan per Merk HP')
plt.xlabel('Merk HP')
plt.ylabel('Total')
plt.legend(title='Variable')
plt.show()

# Pie Chart untuk Persentase Penjualan Berdasarkan Wilayah
plt.figure(figsize=(10, 6))
total_sales_per_region = data.groupby('Wilayah')['Jumlah Penjualan'].sum()
plt.pie(total_sales_per_region, labels=total_sales_per_region.index, autopct='%1.1f%%', startangle=140)
plt.title('Persentase Penjualan Berdasarkan Wilayah')
plt.axis('equal')
plt.show()

# Diagram Venn untuk Hubungan Antara Produksi, Penjualan, dan Persediaan
venn_labels = {
    '100': len(data),
    '010': len(data),
    '001': len(data),
    '110': len(data[(data['Jumlah Produksi'] > 0) & (data['Jumlah Penjualan'] > 0)]),
    '101': len(data[(data['Jumlah Produksi'] > 0) & (data['Jumlah Persediaan Akhir'] > 0)]),
    '011': len(data[(data['Jumlah Penjualan'] > 0) & (data['Jumlah Persediaan Akhir'] > 0)]),
    '111': len(data[(data['Jumlah Produksi'] > 0) & (data['Jumlah Penjualan'] > 0) & (data['Jumlah Persediaan Akhir'] > 0)])
}

plt.figure(figsize=(8, 6))
venn_diagram = venn3(subsets=venn_labels, set_labels=('Produksi', 'Penjualan', 'Persediaan'))
plt.title('Diagram Venn untuk Hubungan Antara Produksi, Penjualan, dan Persediaan')
plt.show()

# Statistik terkait visualisasi
total_produksi_mean = data['Jumlah Produksi'].mean()
total_penjualan_mean = data['Jumlah Penjualan'].mean()
total_persediaan_mean = data['Jumlah Persediaan Akhir'].mean()

print("Statistik Tambahan:")
print("Rata-rata Jumlah Produksi:", total_produksi_mean)
print("Rata-rata Jumlah Penjualan:", total_penjualan_mean)
print("Rata-rata Jumlah Persediaan Akhir:", total_persediaan_mean)
