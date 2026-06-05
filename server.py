from flask import Flask, request
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
DATA_FILE = "traffic_log.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["timestamp", "hour", "duration_ms", "anomaly_flag"])
    df.to_csv(DATA_FILE, index=False)

@app.route('/api/log', methods=['POST'])
def log_data():
    duration_ms = int(request.form.get('duration_ms', 0))
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_hour = datetime.now().hour
    
    df = pd.read_csv(DATA_FILE)
    anomaly_flag = 0
    response_msg = "OK"
    
  
    is_dynamic_anomaly = False
    if len(df) >= 5:
        recent_entries = df.tail(5)
        avg_duration = recent_entries['duration_ms'].mean()
        if duration_ms > (avg_duration * 3):
            is_dynamic_anomaly = True
            
    if is_dynamic_anomaly or duration_ms > 4000:
        anomaly_flag = 1
        response_msg = "ALARM"
        print(f"⚠️ ANOMALY DETECTED AT {timestamp}!")
            
    new_data = pd.DataFrame([[timestamp, current_hour, duration_ms, anomaly_flag]], 
                            columns=["timestamp", "hour", "duration_ms", "anomaly_flag"])
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    
    print(f"Logged: {timestamp} | Duration: {duration_ms}ms | Anomaly: {anomaly_flag}")
    return response_msg

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)