# RNode Firmware CE - Testing and Validation Guide

## Quick Start

For rapid iteration: **Flash → Validate → Test → Debug**

```bash
# After building and flashing firmware
rnodeconf /dev/ttyUSB0 --info      # Step 1: Validate device
rnodeconf /dev/ttyUSB0 --tnc       # Step 2: Enable TNC mode
meshchat                             # Step 3: Test with application
```

## Prerequisites

### Hardware
- RNode device (any supported board)
- USB cable for flashing and serial communication
- USB-to-serial adapter (if needed)

### Software
```bash
# Build firmware (assuming Arduino/esptool workflow)
# (See README.md for platform-specific build instructions)

# Install Reticulum and rnodeconf
pip install rns
# OR from source:
git clone https://github.com/markqvist/Reticulum
cd Reticulum && pip install -e .
```

## Phase 1: Firmware Validation

### Step 1.1: Device Detection
```bash
rnodeconf /dev/ttyUSB0 --info
```

**Expected Output**:
```
RNode detected
Device detected
Current firmware version: X.XX
Provisioned: Yes
...
```

**Failure Scenarios**:
- "No RNode found": Check USB connection, baud rate
- "Invalid response while detecting": Firmware may not be flashing correctly
- Timeout: Device not responding, check serial port name

### Step 1.2: Full Device Probe
```bash
rnodeconf /dev/ttyUSB0 --info -v
```

The `-v` flag shows verbose output with:
- Serial port opening/closing
- KISS frame transmission
- Command responses received
- Timing information

**What to verify**:
```
✅ Radio reporting frequency is XXX.XXX MHz
✅ Radio reporting bandwidth is XXX.XX KHz
✅ Radio reporting TX power is XX dBm
✅ Radio reporting spreading factor is X
✅ Radio reporting coding rate is X
✅ EEPROM checksum correct
✅ Device signature validated
```

### Step 1.3: Configuration Inspection
```bash
rnodeconf /dev/ttyUSB0 --config
```

**Expected behavior**:
- Shows current device settings
- If WiFi unavailable: "Could not read WiFi configuration" message (non-fatal)
- Should NOT hang or crash

**Sample output**:
```
Device configuration:
  Bluetooth              : Enabled
  WiFi                   : Disabled (or unavailable message)
  Interference avoidance : Enabled
  Display brightness     : 200
  Display address        : Default
  ...
```

## Phase 2: TNC Mode Configuration

### Step 2.1: Switch to TNC Mode
```bash
rnodeconf /dev/ttyUSB0 --tnc
```

**Expected**:
- Device resets into TNC mode
- Takes 2-3 seconds
- Returns to prompt

### Step 2.2: Verify TNC Mode Active
```bash
rnodeconf /dev/ttyUSB0 --info
```

Should show device is in TNC mode (ready for Reticulum communication)

### Step 2.3: Set Radio Parameters (if needed)
```bash
# Example: Set frequency for EU 868 MHz band
rnodeconf /dev/ttyUSB0 -f 868000000 -b 125000 -p 17 -s 7 -c 5
```

Parameters:
- `-f`: Frequency in Hz
- `-b`: Bandwidth in Hz
- `-p`: TX Power in dBm
- `-s`: Spreading Factor (7-12)
- `-c`: Coding Rate (5-8)

## Phase 3: Reticulum Integration

### Step 3.1: Configure Reticulum
Edit `~/.config/Reticulum/config`:

```yaml
[[RNode Interface]]
  Type = RNode
  Port = /dev/ttyUSB0
  Frequency = 868000000
  Bandwidth = 125000
  TX Power = 17
  Spreading Factor = 7
  Coding Rate = 5
```

### Step 3.2: Test RNS Initialization
```bash
python3 << 'EOF'
import RNS
print("Initializing Reticulum...")
reticulum = RNS.Reticulum()
print("✓ RNS initialized successfully")
print(f"✓ Node ID: {RNS.hexrep(reticulum.identity.hash)}")

# List interfaces
print("\nActive interfaces:")
for iface in reticulum.interfaces:
    print(f"  - {iface}")
EOF
```

**Expected**:
- Initialization completes without errors
- RNode interface appears in interface list
- No serial port errors

### Step 3.3: Debug Mode Testing
```bash
python3 << 'EOF'
import RNS

# Enable debug logging
RNS.loglevel = RNS.LOG_DEBUG

print("Initializing with debug output...")
reticulum = RNS.Reticulum()

# Check interface details
for iface in reticulum.interfaces:
    print(f"\nInterface: {iface}")
    if hasattr(iface, 'bitrate'):
        print(f"  Bitrate: {iface.bitrate} kbps")
    if hasattr(iface, 'r_frequency'):
        print(f"  Frequency: {iface.r_frequency} Hz")
EOF
```

## Phase 4: Application Testing

### Step 4.1: meshchat
```bash
meshchat
```

**In meshchat**:
- Press `n` to create new identity (if first time)
- Should show your node in peer list
- Can send test message to yourself
- Check message appears in chat

### Step 4.2: nomadnet
```bash
nomadnet
```

**In nomadnet**:
- Should connect to network
- Should show local node
- Browse directory (if available)
- Can ping other nodes on network

### Step 4.3: Direct RNS Testing
```bash
python3 << 'EOF'
import RNS
import time

# Initialize
RNS.loglevel = RNS.LOG_NOTICE
reticulum = RNS.Reticulum()

# Create an echo destination
class EchoDestination(RNS.Destination):
    def __init__(self):
        super().__init__(None, RNS.Destination.IN, RNS.Destination.SINGLE)

    def packet_received(self, data, packet):
        print(f"Received {len(data)} bytes from {RNS.hexrep(packet.sender_id)}")

echo = EchoDestination()
print(f"Created echo destination: {RNS.hexrep(echo.hash)}")
print(f"Your node: {RNS.hexrep(reticulum.identity.hash)}")

# Give network time to settle
print("Waiting for network settle...")
time.sleep(5)

print("✓ Test environment ready for manual testing")
EOF
```

## Testing Checklist

### ✅ Firmware Validation
- [ ] Device detected by `rnodeconf --info`
- [ ] All radio parameters report correctly
- [ ] EEPROM checksum: VALID
- [ ] Firmware signature: VALIDATED
- [ ] Device provisioned: YES
- [ ] No timeouts or errors

### ✅ TNC Mode
- [ ] Successfully switches to TNC mode with `--tnc`
- [ ] Device info shows TNC mode active
- [ ] Can set radio parameters after TNC switch

### ✅ WiFi Feature Stub
- [ ] `--config` doesn't hang or crash
- [ ] Shows graceful message about WiFi unavailability
- [ ] Other config options still display
- [ ] No error in validation

### ✅ Reticulum Integration
- [ ] RNS initializes without serial errors
- [ ] RNode interface appears in interface list
- [ ] No "interface offline" messages
- [ ] Can query interface parameters

### ✅ Application Testing
- [ ] meshchat launches without errors
- [ ] nomadnet launches without errors
- [ ] Can see node identity in application
- [ ] Network communication works

## Debugging Guide

### Issue: Device Not Detected

**Symptoms**: "No RNode found" or timeout after "Detecting..."

**Diagnosis**:
```bash
# Check USB connection
lsusb | grep -i serial

# Verify port exists
ls -l /dev/ttyUSB*

# Check device is readable
cat /dev/ttyUSB0 | head -c 100
```

**Solutions**:
1. Try different USB port or cable
2. Check FTDI/CH340 drivers are installed (platform-specific)
3. Verify baud rate: `rnodeconf /dev/ttyUSB0 -b 115200 --info`
4. Reset device: unplug, wait 5s, plug back in

### Issue: EEPROM Checksum Mismatch

**Symptoms**: "EEPROM checksum mismatch" error

**Diagnosis**:
```bash
# Download and inspect EEPROM
rnodeconf /dev/ttyUSB0 --eeprom-read

# Check provisioning status
rnodeconf /dev/ttyUSB0 --info
```

**Solutions**:
1. Device may have old/corrupt provisioning
2. Re-provision device: `rnodeconf /dev/ttyUSB0 --autoinstall`
3. Or manually: `rnodeconf /dev/ttyUSB0 --eeprom-wipe` then re-provision

### Issue: Firmware Signature Validation Failed

**Symptoms**: "WARNING! Device signature validation failed"

**Likely Causes**:
- Device was signed with different key
- Device is self-signed locally
- Firmware is custom/modified

**Solutions**:
1. Expected for development builds—can be ignored for testing
2. To trust locally: copy signing key to `~/.config/Reticulum/firmware/signing.key`
3. Use `--autoinstall` to re-provision with official firmware

### Issue: Reticulum Interface Won't Connect

**Symptoms**: "Interface offline" or no RNode in interface list

**Diagnosis**:
```bash
# Check config syntax
cat ~/.config/Reticulum/config | grep -A 5 "RNode"

# Test with verbose output
python3 << 'EOF'
import RNS
RNS.loglevel = RNS.LOG_DEBUG
reticulum = RNS.Reticulum()
print("Check output above for RNode initialization")
EOF
```

**Solutions**:
1. Verify port name matches device: `ls /dev/ttyUSB*`
2. Verify TNC mode is active: `rnodeconf /dev/ttyUSB0 --info`
3. Check config file syntax (YAML indentation)
4. Try default config: `rnodeconf /dev/ttyUSB0 --normal` then back to `--tnc`

### Issue: RNS Initialization Hangs

**Symptoms**: Process stuck after "Initializing Reticulum..."

**Diagnosis**:
```bash
# Run with timeout
timeout 10 python3 -c "import RNS; RNS.Reticulum()" || echo "Timeout/Error"

# Check RNode is responding
rnodeconf /dev/ttyUSB0 --info
```

**Solutions**:
1. Device may be unresponsive—try reset
2. Serial port may be locked by another process: `lsof | grep ttyUSB0`
3. Kill conflicting process: `pkill rnodeconf` or `pkill -f RNS`

### Issue: New Statistics Not Received

**Symptoms**: `r_stat_chtm`, `r_stat_bat`, etc. are None

**Diagnosis**:
```bash
# Check device sends stats
rnodeconf /dev/ttyUSB0 --info -v | grep -i "stat"

# Inspect readLoop processing
python3 << 'EOF'
import serial
import time
port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
# Any output indicates device is responding
print("Raw device output (first 100 bytes):")
time.sleep(0.5)
data = port.read(100)
print(repr(data))
port.close()
EOF
```

**Solutions**:
1. New stats are optional—not required for basic operation
2. Verify firmware includes stats commands: check `Framing.h`
3. Stats may only transmit on request (check firmware code)

## Advanced Testing

### Serial Protocol Analysis
```bash
# Capture serial communication with timeout
timeout 10 rnodeconf /dev/ttyUSB0 --info 2>&1 | tee capture.log

# Analyze with Python
python3 << 'EOF'
with open('capture.log', 'r') as f:
    for line in f:
        if 'reporting' in line.lower():
            print(line.strip())
EOF
```

### Stress Testing
```bash
# Repeat configuration queries
for i in {1..100}; do
    echo "Iteration $i..."
    rnodeconf /dev/ttyUSB0 --info > /dev/null
    [ $? -ne 0 ] && echo "FAILED at iteration $i" && break
done
echo "Completed all iterations"
```

### Performance Testing
```bash
# Time device communication
time rnodeconf /dev/ttyUSB0 --info

# Expected: ~3-5 seconds for full device probe
```

## Known Test Scenarios

### Scenario A: Fresh Flash
1. Flash firmware to clean device
2. Expect: All validations pass immediately
3. Verify: Proceed to meshchat test

### Scenario B: Existing Device with Old Firmware
1. Flash new refactored firmware
2. Expect: May see signature mismatch (old provisioning)
3. Option 1: Ignore and continue testing
4. Option 2: Re-provision with `--autoinstall`

### Scenario C: WiFi Not Restored
1. Run `rnodeconf --config`
2. Expect: "Could not read WiFi configuration" message
3. Verify: Other config displays correctly
4. Verify: Validation continues without error

## Cleanup Between Tests

```bash
# Kill any hanging processes
pkill -f rnodeconf
pkill -f meshchat
pkill -f nomadnet
pkill -f RNS

# Reset device
# (unplug/replug USB)

# Clear any stale logs
rm -f ~/.local/share/Reticulum/*.log

# Fresh start
rnodeconf /dev/ttyUSB0 --info
```

## Session Recovery

After testing, to return to development session:

```bash
# Commit any test results/findings
git status
git add .
git commit -m "Test results: [what you tested]"

# Document issues found
git log -1  # Show latest commit

# Ready for next session
echo "Session ready for review - all changes committed"
```

## Logging and Troubleshooting Resources

- **rnodeconf verbose logs**: `rnodeconf -v` flag
- **Reticulum logs**: `~/.local/share/Reticulum/`
- **Serial port issues**: `dmesg | tail -20`
- **USB device issues**: `lsusb -vv`

## Next Steps After Successful Testing

1. ✅ Validation passed → Ready for application deployment
2. ✅ All tests passed → Ready for WiFi backport
3. ✅ Issues found → Document in issue tracker
4. ✅ New features working → Update feature status in integration docs
