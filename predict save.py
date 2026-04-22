import keras
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import concurrent.futures
# Порог
normalThreshold = 0.5
suspectThreshold = 0.75
monitoring_result_file_path = 'D:\\Python\\MonitoringSecurityProject\\Statistics\\monitoring_result.txt'
best_model_DDoS = keras.models.load_model('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models_saves\\DDoS_best_model.keras')
best_model_PortScan = keras.models.load_model('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models_saves\\PortScan_best_model.keras')
best_model_Bot = keras.models.load_model('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models_saves\\Bot_best_model.keras')
def makePred(data):
    data
    chunk_size = 10000  # Размер части данных для обработки

# Разбиение данных на части
    data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Создание пула потоков для обработки данных
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(pred, data_chunks)

def pred(data):
    
    rowNum = data.shape[0]

    df_DDos = data[["Tot Fwd Pkts", "Tot Bwd Pkts", "Fwd Pkt Len Min", "Fwd Pkt Len Mean", 
             "Fwd Pkt Len Std", "Bwd Pkt Len Min", "Fwd Header Len", "Bwd Header Len", 
             "Pkt Len Min", "Pkt Len Mean", "Fwd PSH Flags", "ACK Flag Cnt", "Fwd URG Flags", 
             "Down/Up Ratio", "Pkt Size Avg", "Fwd Seg Size Avg", "Subflow Bwd Pkts", "Fwd Act Data Pkts", 
             "Fwd Seg Size Min"]]
    
    df_PortScan = data[["Dst Port", "Flow Duration", "Tot Fwd Pkts", "Tot Bwd Pkts", 
                                       "TotLen Fwd Pkts", "TotLen Bwd Pkts", "Fwd Pkt Len Max", 
                                       "Fwd Pkt Len Min", "Fwd Pkt Len Mean", "Fwd Pkt Len Std", 
                                       "Bwd Pkt Len Max", "Bwd Pkt Len Min", "Bwd Pkt Len Mean", 
                                       "Bwd Pkt Len Std", "Fwd Header Len", "Bwd Header Len", "Fwd Pkts/s", 
                                       "Bwd Pkts/s", "Pkt Len Min", "Pkt Len Max", 
                                       "Pkt Len Mean", "Pkt Len Std", "Pkt Len Var", "FIN Flag Cnt", 
                                       "SYN Flag Cnt", "RST Flag Cnt", "PSH Flag Cnt", "Down/Up Ratio", 
                                       "Pkt Size Avg", "Fwd Seg Size Avg", "Bwd Seg Size Avg", 
                                       "Subflow Fwd Pkts", "Subflow Fwd Byts", "Subflow Bwd Pkts", 
                                       "Subflow Bwd Byts", "Init Fwd Win Byts", "Init Bwd Win Byts", 
                                       "Fwd Act Data Pkts", "Fwd Seg Size Min"]]
    
    df_Bot = data[["Flow Duration", "Tot Fwd Pkts", "Tot Bwd Pkts", "TotLen Fwd Pkts", 
                                       "TotLen Bwd Pkts","Fwd Pkt Len Max", "Fwd Pkt Len Min", "Fwd Pkt Len Mean", "Fwd Pkt Len Std",
                                       "Bwd Pkt Len Max", "Bwd Pkt Len Min", "Bwd Pkt Len Mean", "Bwd Pkt Len Std",
                                       "Fwd PSH Flags", "Bwd PSH Flags", "Fwd URG Flags", "Bwd URG Flags",
                                       "Active Mean", "Active Std", "Active Max", "Active Min"]]
    df_DDos_array = {}
    df_PortScan_array = {}
    df_Bot_array = {}

    statistic_for_output = data[["Timestamp", "Src IP", "Dst IP"]]

    '''for item in df_DDos:
        df_DDos_array[item] = df_DDos[item].astype("Float32")
    for item in df_PortScan:
        df_PortScan_array[item] = df_PortScan[item].astype("Float32")
    for item in df_Bot:
        df_Bot_array[item] = df_Bot[item].astype("Float32")'''

    df_PortScan_array = pd.DataFrame({key: value.astype("float32") for key, value in df_PortScan.items()})
    df_DDos_array = pd.DataFrame({key: value.astype("float32") for key, value in df_DDos.items()})
    df_Bot_array = pd.DataFrame({key: value.astype("float32") for key, value in df_Bot.items()})
    
    scaler = StandardScaler()
    df_DDos_array = scaler.fit_transform(df_DDos_array)
    df_Bot_array = scaler.fit_transform(df_Bot_array)
    df_PortScan_array = scaler.fit_transform(df_PortScan_array)
    for index in range(rowNum):
        pred_DDoS = best_model_DDoS.predict(np.reshape(df_DDos_array[index], (1, 19)))
        pred_PortScan = best_model_PortScan.predict(np.reshape(df_PortScan_array[index], (1, 39)))
        pred_Bot = best_model_Bot.predict(np.reshape(df_Bot_array[index], (1, 21)))
        if(max(pred_Bot, pred_DDoS, pred_PortScan) >= 1):
            print(pred_DDoS, pred_PortScan, pred_Bot)
            print('Suspect')
            with open(monitoring_result_file_path, 'a') as file:  # Открываем файл для дописывания
                if(max(pred_Bot, pred_DDoS, pred_PortScan) == pred_DDoS):
                    name = 'DDoS'
                elif(max(pred_Bot, pred_DDoS, pred_PortScan) == pred_PortScan):
                    name = 'PortScan'
                else:
                    name = 'Bot'
                file.write(f'{name} - {statistic_for_output.loc[index]}\n')
        else:
            print(pred_DDoS, pred_PortScan, pred_Bot)
            print('Normal')

        '''if(pred_Bot <= normalThreshold and pred_DDoS <= normalThreshold and pred_PortScan <= normalThreshold):
            print(pred_DDoS, pred_PortScan, pred_Bot)
            print('Normal')
        elif(max(pred_Bot, pred_DDoS, pred_PortScan) >= suspectThreshold):
            print(pred_DDoS, pred_PortScan, pred_Bot)
            print('Suspect')
            with open(monitoring_result_file_path, 'a') as file:  # Открываем файл для дописывания
                if(max(pred_Bot, pred_DDoS, pred_PortScan) == pred_DDoS):
                    name = 'DDoS'
                elif(max(pred_Bot, pred_DDoS, pred_PortScan) == pred_PortScan):
                    name = 'PortScan'
                else:
                    name = 'Bot'
                file.write(f'{name} - {statistic_for_output.loc[index]}\n')
        else:
            print(pred_DDoS, pred_PortScan, pred_Bot)
            print('Unkown')
            with open(monitoring_result_file_path, 'a') as file:  # Открываем файл для дописывания
                file.write(f'Unkown - {statistic_for_output.loc[index]}\n')'''