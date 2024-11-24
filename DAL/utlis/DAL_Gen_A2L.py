import re
import json

def extract_measurements_and_characteristics(a2l_file):
    with open(a2l_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Tìm toàn bộ block MEASUREMENT và CHARACTERISTIC
    measurement_blocks = re.findall(r'/begin MEASUREMENT(.*?)/end MEASUREMENT', content, re.DOTALL)
    characteristic_blocks = re.findall(r'/begin CHARACTERISTIC(.*?)/end CHARACTERISTIC', content, re.DOTALL)

    measurements = []
    characteristics = []

    # Trích xuất thông tin từ block MEASUREMENT
    for block in measurement_blocks:
        measurement_info = {}
        name = re.search(r'/\* Name\s+\*/\s+(\w+)', block)
        long_identifier = re.search(r'/\* Long identifier\s+\*/\s+"(.*?)"', block)
        data_type = re.search(r'/\* Data type\s+\*/\s+(\w+)', block)
        conversion_method = re.search(r'/\* Conversion method\s+\*/\s+(\w+)', block)
        ecu_address = re.search(r'ECU_ADDRESS\s+([0xA-Fa-f0-9]+)', block)
        lower_limit = re.search(r'/\* Lower limit\s+\*/\s+(\d+)', block)
        upper_limit = re.search(r'/\* Upper limit\s+\*/\s+(\d+)', block)

        if name:
            measurement_info["Name"] = name.group(1)
        if long_identifier:
            measurement_info["Long identifier"] = long_identifier.group(1)
        if data_type:
            measurement_info["Data type"] = data_type.group(1)
        if conversion_method:
            measurement_info["Conversion method"] = conversion_method.group(1)
        if ecu_address:
            measurement_info["ECU_ADDRESS"] = ecu_address.group(1)
        if lower_limit:
            measurement_info["Lower limit"] = int(lower_limit.group(1))
        if upper_limit:
            measurement_info["Upper limit"] = int(upper_limit.group(1))

        measurements.append(measurement_info)

    # Trích xuất thông tin từ block CHARACTERISTIC
    for block in characteristic_blocks:
        characteristic_info = {}
        name = re.search(r'/\* Name\s+\*/\s+(\w+)', block)
        long_identifier = re.search(r'/\* Long Identifier\s+\*/\s+"(.*?)"', block)
        char_type = re.search(r'/\* Type\s+\*/\s+(\w+)', block)
        ecu_address = re.search(r'/\* ECU Address\s+\*/\s+([0xA-Fa-f0-9]+)', block)
        record_layout = re.search(r'/\* Record Layout\s+\*/\s+(\w+)', block)
        max_difference = re.search(r'/\* Maximum Difference\s+\*/\s+([\d.eE+-]+)', block)
        conversion_method = re.search(r'/\* Conversion Method\s+\*/\s+(\w+)', block)
        lower_limit = re.search(r'/\* Lower Limit\s+\*/\s+([\d.eE+-]+)', block)
        upper_limit = re.search(r'/\* Upper Limit\s+\*/\s+([\d.eE+-]+)', block)

        if name:
            characteristic_info["Name"] = name.group(1)
        if long_identifier:
            characteristic_info["Long Identifier"] = long_identifier.group(1)
        if char_type:
            characteristic_info["Type"] = char_type.group(1)
        if ecu_address:
            characteristic_info["ECU Address"] = ecu_address.group(1)
        if record_layout:
            characteristic_info["Record Layout"] = record_layout.group(1)
        if max_difference:
            characteristic_info["Maximum Difference"] = float(max_difference.group(1))
        if conversion_method:
            characteristic_info["Conversion Method"] = conversion_method.group(1)
        if lower_limit:
            characteristic_info["Lower Limit"] = float(lower_limit.group(1))
        if upper_limit:
            characteristic_info["Upper Limit"] = float(upper_limit.group(1))

        characteristics.append(characteristic_info)

    return measurements, characteristics


# Đường dẫn tới file A2L
a2l_file = "385497.a2l"
measurements, characteristics = extract_measurements_and_characteristics(a2l_file)

# Lưu kết quả ra file JSON
output_file = "385497.json"
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump({
        "Measurements": measurements,
        "Characteristics": characteristics
    }, json_file, ensure_ascii=False, indent=4)

print(f"Dữ liệu đã được lưu ra file JSON: {output_file}")
