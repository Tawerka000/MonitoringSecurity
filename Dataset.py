import pandas as pd
import numpy as np
# Загрузка датасета из файла
df = pd.read_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\Friday-WorkingHours-Morning.pcap_ISCX.csv')

num_rows = df.shape[0]
print(f'В датасете без обработки содержится {num_rows} записей.')

# Удаление дубликатов
df = df.drop_duplicates()

num_rows = df.shape[0]
print(f'После удаления дубликатов в датасете осталось {num_rows} записей.')

# Замена бесконечных значений на NaN
f = df.replace([np.inf, -np.inf], np.nan)

# Удаление строк с пустыми и бесконечными значениями
df = df.dropna()

num_rows = df.shape[0]
print(f'После удаления пустых и inf значений в датасете осталось {num_rows} записей.')

benign_df = df[df[' Label'] == 'BENIGN']
other_df = df[df[' Label'] != 'BENIGN']

print(f'Запсей размеченных как безопасные: {benign_df.shape[0]}.')
print(f'Запсей размеченных как небезопасные: {other_df.shape[0]}.')



if(benign_df.shape[0] > other_df.shape[0]):
    df = benign_df
    percentage_to_drop = 1 - abs(other_df.shape[0] / benign_df.shape[0])
else:
    df = other_df
    percentage_to_drop = 1 - abs(benign_df.shape[0] / other_df.shape[0])

# Вычисление количества строк для удаления
num_rows_to_drop = int(len(df) * percentage_to_drop)

# Генерация случайных индексов строк для удаления
indices_to_drop = np.random.choice(df.index, num_rows_to_drop, replace=False)

# Удаление выбранных строк
df = df.drop(indices_to_drop)

if(benign_df.shape[0] > other_df.shape[0]):
    benign_df = df
else:
    other_df = df

print(f'Запсей размеченных как безопасные после обработки: {benign_df.shape[0]}.')
print(f'Запсей размеченных как небезопасные после обработки: {other_df.shape[0]}.')

merged_df = pd.concat([benign_df, other_df])

# Сохранение объединенного датасета в CSV
merged_df.to_csv('BotnewDataset.csv', index=False)
