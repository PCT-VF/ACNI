import json
import can
import pyxcp
from pyxcp import xcp

# Đọc dữ liệu từ file JSON chứa Measurements và Characteristics
def read_a2l_data_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    measurements = data.get("Measurements", [])
    characteristics = data.get("Characteristics", [])
    
    return measurements, characteristics

# Thiết lập kết nối CAN với pyxcp
def setup_can_channel(channel='can0', bitrate=500000):
    bus = can.interface.Bus(channel=channel, bustype='socketcan', bitrate=bitrate)
    return bus

# Viết giá trị vào ECU sử dụng XCP
def write_to_ecu(variable_name, value, characteristics, bus):
    # Tìm thông tin characteristic trong dictionary
    characteristic = next((item for item in characteristics if item["Name"] == variable_name), None)
    
    if characteristic:
        ecu_address = characteristic["ECU Address"]
        print(f"Writing value {value} to ECU address {ecu_address}")
        
        # Thiết lập phiên làm việc XCP
        session = xcp.XCPSession(bus)
        
        # Địa chỉ ECU là một phần quan trọng trong XCP, chuyển đổi nó thành giá trị hợp lệ
        ecu_address = int(ecu_address, 16)  # Chuyển chuỗi HEX sang int
        
        # Tạo message XCP và gửi yêu cầu ghi giá trị vào ECU
        # Ở đây bạn cần thiết lập cấu hình của ECU và phương thức write tương ứng
        session.set_address(ecu_address)
        session.write(variable_name, value)
        
        print(f"Sent XCP write command to ECU {ecu_address} with value {value}")
    else:
        print(f"Variable {variable_name} not found in Characteristics")

# Đọc giá trị từ ECU sử dụng XCP
def read_from_ecu(variable_name, measurements, bus):
    # Tìm thông tin measurement trong dictionary
    measurement = next((item for item in measurements if item["Name"] == variable_name), None)
    
    if measurement:
        ecu_address = measurement["ECU_ADDRESS"]
        print(f"Reading value from ECU address {ecu_address}")
        
        # Thiết lập phiên làm việc XCP
        session = xcp.XCPSession(bus)
        
        # Địa chỉ ECU là một phần quan trọng trong XCP, chuyển đổi nó thành giá trị hợp lệ
        ecu_address = int(ecu_address, 16)  # Chuyển chuỗi HEX sang int
        
        # Tạo message XCP và gửi yêu cầu đọc giá trị từ ECU
        session.set_address(ecu_address)
        value = session.read(variable_name)
        
        print(f"Received value from ECU {ecu_address}: {value}")
        return value
    else:
        print(f"Variable {variable_name} not found in Measurements")
        return None

# Đọc dữ liệu từ file JSON
json_file = "385497.json"
measurements, characteristics = read_a2l_data_from_json(json_file)

# Thiết lập kết nối CAN
bus = setup_can_channel()

# Ví dụ sử dụng hàm ghi và đọc với pyxcp
write_to_ecu("S2S_WindowCAppControlRL_Dummy", 100, characteristics, bus)
value = read_from_ecu("COM_RightStalkSwitchSts", measurements, bus)
print(f"Value read from ECU: {value}")
