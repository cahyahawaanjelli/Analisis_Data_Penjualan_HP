import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn3

# Membaca data dari CSV
produksi = pd.read_csv('produksi.csv')
penjualan = pd.read_csv('penjualan.csv')
persediaan = pd.read_csv('persediaan.csv')
wilayah = pd.read_csv('wilayah.csv')

# Merge data
merged_data = pd.merge(pd.merge(produksi, penjualan, on=['Bulan', 'Merk HP', 'Model HP']),
                       persediaan, on=['Bulan', 'Merk HP', 'Model HP'])
merged_data = pd.merge(merged_data, wilayah, on=['Merk HP', 'Model HP'])

# Visualisasi 1: Perbandingan produksi per merek HP
sns.barplot(data=merged_data, x='Merk HP', y='Jumlah Produksi', hue='Bulan')
plt.title('Perbandingan Produksi per Merek HP')
plt.xlabel('Merek HP')
plt.ylabel('Jumlah Produksi')
plt.xticks(rotation=45)
plt.legend(title='Bulan', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Visualisasi 2: Perbandingan penjualan antar wilayah
sns.barplot(data=merged_data, x='Wilayah', y='Jumlah Penjualan', hue='Merk HP')
plt.title('Perbandingan Penjualan antar Wilayah')
plt.xlabel('Wilayah')
plt.ylabel('Jumlah Penjualan')
plt.xticks(rotation=45)
plt.legend(title='Merek HP', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Visualisasi 3: Korelasi antara produksi, penjualan, dan persediaan
sns.heatmap(merged_data[['Jumlah Produksi', 'Jumlah Penjualan', 'Jumlah Persediaan Awal']].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Korelasi Produksi, Penjualan, dan Persediaan')
plt.show()

# Visualisasi 4: Tren penjualan
sns.lineplot(data=penjualan, x='Bulan', y='Jumlah Penjualan', hue='Merk HP', marker='o')
plt.title('Tren Penjualan dari Bulan ke Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penjualan')
plt.xticks(rotation=45)
plt.legend(title='Merek HP', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Visualisasi 5: Perbandingan rata-rata produksi, penjualan, dan persediaan per bulan
monthly_stats = merged_data.groupby('Bulan').mean().reset_index()
plt.plot(monthly_stats['Bulan'], monthly_stats['Jumlah Produksi'], label='Produksi', marker='o')
plt.plot(monthly_stats['Bulan'], monthly_stats['Jumlah Penjualan'], label='Penjualan', marker='o')
plt.plot(monthly_stats['Bulan'], monthly_stats['Jumlah Persediaan Awal'], label='Persediaan Awal', marker='o')
plt.title('Perbandingan Rata-Rata Produksi, Penjualan, dan Persediaan per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-Rata')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Visualisasi 6: Pie chart persentase penjualan per merek HP
total_penjualan_per_merk = merged_data.groupby('Merk HP')['Jumlah Penjualan'].sum()
plt.pie(total_penjualan_per_merk, labels=total_penjualan_per_merk.index, autopct='%1.1f%%', startangle=140)
plt.title('Persentase Penjualan per Merek HP')
plt.axis('equal')
plt.show()

# Visualisasi 7: Diagram Venn untuk hubungan antara produksi, penjualan, dan persediaan
venn3(subsets=(len(produksi), len(penjualan), len(persediaan), len(merged_data),
               len(merged_data) - len(produksi) - len(penjualan) + len(persediaan),
               len(merged_data) - len(produksi) - len(persediaan) + len(penjualan),
               len(merged_data) - len(penjualan) - len(persediaan) + len(produksi))),
plt.title('Hubungan antara Produksi, Penjualan, dan Persediaan')
plt.show()
