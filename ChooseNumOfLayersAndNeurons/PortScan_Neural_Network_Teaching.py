import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras

# Списки для хранения результатов
accuracies = []
losses = []

neural_network_name = 'PortScan'

dataset_for_teach_path = 'D:\\Python\MonitoringSecurityProject\\Datasets\\NewDataSets\\PortScannewDataset.csv'
layers_save_path = 'D:\\Python\\MonitoringSecurityProject\\Statistics\\{}_Layers.xlsx'.format(neural_network_name)
neurons_save_path = 'D:\\Python\\MonitoringSecurityProject\\Statistics\\{}_Neurons.xlsx'.format(neural_network_name)
max_num_of_layers = 31
max_num_of_neurons = 101
num_of_neurons_for_start = 15

selected_features = pd.read_csv(dataset_for_teach_path)
selected_features = selected_features[[" Destination Port", " Flow Duration", " Total Fwd Packets", " Total Backward Packets", 
                                       "Total Length of Fwd Packets", " Total Length of Bwd Packets", " Fwd Packet Length Max", 
                                       " Fwd Packet Length Min", " Fwd Packet Length Mean", " Fwd Packet Length Std", 
                                       "Bwd Packet Length Max", " Bwd Packet Length Min", " Bwd Packet Length Mean", 
                                       " Bwd Packet Length Std", " Fwd Header Length", " Bwd Header Length", "Fwd Packets/s", 
                                       " Bwd Packets/s", " Min Packet Length", " Max Packet Length", 
                                       " Packet Length Mean", " Packet Length Std", " Packet Length Variance", "FIN Flag Count", 
                                       " SYN Flag Count", " RST Flag Count", " PSH Flag Count", " Down/Up Ratio", 
                                       " Average Packet Size", " Avg Fwd Segment Size", " Avg Bwd Segment Size", 
                                       "Subflow Fwd Packets", " Subflow Fwd Bytes", " Subflow Bwd Packets", 
                                       " Subflow Bwd Bytes", "Init_Win_bytes_forward", " Init_Win_bytes_backward", 
                                       " act_data_pkt_fwd", " min_seg_size_forward", " Label"]]
# Разделение на признаки и целевую переменную
X = {}
X = selected_features.drop(columns=[" Label"]).copy()
y = selected_features[" Label"].map(lambda x: False if x == 'BENIGN' else True)
X = pd.DataFrame({key: value.astype("float32") for key, value in X.items()})

# Разделение на тренировочный и тестовый набор
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

'''# Масштабирование признаков
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)'''

# Обучение на увеличивающемся количестве слоёв с выводом статистики
for num_of_layers in range(1, max_num_of_layers):
    model = keras.Sequential()
    model.add(keras.layers.Input(shape=(X_train.shape[1],)))
    for _ in range(1, num_of_layers):
         model.add(keras.layers.Dense(num_of_neurons_for_start, activation='relu'))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=10, batch_size=512, validation_data=(X_test, y_test))

    accuracy = max(history.history['val_accuracy'])
    loss = min(history.history['val_loss'])

    accuracies.append(accuracy)
    losses.append(loss)

    print(f"Количество слоёв: {num_of_layers} - Точность: {accuracy}; Потери: {loss}")
# Вывод статистики по слоям
results_df = pd.DataFrame({
    'Количество слоёв': range(1, max_num_of_layers),
    'Точность': accuracies,
    'Потери': losses
})
results_df.to_excel(layers_save_path, index=False)
optimal_num_of_layers = 0

# Выбираем оптимальное значение слоёв
max_accuracy = max(accuracies)
index_of_max_accuracy = accuracies.index(max_accuracy)
min_loss = min(losses)
index_of_min_loss = losses.index(min_loss)
if(index_of_max_accuracy == index_of_min_loss):
     optimal_num_of_layers = index_of_max_accuracy + 1
else:
     if(abs(accuracies[index_of_max_accuracy] - accuracies[index_of_min_loss]) > (losses[index_of_max_accuracy] - losses[index_of_min_loss])):
          optimal_num_of_layers = index_of_max_accuracy + 1
     else:
          optimal_num_of_layers = index_of_min_loss + 1



# Обнуление статистики
accuracies = []
losses = []

for num_of_neurons in range(1, max_num_of_neurons):
    model = keras.Sequential()
    model.add(keras.layers.Input(shape=(X_train.shape[1],)))
    for _ in range(1, optimal_num_of_layers):
         model.add(keras.layers.Dense(num_of_neurons, activation='relu'))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=10, batch_size=512, validation_data=(X_test, y_test))

    accuracy = max(history.history['val_accuracy'])
    loss = min(history.history['val_loss'])

    accuracies.append(accuracy)
    losses.append(loss)

    print(f"Количество нейронов: {num_of_neurons} - Точность: {accuracy}; Потери: {loss}")

# Вывод статистики по нейронам
results_df = pd.DataFrame({
    'Количество нейронов': range(1, max_num_of_neurons),
    'Точность': accuracies,
    'Потери': losses
})
results_df.to_excel(neurons_save_path, index=False)

# Выбираем оптимальное количество нейронов
max_accuracy = max(accuracies)
index_of_max_accuracy = accuracies.index(max_accuracy)
min_loss = min(losses)
index_of_min_loss = losses.index(min_loss)
if(index_of_max_accuracy == index_of_min_loss):
     optimal_num_of_neurons = index_of_max_accuracy + 1
else:
     if(abs(accuracies[index_of_max_accuracy] - accuracies[index_of_min_loss]) > (losses[index_of_max_accuracy] - losses[index_of_min_loss])):
          optimal_num_of_neurons = index_of_max_accuracy + 1
     else:
          optimal_num_of_neurons = index_of_min_loss + 1

print(f'Оптимальное количество слоёв: {optimal_num_of_layers}')
print(f'Оптимальное количество нейронов: {optimal_num_of_neurons}')

with open('D:\\Python\\MonitoringSecurityProject\\Statistics\\{}.txt'.format(neural_network_name), 'w') as file:
                file.write(f'Оптимальное количество слоёв: {optimal_num_of_layers}\nОптимальное количество нейронов: {optimal_num_of_neurons}')