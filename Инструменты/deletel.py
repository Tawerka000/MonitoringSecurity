import pandas as pd
from sklearn.model_selection import train_test_split

ddos = pd.read_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')
portscan = pd.read_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv')
bot = pd.read_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\Friday-WorkingHours-Morning.pcap_ISCX.csv')

ddos = ddos.sample(frac=1).reset_index(drop=True)
portscan = portscan.sample(frac=1).reset_index(drop=True)
bot = bot.sample(frac=1).reset_index(drop=True)

ddos_train, ddos_real = train_test_split(ddos, test_size=0.1)
portscan_train, portscan_real = train_test_split(portscan, test_size=0.1)
bot_train, bot_real = train_test_split(bot, test_size=0.1)

real_part = pd.concat([ddos_real, portscan_real, bot_real], ignore_index=True)
real_part = real_part.sample(frac=1).reset_index(drop=True)
real_part.to_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\NewDataSets\\RealData.csv')

ddos_train.to_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\NewDataSets\\DDoS_train.csv')
portscan_train.to_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\NewDataSets\\PortScan_train.csv')
bot_train.to_csv('D:\\Python\\MonitoringSecurityProject\\Datasets\\NewDataSets\\Bot_train.csv')