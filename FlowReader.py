from datetime import datetime
import os
import pandas as pd

class Reader():

    def readRealTime(self):
        folder_path = 'C:\\Users\\tawer\\Downloads\\CICFlowmeter\\bin\\data\\daily'
        today_date = datetime.now().strftime('%Y-%m-%d')
        file_name = f"{today_date}_Flow.csv"
        file_path = os.path.join(folder_path, file_name)
        data = []
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
            os.remove(file_path)
            if(data.empty):
                return data, True
            else:
                return data, False
        return data, True
    def readRawData(self):
        file_path = 'D:\\Python\\MonitoringSecurityProject\\Datasets\\NewDataSets\\RealData.csv'
        data = []
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
            if(data.empty):
                return data, True
            else:
                return data, False
        return data, True
        