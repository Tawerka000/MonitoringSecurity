import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras
import settings
# Определение пути для сохранения модели
model_checkpoint = keras.callbacks.ModelCheckpoint('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models_saves\\PortScan_best_model.keras', monitor=settings.monitor, mode=settings.mode, save_best_only=True, verbose=1)

selected_features = pd.read_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\NewDataSets\\PortScannewDataset.csv')
#selected_features = pd.read_csv('D:\Python\MonitoringSecurityProject\Datasets\Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv')
#selected_features = pd.read_csv('D:\Python\MonitoringSecurityProject\Datasets\TrafficLabelling\Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv')
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
#for item in X:
#        X[item]=X[item].astype("Float32")
y = selected_features[" Label"].map(lambda x: False if x == 'BENIGN' else True)
X = pd.DataFrame({key: value.astype("float32") for key, value in X.items()})
# Разделение на тренировочный и тестовый набор
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Масштабирование признаков
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# Создание модели Keras
model = keras.Sequential()
model.add(keras.layers.Input(shape=(X_train.shape[1],)))
for _ in range(1, 29):
        model.add(keras.layers.Dense(82, activation='relu'))
        #model.add(keras.layers.LeakyReLU(alpha=0.3))
        #model.add(keras.layers.PReLU())
model.add(keras.layers.Dense(1, activation='sigmoid'))
opt = keras.optimizers.RMSprop(learning_rate=0.001, rho=0.9)
# Компиляция модели
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy']) 

# Обучение модели
history = model.fit(X_train, y_train, epochs=30, batch_size=256, validation_data=(X_test, y_test), callbacks=[model_checkpoint])
#вывод наилучшего результата
accuracy = max(history.history['val_accuracy'])
loss = min(history.history['val_loss'])

print(accuracy)
print(loss)