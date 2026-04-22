import keras
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

monitoring_result_file_path = 'D:\\Python\\MonitoringSecurityProject\\Statistics\\monitoring_result.txt'
best_model_DDoS = keras.models.load_model('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models_saves\\DDoS_best_model.keras')
best_model_PortScan = keras.models.load_model('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models_saves\\PortScan_best_model.keras')
#best_model_Bot = keras.models.load_model('D:\\Python\\MonitoringSecurityProject\\NeuralNetwork_models_saves\\Bot_best_model.keras')
def makePred(data, RealData):

    realTimeDDoSColumns = ["Tot Fwd Pkts", "Tot Bwd Pkts", "Fwd Pkt Len Min", "Fwd Pkt Len Mean", 
             "Fwd Pkt Len Std", "Bwd Pkt Len Min", "Fwd Header Len", "Bwd Header Len", 
             "Pkt Len Min", "Pkt Len Mean", "Fwd PSH Flags", "ACK Flag Cnt", "Fwd URG Flags", 
             "Down/Up Ratio", "Pkt Size Avg", "Fwd Seg Size Avg", "Subflow Bwd Pkts", "Fwd Act Data Pkts", 
             "Fwd Seg Size Min"]
    
    realTimePortScanColumns = ["Dst Port", "Flow Duration", "Tot Fwd Pkts", "Tot Bwd Pkts", 
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
                                       "Fwd Act Data Pkts", "Fwd Seg Size Min"]
    
    testDDoSColumns = [" Total Fwd Packets", " Total Backward Packets", " Fwd Packet Length Min",
                                       " Fwd Packet Length Mean", " Fwd Packet Length Std", " Bwd Packet Length Min",
                                       " Fwd Header Length", " Bwd Header Length", " Min Packet Length", " Packet Length Mean",
                                       " PSH Flag Count", " ACK Flag Count", " URG Flag Count", " Down/Up Ratio",
                                       " Average Packet Size", " Avg Fwd Segment Size", " Subflow Bwd Packets",
                                       " act_data_pkt_fwd", " min_seg_size_forward"]

    testPortScanColumns = [" Destination Port", " Flow Duration", " Total Fwd Packets", " Total Backward Packets", 
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
                                       " act_data_pkt_fwd", " min_seg_size_forward"]

    df_DDos = data[realTimeDDoSColumns]
    df_PortScan = data[realTimePortScanColumns]

    df_DDos_array = {}
    df_PortScan_array = {}

    df_PortScan_array = pd.DataFrame({key: value.astype("float32") for key, value in df_PortScan.items()})
    df_DDos_array = pd.DataFrame({key: value.astype("float32") for key, value in df_DDos.items()})
    
    pred_DDoS = best_model_DDoS.predict(df_DDos_array)
    pred_PortScan = best_model_PortScan.predict(df_PortScan_array)

    pred_values = np.array([pred_DDoS, pred_PortScan])
    max_values = np.max(pred_values, axis=0)
    with open(monitoring_result_file_path, 'a') as file:  # Открываем файл для дописывания
        if(RealData):
            for index in range(len(pred_DDoS)):
                if(max_values[index] == 1):
                    if((max_values[index]) == pred_DDoS[index]):
                        name = 'DDoS'
                    elif((max_values[index]) == pred_PortScan[index]):
                        name = 'PortScan'
                    file.write(f'{name}\n') # - {statistic_for_output.loc[index]}
        else:
            for index in range(len(pred_DDoS)):
                if(max_values[index] == 1):
                    if((max_values[index]) == pred_DDoS[index]):
                        name = 'DDoS'
                    elif((max_values[index]) == pred_PortScan[index]):
                        name = 'PortScan'
                    file.write(f'{name}\n') # - {statistic_for_output.loc[index]}