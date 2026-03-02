import json
import os
import sys

MANIFEST_FILE = "boards_manifest.json"
TARGET_HEADER = "boards_target.h"

# Global Defaults (Mirroring Boards.h logic)
DEFAULTS = {
    "VALIDATE_FIRMWARE": "true",
    "GPS_BAUD_RATE": 9600,
    "EEPROM_SIZE": 1024,
    "DISPLAY_SCALE": 1,
    "HAS_DISPLAY": "false",
    "HAS_GPS": "false",
    "HAS_TCXO": "false",
    "PIN_DISP_SLEEP": -1,
    "OCP_TUNED": "0x00",
    "CONFIG_UART_BUFFER_SIZE": 6144,
    "CONFIG_QUEUE_0_SIZE": 6144,
    "CONFIG_QUEUE_MAX_LENGTH": 200
}

def load_manifest():
    if not os.path.exists(MANIFEST_FILE):
        print(f"Error: {MANIFEST_FILE} not found.")
        sys.exit(1)
    with open(MANIFEST_FILE, "r") as f:
        return json.load(f)

def run_menu():
    manifest = load_manifest()
    boards = manifest.get("boards", [])

    print("\n--- RNode Firmware Configuration ---")
    for i, board in enumerate(boards):
        print(f"{i}) {board.get('display_name', board['name'])} [{board['mcu']}]")

    try:
        board_idx = int(input("\nSelect target board: "))
        selected_board = boards[board_idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    models = selected_board.get("models", [])
    print(f"\nVariants for {selected_board['display_name']}:")
    for i, model in enumerate(models):
        print(f"{i}) {model['display_name']}")

    try:
        model_idx = int(input("\nSelect board model: "))
        selected_model = models[model_idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # 1. Start with Global Defaults
    config = DEFAULTS.copy()

    # 2. Apply Board Identity & Platform
    config.update({
        "BOARD_ID": selected_board['board_id'],
        "BOARD_MODEL": selected_board['product'],
        "BOARD_VARIANT": selected_model['model'],
        "PLATFORM": f"PLATFORM_{selected_board['platform']}",
        "MCU_VARIANT": selected_board['mcu'],
        "TARGET_FQBN": f"\"{selected_board['fqbn']}\""
    })

    # 3. Apply Capabilities & Memory
    caps = selected_board.get("capabilities", {})
    config["HAS_DISPLAY"] = str(caps.get("has_display", False)).lower()
    config["HAS_GPS"] = str(caps.get("has_gps", False)).lower()
    config["HAS_TCXO"] = str(caps.get("has_tcxo", False)).lower()

    mem = selected_board.get("memory", {})
    if "eeprom_size" in mem: config["EEPROM_SIZE"] = mem["eeprom_size"]
    if "uart_buffer_size" in mem: config["CONFIG_UART_BUFFER_SIZE"] = mem["uart_buffer_size"]

    # 4. Apply Display & GPS (with pin_ prefix mapping)
    disp = selected_board.get("display", {})
    if "pin_scl" in disp: config["PIN_SCL"] = disp["pin_scl"]
    if "pin_sda" in disp: config["PIN_SDA"] = disp["pin_sda"]
    if "pin_rst" in disp: config["PIN_RST"] = disp["pin_rst"]
    if "pin_disp_sleep" in disp: config["PIN_DISP_SLEEP"] = disp["pin_disp_sleep"]

    if config["HAS_GPS"] == "true":
        gps = selected_board.get("gps", {})
        config["GPS_BAUD_RATE"] = gps.get("baud", 9600)
        config["PIN_GPS_RX"] = gps.get("pin_rx", -1)
        config["PIN_GPS_TX"] = gps.get("pin_tx", -1)

    # 5. Apply Model Pins & Deviations
    model_pins = selected_model.get("pins", {})
    for k, v in model_pins.items():
        if k.startswith("pin_"):
            macro_name = k.upper()
            config[macro_name] = v

    if "ocp_tuned" in selected_model:
        config["OCP_TUNED"] = selected_model["ocp_tuned"]

    # Generate the single-target header
    with open(TARGET_HEADER, "w") as f:
        f.write("// Auto-generated Target Configuration\n")
        f.write("#ifndef BOARDS_TARGET_H\n#define BOARDS_TARGET_H\n")
        f.write("#define USING_BOARDS_TARGET_H\n\n")
        for key, value in config.items():
            f.write(f"#define {key} {value}\n")
        f.write("\n#endif // BOARDS_TARGET_H\n")

    print(f"\nConfiguration saved to {TARGET_HEADER}")
    print(f"Target FQBN: {selected_board['fqbn']}")

if __name__ == "__main__":
    run_menu()