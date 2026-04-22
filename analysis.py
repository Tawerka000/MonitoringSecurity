from joblib import load
import keras
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Порог
threshold = 0.5

def makePred(data):
    best_model = keras.models.load_model('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models\\DDos_best_model.keras')
    df = data[["Tot Fwd Pkts", "Tot Bwd Pkts", "Fwd Pkt Len Min", "Fwd Pkt Len Mean", 
             "Fwd Pkt Len Std", "Bwd Pkt Len Min", "Fwd Header Len", "Bwd Header Len", 
             "Pkt Len Min", "Pkt Len Mean", "Fwd PSH Flags", "ACK Flag Cnt", "Fwd URG Flags", 
             "Down/Up Ratio", "Pkt Size Avg", "Fwd Seg Size Avg", "Subflow Bwd Pkts", "Fwd Act Data Pkts", 
             "Fwd Seg Size Min"]]
    df_array = {}
    time_df = data[["Timestamp", "Src IP", "Dst IP"]]
    for item in df:
        df_array[item]=df[item].astype("Float32")
    df_array = pd.DataFrame({key: value.astype("float32") for key, value in df.items()})
    scaler = StandardScaler()
    df_array = scaler.fit_transform(df_array)
    for index, row in enumerate(df_array):
        pred = best_model.predict(np.reshape(df_array[index], (1, 19)))
        if(pred > threshold):
            print(pred)
            print('DDos')
            with open('D:\\Python\\MonitoringSecurityProject\\Statistics\\monitoring_result.txt', 'a') as file:  # Открываем файл для дописывания
                file.write(f'ddos - {time_df.loc[index]}\n')
        else:
            print(pred)
            print('Normal')