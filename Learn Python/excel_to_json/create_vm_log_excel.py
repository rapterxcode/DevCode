import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# สร้างข้อมูลตัวอย่าง
np.random.seed(42)

# สร้างช่วงเวลา
start_time = datetime(2024, 1, 1, 0, 0, 0)
time_interval = timedelta(minutes=5)
times = [start_time + (time_interval * i) for i in range(100)]

# สร้างรายการ VM
vm_names = [f'ubuntu-vm-{i:02d}' for i in range(1, 6)]

# สร้างรายการ services
services = [
    'grafana-server',
    'prometheus',
    'node-exporter',
    'nginx',
    'postgresql',
    'docker',
    'systemd'
]

# สร้างระดับความรุนแรง
severity_levels = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']

# สร้างข้อมูล
data = {
    'timestamp': [],
    'vm_name': [],
    'service': [],
    'severity': [],
    'message': [],
    'cpu_usage': [],
    'memory_usage': [],
    'disk_usage': [],
    'network_in': [],
    'network_out': []
}

# สร้างข้อมูล log
for time in times:
    vm = random.choice(vm_names)
    service = random.choice(services)
    severity = random.choices(severity_levels, weights=[60, 25, 10, 5])[0]
    
    # สร้างข้อความ log
    if severity == 'INFO':
        message = f"Service {service} is running normally"
    elif severity == 'WARNING':
        message = f"High resource usage detected for {service}"
    elif severity == 'ERROR':
        message = f"Failed to start {service}"
    else:
        message = f"Critical failure in {service}"

    # สร้างข้อมูล metrics
    cpu = np.random.uniform(10, 90)
    memory = np.random.uniform(20, 80)
    disk = np.random.uniform(30, 95)
    net_in = np.random.uniform(100, 1000)
    net_out = np.random.uniform(100, 1000)

    # เพิ่มข้อมูลลงใน dictionary
    data['timestamp'].append(time)
    data['vm_name'].append(vm)
    data['service'].append(service)
    data['severity'].append(severity)
    data['message'].append(message)
    data['cpu_usage'].append(round(cpu, 2))
    data['memory_usage'].append(round(memory, 2))
    data['disk_usage'].append(round(disk, 2))
    data['network_in'].append(round(net_in, 2))
    data['network_out'].append(round(net_out, 2))

# สร้าง DataFrame
df = pd.DataFrame(data)

# บันทึกเป็นไฟล์ Excel
excel_file = 'ubuntu_vm_logs.xlsx'

# สร้าง Excel writer
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    # บันทึกข้อมูล log
    df.to_excel(writer, sheet_name='VM Logs', index=False)
    
    # สร้าง sheet สรุปข้อมูล
    summary_data = {
        'Metric': ['Total Logs', 'Error Logs', 'Warning Logs', 'Critical Logs'],
        'Count': [
            len(df),
            len(df[df['severity'] == 'ERROR']),
            len(df[df['severity'] == 'WARNING']),
            len(df[df['severity'] == 'CRITICAL'])
        ]
    }
    pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

print(f"สร้างไฟล์ Excel ตัวอย่างเรียบร้อยแล้ว: {excel_file}")
print("\nตัวอย่างข้อมูล Log:")
print(df.head()) 