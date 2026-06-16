import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

output_dir = './charts'
os.makedirs(output_dir, exist_ok=True)

print("Biểu đồ chủ đề 1 - Phân tích Big Tech")
try:
	df_raw = pd.read_csv('result_bigtech.txt', sep='\t', names=['Key', 'Count'])
	df_raw['Key'] = df_raw['Key'].astype(str).str.strip()
		
	source_list = []
	company_list = []
	for item in df_raw['Key']:
		if '_' in item:
			parts = item.split('_', 1)
			source_list.append(parts[0].strip())
			company_list.append(parts[1].strip())
		else:
			source_list.append('Global')
			company_list.append(item.strip())
	df_raw['Source'] = source_list
	df_raw['Company'] = company_list

	df_pivot = df_raw.pivot(index='Company', columns='Source', values='Count').fillna(0)
	df_pivot['Total'] = df_pivot.sum(axis=1)
	df_pivot = df_pivot.sort_values(by='Total', ascending=False).drop(columns='Total')
	
	
	ax = df_pivot.plot(kind='bar', stacked=True, figsize=(10, 6), color=['#e31a1c', '#1f78b4'], edgecolor='white')
	for container in ax.containers:
		labels = [f'{int(v.get_height())}' if v.get_height() > 0 else '' for v in container]
		ax.bar_label(container, labels=labels, label_type='center', color='white', fontsize=10, fontweight='bold')
	plt.title(f'Thống kê Sức hút của các Tập đoàn Công Nghệ', fontsize=14, fontweight='bold')
	plt.xlabel('Tập đoàn/Thương hiệu', fontsize=12)
	plt.ylabel('Tần suất xuất hiện (lần)', fontsize=12)
	plt.ylim(0, df_raw['Count'].max() * 1.15)
	plt.xticks(rotation=15)
	plt.legend(title='Nguồn bài viết')
	plt.tight_layout()
	plt.savefig(f'{output_dir}/bigtech.png', dpi=300)
	plt.close()
except Exception as e:
	print(f"Lỗi vẽ biểu đồ Bigram: {e}")

print("Biểu đồ chủ dề 2")
try:
	df_st = pd.read_csv('result_sentiment.txt', sep='\t', names=['Source', 'Sentiment', 'Count'])
	
	df_st['Sentiment'] = df_st['Sentiment'].str.strip()
	df_st['Source'] = df_st['Source'].str.strip()

	df_st = df_st[df_st['Source'].isin(['Global', 'VN'])]
	df_grouped = df_st.groupby(['Source', 'Sentiment'], as_index=False)['Count'].sum()
	
	plt.figure(figsize=(10, 6))
	
	sentiment_order = ['Positive', 'Neutral', 'Negative']

	ax=sns.barplot(data=df_grouped, x='Sentiment', y='Count', hue='Source', palette='Set2', order=sentiment_order, errorbar=None)
	
	for container in ax.containers:
		ax.bar_label(container, fmt='%d', padding=3, fontsize=10, fontweight='bold')

	plt.title('So sánh sắc thái bài viết (Sentiment Analysis)', fontsize=14, fontweight='bold')
	plt.xlabel('Sắc thái', fontsize=12)
	plt.ylabel('Số lượng bài viết', fontsize=12)

	plt.ylim(0, df_grouped['Count'].max() *1.15)
	plt.legend(title='Nguồn bài viết')
	plt.tight_layout()
	plt.savefig(f'{output_dir}/sentiment_analysis.png', dpi=300)
	plt.close()
except Exception as e:
	print(f"Lỗi vẽ biểu đồ Sentiment: {e}")

print("Biểu đồ chủ đề 3")
try:
	
	df_len = pd.read_csv('result_length.txt', sep='\t', names=['Source', 'Length_Group', 'Count'])
	df_len['Length_Group'] = df_len['Length_Group'].str.strip()
	df_len['Source'] = df_len['Source'].str.strip()
	df_len = df_len[df_len['Source'].isin(['Global', 'VN'])]

	df_grouped = df_len.groupby(['Source', 'Length_Group'], as_index=False)['Count'].sum()

	df_grouped['Length_Group'] = df_grouped['Length_Group'].replace({'Short': 'Short (<300 words)', 'Medium': 'Medium (300-1000 words)', 'Long': 'Long (>1000 words)'})
	
	plt.figure(figsize=(10, 6))

	custom_order = ['Short (<300 words)', 'Medium (300-1000 words)', 'Long (>1000 words)']
	ax=sns.barplot(data=df_grouped, x='Length_Group', y='Count', hue='Source', palette='muted',
		order=custom_order, errorbar=None)
	for container in ax.containers:
		ax.bar_label(container, fmt='%d', padding=3, fontsize=10, fontweight='bold')
	plt.ylim(0, df_grouped['Count'].max() * 1.15)
	plt.title('Phân loại độ dài bài viết & Mức độ chuyên sâu', fontsize=14, fontweight='bold')
	plt.xlabel('Nhóm độ dài', fontsize=12)
	plt.ylabel('Số lượng bài viết', fontsize=12)
	plt.legend(title='Nguồn bài viết')
	plt.tight_layout()
	plt.savefig(f'{output_dir}/article_length.png', dpi=300)
	plt.close()
except Exception as e:
	print(f"Lỗi vẽ biểu đồ Độ dài: {e}")
print(f"Vẽ biểu đồ thành công!")
