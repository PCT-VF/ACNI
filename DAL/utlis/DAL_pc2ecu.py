import json
from pya2l.parser import A2lParser as Parser

# Đọc file A2L
def parse_a2l_file(file_path):
    try:
        with open(file_path, 'r') as file:
            a2l_string = file.read()

        # Phân tích file A2L và tạo AST
        with Parser() as p:
            ast = p.tree_from_a2l(a2l_string.encode())

        # Kiểm tra và truy xuất thông tin từ cây AST
        if hasattr(ast.PROJECT, 'MODULE') and len(ast.PROJECT.MODULE) > 0:
            module = ast.PROJECT.MODULE[0]
            module_name = module.Name.Value
            print(f"Module name: {module_name}")

            if hasattr(module, 'CHARACTERISTIC') and len(module.CHARACTERISTIC) > 0:
                characteristic = module.CHARACTERISTIC[0]
                characteristic_name = characteristic.Name.Value
                print(f"Characteristic name: {characteristic_name}")
            else:
                print("No CHARACTERISTIC found in the module.")
        else:
            print("No MODULE found in the project.")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Đường dẫn tới file A2L
a2l_file_path = "385497.a2l"

# Phân tích file A2L
parse_a2l_file(a2l_file_path)
