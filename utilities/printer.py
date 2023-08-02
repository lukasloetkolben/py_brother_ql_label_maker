import subprocess
from pathlib import Path

from brother_ql.labels import ALL_LABELS


def get_label_by_name(label_name):
    for label in ALL_LABELS:
        if label.name == label_name:
            return label


def get_label_by_identifier(ident):
    for label in ALL_LABELS:
        if label.identifier == ident:
            return label


def run_brother_ql_command(model: str, identifier: str, label: str, file: Path):
    try:
        # Execute the command and capture the output
        command = f"brother_ql -b pyusb -m {model} -p {identifier} print -l {label} {str(file)}"
        print(command)
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

# def find_connected_brother_ql_printers():
#     vendor_id = 0x04f9  # Brother's Vendor ID
#     product_id = 0x2015  # Brother's Product ID for QL printers
#
#     printers = []
#
#     # Find all USB devices with the given vendor and product IDs
#     usb_devices = usb.core.find(find_all=True, idVendor=vendor_id, idProduct=product_id)
#
#     for dev in usb_devices:
#         # Get the device descriptor
#         dev_descriptor = usb.util.get_string(dev, dev.iProduct)
#
#         # Append the identifier in the desired format to the list of printers
#         identifier = f"usb://{vendor_id:04x}:{product_id:04x}/{dev_descriptor}"
#         printers.append(identifier)
#
#     return printers
#
# if __name__ == "__main__":
#     connected_printers = find_connected_brother_ql_printers()
#
#     if connected_printers:
#         for printer in connected_printers:
#             print(printer)
#     else:
#         print("No Brother QL printers found.")
#
