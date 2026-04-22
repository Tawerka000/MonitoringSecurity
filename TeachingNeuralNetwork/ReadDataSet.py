import pandas as pd
import os

'''folder_path = 'D:\\Python\\Test\\myApp\\Datasets'
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    if(file.endswith('.csv')):
        df = pd.read_csv(file_path,  on_bad_lines='skip')
        last_column = df.columns[-1]
        unique_values = df[last_column].unique()
        print(file)
        print("Уникальные значения для последнего столбца:")
        for value in unique_values:
            print(value)'''

def read_data():
    return pd.read_csv('D:\\Python\\Test\\myApp\\Datasets\\Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')

