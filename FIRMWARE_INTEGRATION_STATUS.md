# RNode Firmware CE - Integration Status

## Current Branch
**`claude/review-repo-updates-8VfF2`** - T-Deck feature expansion (WiFi, GPS, keyboard)

## Integration Overview

This branch represents a major refactoring of the RNode firmware protocol layer, with corresponding updates to the rnodeconf utility in the Reticulum repository.

### What Changed

#### Previous Session (branch: `claude/update-rnodeconf-firmware-KmoUs`)
- **Radio Control Enhancements**: Implicit header mode, air lock controls (short-term & long-term)
- **Advanced Statistics**: Channel time, physical parameters, battery level, CSMA metrics
- **Flashblock I/O**: Read/write operations for external flash storage
- **System Features**: Logging, time synchronization, interface selection, GPS support, mux chain/discovery
- **Display Enhancements**: Display read capability, improved rotation control
- **Bluetooth**: Unpair command for cleaner device management
- Protocol reorganized: commands moved into `Framing.h`, new error codes, `CMD_UNLOCK_ROM`

#### This Session (branch: `claude/review-repo-updates-8VfF2`)
- **T-Deck: WiFi enabled** — `HAS_CONSOLE true` in `Boards.h`; the existing `Console.h` WiFi AP is now compiled in for T-Deck builds
- **T-Deck: GPS enabled** — `HAS_GPS true`, `GPS_BAUD_RATE 9600`, `PIN_GPS_RX 5`, `PIN_GPS_TX 6` added to `Boards.h`; activates the existing TinyGPS+/SoftwareSerial pipeline; **GPS pins need hardware verification for your specific T-Deck variant**
- **T-Deck: I2C defined** — `I2C_SDA 18`, `I2C_SCL 8` added (shared bus for keyboard and trackball)
- **T-Deck: keyboard support** — new `HAS_KEYBOARD` flag, `KEYBOARD_ADDR 0x55`, and new `Keyboard.h` driver that polls the I2C keyboard MCU and emits key presses as `CMD_KEYBOARD (0xA1)` KISS frames
- **Framing.h** — added `CMD_KEYBOARD (0xA1)` and `KEYBOARD_CMD_KEY (0x00)` subcommand
- **rnodeconf.py** — added `KISS.CMD_KEYBOARD`, `GPS_CMD_LAT/LNG`, `KEYBOARD_CMD_KEY` constants; GPS and keyboard KISS frame parsers in `readLoop()`; `r_gps_latitude`, `r_gps_longitude`, `r_keyboard_key` fields on `RNode`

#### WiFi Configuration Commands (still pending firmware-side)
- `CMD_WIFI_MODE (0x6A)`, `CMD_WIFI_SSID (0x6B)`, `CMD_WIFI_PSK (0x6C)`, `CMD_WIFI_CHN (0x6E)`
- `CMD_WIFI_IP (0x84)`, `CMD_WIFI_NM (0x85)`, `CMD_CFG_READ (0x6D)`
- rnodeconf already has full implementations of these; firmware command handlers still need adding

## Validation Status

### ✅ Validated Components
- Device detection and identification
- EEPROM reading and integrity checking
- Firmware signature validation
- Device provisioning verification
- Configuration storage validation
- Basic radio parameter validation

### ⚠️ WiFi Feature Status
- **AP Mode**: `HAS_CONSOLE true` now enabled for T-Deck — the WiFi AP (Console.h) compiles and runs
- **Config Commands**: `CMD_WIFI_*` KISS command handlers are NOT yet implemented in firmware; rnodeconf `--wifi`, `--ssid`, `--psk`, etc. will send frames but the device won't respond
- **rnodeconf Integration**: Full WiFi config methods exist in rnodeconf.py, gracefully stubbed with try/except
- **Next**: Implement `CMD_WIFI_*` handlers in `RNode_Firmware_CE.ino` `serial_callback()`

### ⚠️ GPS Pin Status
- T-Deck GPS pins set to `PIN_GPS_RX 5`, `PIN_GPS_TX 6` as reasonable defaults
- **Must be verified** against the physical T-Deck variant (T-Deck vs T-Deck Plus, hardware revision)
- Refer to LilyGO T-Deck schematic or factory test code, or Meshtastic T-Deck variant definitions

## Integration with Reticulum rnodeconf

The Reticulum repository's `rnodeconf.py` has been updated to:
- ✅ Recognize all new firmware commands
- ✅ Process new statistics from device
- ✅ Handle new error codes with specific messages
- ✅ Support graceful WiFi feature stub
- ✅ Maintain backward compatibility with existing validation flow
- ✅ Parse `CMD_GPS` frames → `r_gps_latitude` / `r_gps_longitude` (signed int32 × 10⁻⁶)
- ✅ Parse `CMD_KEYBOARD` frames → `r_keyboard_key` with printable-char logging
- ✅ `KISS.CMD_KEYBOARD (0xA1)`, `GPS_CMD_LAT/LNG`, `KEYBOARD_CMD_KEY` constants added

**Sync Status**: Both repos synchronized on branch `claude/review-repo-updates-8VfF2`.

## Next Steps

### 1. Verify T-Deck GPS Pins (Before flashing)
Confirm `PIN_GPS_RX` and `PIN_GPS_TX` in `Boards.h` match the physical hardware:
- Check LilyGO T-Deck schematic/factory test code at `github.com/Xinyuan-LilyGO/T-Deck`
- Cross-reference with Meshtastic T-Deck Plus variant definitions
- Update `Boards.h` if pins differ from the current placeholder values (RX=5, TX=6)

### 2. Implement WiFi Config Command Handlers in Firmware (High Priority)
**Location**: `RNode_Firmware_CE.ino` → `serial_callback()`
**rnodeconf**: Already fully implemented — no changes needed there

Add `else if` cases for:
- `CMD_WIFI_MODE (0x6A)` — set WiFi mode (OFF / AP / STATION), persist to EEPROM
- `CMD_WIFI_SSID (0x6B)` — store SSID to SPIFFS
- `CMD_WIFI_PSK (0x6C)` — store PSK to SPIFFS
- `CMD_WIFI_CHN (0x6E)` — set channel, persist to EEPROM
- `CMD_WIFI_IP (0x84)` / `CMD_WIFI_NM (0x85)` — static IP config, persist to EEPROM
- `CMD_CFG_READ (0x6D)` — read back current WiFi config and send to host

### 3. T-Deck Display (`HAS_DISPLAY`)
Currently `false` / "to be tested". The ST7789 TFT driver exists but is not active. Next: enable `HAS_DISPLAY true`, compile, validate display initialisation on real hardware.

### 4. Remaining Feature Implementation
- **Logging** (`CMD_LOG`): Firmware serial debug logging channel
- **Flashblock** (`CMD_FB_*`): External flash read/write
- **System time** (`CMD_TIME`): Time synchronisation

### 5. Testing Requirements
- [ ] Verify T-Deck GPS pin assignment against hardware before flashing
- [ ] Flash T-Deck and confirm GPS NMEA sentences received (serial monitor)
- [ ] Confirm keyboard I2C polling works (key presses appear in rnodeconf log)
- [ ] Test WiFi AP comes up — connect to device AP on 10.0.0.1
- [ ] Validate device detection with refactored firmware (`rnodeconf --info`)
- [ ] Test EEPROM reading and parsing
- [ ] Verify signature validation still works
- [ ] Test new statistics reception (CHTM, PHYPRM, BAT, CSMA)
- [ ] Verify new error codes are properly logged

## File Structure Reference

### Firmware Side
- **Framing.h**: Command definitions and protocol constants
- **RNode_Firmware_CE.ino**: Main firmware with command handling
- **Radio.cpp/hpp**: Radio parameter handling
- **Utilities.h**: Hardware utility functions

### rnodeconf Side
- **RNS/Utilities/rnodeconf.py**: Device configuration and validation utility
  - Lines 73-158: KISS class with all command definitions
  - Lines 428-482: RNode class with state variables
  - Lines 488-760: readLoop() command processing
  - Lines 3828-3833: WiFi feature stub with error handling

## Backport Checklist

For WiFi feature restoration:

```
[ ] Restore WiFi module to firmware
[ ] Implement CMD_WIFI_MODE command handling
[ ] Implement CMD_WIFI_SSID command handling
[ ] Implement CMD_WIFI_PSK command handling
[ ] Implement CMD_WIFI_CHN command handling
[ ] Implement CMD_WIFI_IP command handling
[ ] Implement CMD_WIFI_NM command handling
[ ] Implement CMD_CFG_READ command handling
[ ] Test WiFi configuration reading with rnodeconf
[ ] Verify configuration display in rnodeconf --config
```

## Development Notes

### Branch Purpose
This branch represents a clean separation of concerns:
- Firmware focuses on refactored protocol implementation
- rnodeconf focuses on device validation and configuration
- Clear interfaces between components via KISS protocol

### Compatibility Considerations
- New commands are backward compatible (old firmware will ignore unknown commands)
- Old commands are preserved for compatibility where possible
- WiFi feature can be restored independently without breaking validation flow

### Known Limitations
1. WiFi configuration is unavailable until feature is restored to firmware
2. Advanced statistics (CHTM, PHYPRM, BAT, CSMA) reception in place but not yet displayed by rnodeconf
3. GPS, logging, and flashblock features have command definitions but no rnodeconf UI yet

## Contact & Questions

For integration questions or issues:
- Check both repo branches are on `claude/update-rnodeconf-firmware-KmoUs`
- Review Framing.h command definitions against rnodeconf KISS class
- Verify readLoop handlers match expected command responses
