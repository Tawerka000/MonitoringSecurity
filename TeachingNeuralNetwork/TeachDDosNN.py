import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras
import settings
# Определение пути для сохранения модели
model_checkpoint = keras.callbacks.ModelCheckpoint('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models_saves\\DDoS_best_model.keras', monitor=settings.monitor, mode=settings.mode, save_best_only=True, verbose=1)

selected_features = pd.read_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\NewDataSets\\DDoSnewDataset.csv')
selected_features = selected_features[[" Total Fwd Packets", " Total Backward Packets", " Fwd Packet Length Min",
                                       " Fwd Packet Length Mean", " Fwd Packet Length Std", " Bwd Packet Length Min",
                                       " Fwd Header Length", " Bwd Header Length", " Min Packet Length", " Packet Length Mean",
                                       " PSH Flag Count", " ACK Flag Count", " URG Flag Count", " Down/Up Ratio",
                                       " Average Packet Size", " Avg Fwd Segment Size", " Subflow Bwd Packets",
                                       " act_data_pkt_fwd", " min_seg_size_forward", " Label"]]
# Разделение на признаки и целевую переменную
X = {}
X = selected_features.drop(columns=[" Label"]).copy()
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
for _ in range(1, 8): 
        model.add(keras.layers.Dense(83, activation='relu'))
model.add(keras.layers.Dense(1, activation='sigmoid'))
# Компиляция модели
model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy']) 

# Обучение модели
history = model.fit(X_train, y_train, epochs=30, batch_size=64, validation_data=(X_test, y_test), callbacks=[model_checkpoint])
#вывод наилучшего результата
accuracy = max(history.history['val_accuracy'])
loss = min(history.history['val_loss'])

print(accuracy)
print(loss)