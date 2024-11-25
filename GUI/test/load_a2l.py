from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QScrollArea, QLabel, QHBoxLayout, QCheckBox, QLineEdit, QPushButton, QHeaderView
from PyQt5.QtCore import Qt, QTimer
import random
import json
import sys

def process_item(item, key):
    """
    Lấy giá trị từ key trong item, nếu không tồn tại thì trả về 'Unknown'.
    """
    key_variants = [key, key.replace(" ", "_").upper()]
    for variant in key_variants:
        if variant in item:
            return str(item[variant])  # Trả về giá trị nếu tìm thấy
    return "Unknown"

class A2LViewer(QMainWindow):
    def __init__(self, measurements, characteristics):
        super().__init__()
        self.setWindowTitle("A2L Data Viewer")
        self.resize(2400, 900)

        # Giao diện chính
        main_layout = QHBoxLayout()

        # Tạo hai vùng scroll riêng biệt
        self.measurement_table = self.create_table(
            "Measurements", measurements, ["STT", "Name", "ECU Address", "Select", "Value"]
        )
        self.characteristic_table = self.create_table(
            "Characteristics", characteristics, ["STT", "Name", "ECU Address", "Select", "Value", "Write", "Command"]
        )

        # Điều chỉnh kích thước phần Measurement
        measurement_scroll_area = self.create_scroll_area("Measurements", self.measurement_table)
        measurement_scroll_area.setMinimumWidth(800)

        # Điều chỉnh kích thước phần Characteristics
        characteristic_scroll_area = self.create_scroll_area("Characteristics", self.characteristic_table)
        characteristic_scroll_area.setMinimumWidth(1400)

        # Tạo nút Sort bên ngoài bảng
        sort_button_1 = QPushButton("Sort Measurements Selected")
        sort_button_1.clicked.connect(lambda: self.sort_checked_items(self.measurement_table))

        sort_button_2 = QPushButton("Sort Characteristics Selected")
        sort_button_2.clicked.connect(lambda: self.sort_checked_items(self.characteristic_table))

        # Đặt nút Sort ở phía trên cùng
        button_layout = QVBoxLayout()
        button_layout.addWidget(sort_button_1)
        button_layout.addWidget(sort_button_2)

        main_layout.addWidget(measurement_scroll_area)
        main_layout.addWidget(characteristic_scroll_area)
        main_layout.addLayout(button_layout)

        # Cài đặt layout chính
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Khởi tạo timer để cập nhật giá trị mỗi giây
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all_values)
        self.timer.start(1000)

    def create_scroll_area(self, title, table_widget):
        """
        Tạo một khu vực cuộn với bảng và tiêu đề.
        """
        header_label = QLabel(title)
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table_widget)

        layout = QVBoxLayout()
        layout.addWidget(header_label)
        layout.addWidget(scroll_area)

        container = QWidget()
        container.setLayout(layout)

        return container

    def create_table(self, title, data, headers):
        """
        Tạo bảng dữ liệu với cột Command mới bên cạnh cột Write.
        """
        table_widget = QTableWidget()
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))

        # Điền dữ liệu vào bảng
        for row, item in enumerate(data):
            table_widget.setItem(row, 0, QTableWidgetItem(str(row + 1)))  # STT
            table_widget.setItem(row, 1, QTableWidgetItem(process_item(item, "Name")))
            table_widget.setItem(row, 2, QTableWidgetItem(process_item(item, "ECU Address")))

            checkbox = QCheckBox()
            checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")
            checkbox_widget = QWidget()
            checkbox_layout = QVBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            table_widget.setCellWidget(row, 3, checkbox_widget)

            value_item = QTableWidgetItem("")
            table_widget.setItem(row, 4, value_item)

            if title == "Characteristics":
                write_input = QLineEdit()
                write_input.setPlaceholderText("Enter value")
                table_widget.setCellWidget(row, 5, write_input)

                write_button = QPushButton("Write")
                write_button.clicked.connect(lambda _, r=row, t=table_widget: self.write_value(r, t))
                table_widget.setCellWidget(row, 6, write_button)

                command_button = QPushButton("Command")
                command_button.clicked.connect(lambda _, r=row, t=table_widget: self.copy_value_from_write(r, t))
                table_widget.setCellWidget(row, 7, command_button)

        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        table_widget.resizeColumnsToContents()
        table_widget.setAlternatingRowColors(True)

        return table_widget

    def write_value(self, row, table_widget):
        """
        Xử lý sự kiện khi nút Write được bấm.
        """
        write_widget = table_widget.cellWidget(row, 5)  # Lấy widget của cột "Write"
        value_item = table_widget.item(row, 4)  # Lấy item của cột "Value"

        if write_widget:
            write_value = write_widget.text()  # Lấy giá trị từ ô nhập vào cột "Write"
            value_item.setText(write_value)  # Gán giá trị đó vào cột "Value"

    def copy_value_from_write(self, row, table_widget):
        """
        Xử lý sự kiện khi nút "Command" được nhấn.
        """
        write_widget = table_widget.cellWidget(row, 5)  # Lấy widget của cột "Write"
        value_item = table_widget.item(row, 4)  # Lấy item của cột "Value"

        if write_widget:
            write_value = write_widget.text()  # Lấy giá trị từ ô nhập vào cột "Write"
            value_item.setText(write_value)  # Gán giá trị đó vào cột "Value"

    def update_all_values(self):
        """
        Cập nhật giá trị ở cột "Value" cho tất cả checkbox được chọn.
        """
        for table in [self.measurement_table, self.characteristic_table]:
            row_count = table.rowCount()
            for row in range(row_count):
                checkbox_widget = table.cellWidget(row, 3)
                if checkbox_widget:
                    checkbox = checkbox_widget.layout().itemAt(0).widget()
                    value_item = table.item(row, 4)
                    if value_item:  # Kiểm tra nếu value_item không phải là None
                        if checkbox.isChecked():
                            value_item.setText(str(random.randint(1, 1000)))
                        else:
                            value_item.setText("")

    def sort_checked_items(self, table):
        """
        Sắp xếp các hàng trong bảng sao cho các hàng có checkbox được tick sẽ lên ngoài bảng trên.
        """
        row_count = table.rowCount()

        selected_rows = []
        remaining_rows = []
        
        for row in range(row_count):
            checkbox_widget = table.cellWidget(row, 3)
            checkbox = checkbox_widget.layout().itemAt(0).widget() if checkbox_widget else None
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)
            else:
                remaining_rows.append(row)

        selected_items = []
        for row in selected_rows:
            row_items = []
            for column in range(table.columnCount()):
                item = table.takeItem(row, column)
                row_items.append(item)
            selected_items.append(row_items)

        for row in remaining_rows:
            table.removeRow(row)

        for row_items in reversed(selected_items):
            row_position = table.rowCount()
            table.insertRow(row_position)
            for column, item in enumerate(row_items):
                table.setItem(row_position, column, item)

        for row in remaining_rows:
            row_position = table.rowCount()
            table.insertRow(row_position)
            for column in range(table.columnCount()):
                item = table.takeItem(row, column)
                table.setItem(row_position, column, item)

        table.resizeRowsToContents()


# Hàm đọc JSON
def read_a2l_data_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    measurements = data.get("Measurements", [])
    characteristics = data.get("Characteristics", [])
    
    return measurements, characteristics


# Đọc dữ liệu từ file JSON
json_file = "385497.json"  # Thay đổi tên file nếu cần
measurements, characteristics = read_a2l_data_from_json(json_file)

# Khởi tạo ứng dụng và hiển thị cửa sổ
app = QApplication(sys.argv)
window = A2LViewer(measurements, characteristics)
window.show()
sys.exit(app.exec_())
