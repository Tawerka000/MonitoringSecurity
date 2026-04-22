data_file = open("D:\Python\MonitoringSecurityProject\Statistics\monitoring_result.txt", "r")
data_lines = data_file.readlines()
data_file.close()
value1_count = 0
value2_count = 0

for line in data_lines:
    if line.strip() == 'DDoS':
        value1_count += 1
    elif line.strip() == 'PortScan':
        value2_count += 1

print("Количество строк со значением 'value1':", value1_count)
print("Количество строк со значением 'value2':", value2_count)