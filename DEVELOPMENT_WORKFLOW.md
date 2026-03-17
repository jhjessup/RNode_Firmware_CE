# RNode Firmware CE - Development Workflow Guide

## Overview

This guide helps you work with the refactored firmware and rnodeconf, from initial setup through testing to debugging and iteration.

## Repository Structure

You'll be working with **two synchronized repositories**:

1. **RNode_Firmware_CE** - Firmware implementation
2. **Reticulum** - Control utilities (rnodeconf)

Both are on branch: `claude/review-repo-updates-8VfF2`

## Quick Clone & Setup

```bash
# Clone both repos
git clone https://github.com/jhjessup/RNode_Firmware_CE.git
cd RNode_Firmware_CE
git checkout claude/review-repo-updates-8VfF2

cd ..
git clone https://github.com/markqvist/Reticulum.git
cd Reticulum
git checkout claude/review-repo-updates-8VfF2
pip install -e .

# Verify rnodeconf is available
which rnodeconf
```

## Documentation Map

Each repo now includes comprehensive documentation:

### RNode Firmware CE

| File | Purpose | Use When |
|------|---------|----------|
| **FIRMWARE_INTEGRATION_STATUS.md** | Overview of refactoring, what changed, integration status | Starting work, understanding scope |
| **TESTING_AND_VALIDATION.md** | Step-by-step testing procedures | After building firmware, before testing |
| **DEVELOPMENT_WORKFLOW.md** | This file - how to work with both repos | Setting up development environment |

### Reticulum

| File | Purpose | Use When |
|------|---------|----------|
| **RNODECONF_INTEGRATION_STATUS.md** | rnodeconf changes, command reference, integration details | Understanding what changed in control tool |
| **RNODECONF_TESTING_GUIDE.md** | Testing rnodeconf specifically | Testing device communication |

## Standard Workflow

### Day 1: Initial Setup
```bash
# Clone repos
mkdir rnode-dev && cd rnode-dev
git clone https://github.com/jhjessup/RNode_Firmware_CE.git
git clone https://github.com/markqvist/Reticulum.git

# Checkout branches
cd RNode_Firmware_CE && git checkout claude/review-repo-updates-8VfF2
cd ../Reticulum && git checkout claude/review-repo-updates-8VfF2 && pip install -e .

# Read integration docs
cat RNode_Firmware_CE/FIRMWARE_INTEGRATION_STATUS.md
cat Reticulum/RNODECONF_INTEGRATION_STATUS.md
```

### Day 2: Build & Test
```bash
# Build firmware (following platform-specific README instructions)
cd RNode_Firmware_CE
# [Follow build steps in README.md for your platform]
# [Flash to device]

# Test with rnodeconf
rnodeconf /dev/ttyUSB0 --info
rnodeconf /dev/ttyUSB0 --config

# Proceed to full testing
# See: TESTING_AND_VALIDATION.md
```

### Day 3+: Iterate & Debug
```bash
# Return to development session
cd rnode-dev/RNode_Firmware_CE

# Check current status
git status
git log -1

# Read relevant docs
cat FIRMWARE_INTEGRATION_STATUS.md    # Understand what to work on
cat TESTING_AND_VALIDATION.md         # How to validate changes

# Make changes, test, commit
git add .
git commit -m "Description of changes"
git push -u origin claude/review-repo-updates-8VfF2
```

## Testing Workflow

### Quick Validation (5 minutes)
```bash
rnodeconf /dev/ttyUSB0 --info        # Device detection
rnodeconf /dev/ttyUSB0 --config      # Configuration display
```

### Full Testing (15-20 minutes)
Follow the "Quick Start" section in **TESTING_AND_VALIDATION.md**:
1. Firmware validation
2. TNC mode setup
3. Reticulum integration
4. Application testing

### Comprehensive Testing (1 hour+)
Follow the complete checklist in **TESTING_AND_VALIDATION.md**:
1. All device detection tests
2. EEPROM validation
3. Configuration modification
4. Statistics reception
5. Error code handling
6. WiFi stub verification
7. Full application integration

## WiFi Feature Restoration Workflow

When you're ready to backport WiFi support:

1. **Review the stub**: See RNODECONF_INTEGRATION_STATUS.md, "WiFi Feature Stub"
2. **Understand current state**: `rnodeconf --config` shows graceful handling
3. **Restore to firmware**: Implement WiFi commands in firmware
4. **No rnodeconf changes needed**: Existing try/except automatically handles it
5. **Test**: Run same rnodeconf commands, WiFi will now work
6. **Verify**: `rnodeconf --config` should show WiFi settings

## Debugging Session Recovery

When returning to work after a break:

```bash
# Navigate to project
cd rnode-dev

# Check both repos status
git -C RNode_Firmware_CE status
git -C Reticulum status

# Read relevant docs
cat RNode_Firmware_CE/FIRMWARE_INTEGRATION_STATUS.md    # What changed
cat Reticulum/RNODECONF_INTEGRATION_STATUS.md           # How it integrates

# Quick validation
rnodeconf /dev/ttyUSB0 --info

# See what was being worked on
git -C RNode_Firmware_CE log -1
git -C Reticulum log -1

# Continue where you left off
# (See TESTING_AND_VALIDATION.md or RNODECONF_TESTING_GUIDE.md for procedures)
```

## Development Task Checklist

### ✅ Setup Phase
- [ ] Both repos cloned
- [ ] Correct branches checked out
- [ ] Reticulum installed (`pip install -e .`)
- [ ] rnodeconf available in PATH

### ✅ Build Phase
- [ ] Firmware built successfully
- [ ] Flashed to device
- [ ] Device detected by system

### ✅ Validation Phase
- [ ] Device detection works (`--info`)
- [ ] Configuration reads correctly (`--config`)
- [ ] EEPROM validates
- [ ] Firmware signature validates
- [ ] No serial errors

### ✅ Integration Phase
- [ ] TNC mode enables
- [ ] Reticulum initializes
- [ ] RNode interface appears
- [ ] meshchat/nomadnet connect

### ✅ WiFi Backport Phase (When Starting)
- [ ] Review WiFi stub in docs
- [ ] Understand graceful handling
- [ ] Implement WiFi in firmware
- [ ] Test with rnodeconf
- [ ] Verify no rnodeconf changes needed

## Documentation Quick Reference

### For Understanding Changes
```
Read: FIRMWARE_INTEGRATION_STATUS.md
Then: RNODECONF_INTEGRATION_STATUS.md
```

### For Testing
```
Read: TESTING_AND_VALIDATION.md (Firmware side)
Then: RNODECONF_TESTING_GUIDE.md (Control tool side)
```

### For Debugging Specific Issues

| Issue | Documentation |
|-------|---|
| Device not detected | TESTING_AND_VALIDATION.md → "Debugging Guide" |
| EEPROM errors | RNODECONF_TESTING_GUIDE.md → "Procedure 2" |
| WiFi config unavailable | RNODECONF_TESTING_GUIDE.md → "Phase 5" |
| New stats not received | RNODECONF_TESTING_GUIDE.md → "Phase 3" |
| Reticulum integration fails | TESTING_AND_VALIDATION.md → "Phase 3" |

## File Organization

```
rnode-dev/
├── RNode_Firmware_CE/
│   ├── FIRMWARE_INTEGRATION_STATUS.md          (read first)
│   ├── TESTING_AND_VALIDATION.md               (use for testing)
│   ├── DEVELOPMENT_WORKFLOW.md                 (this file)
│   ├── TESTING_AND_VALIDATION.md
│   ├── Framing.h                               (command definitions)
│   ├── RNode_Firmware_CE.ino                   (main firmware)
│   └── ... (other firmware files)
│
└── Reticulum/
    ├── RNODECONF_INTEGRATION_STATUS.md         (read second)
    ├── RNODECONF_TESTING_GUIDE.md              (use for testing)
    ├── RNS/Utilities/rnodeconf.py              (the tool)
    └── ... (other reticulum files)
```

## Commit Message Convention

When working on this project, use commit messages that reference the integration status:

```bash
git commit -m "Brief description of change

More detailed explanation if needed.

Integration: [Firmware/rnodeconf/Both]
Status: [Integration Phase/WiFi Backport/Other]
Testing: [What was tested]

https://claude.ai/code/session_01SPDW5ZMHSHRKHtacW8jNtJ"
```

Example:
```bash
git commit -m "Add channel time statistics reception

Implements readLoop handler for CMD_STAT_CHTM (0x25) and stores
channel time in r_stat_chtm field.

Integration: rnodeconf
Status: New Statistics Reception
Testing: Verified parsing of 4-byte channel time value"
```

## Switching Between Sessions

### Save Before Closing
```bash
git -C RNode_Firmware_CE status
git -C Reticulum status

# Commit any work
git -C RNode_Firmware_CE add .
git -C RNode_Firmware_CE commit -m "Session work: [what you did]"

git -C Reticulum add .
git -C Reticulum commit -m "Session work: [what you did]"

# Push
git -C RNode_Firmware_CE push
git -C Reticulum push
```

### Resume Session
```bash
cd rnode-dev

# See what's been done
git -C RNode_Firmware_CE log -5 --oneline
git -C Reticulum log -5 --oneline

# Read relevant integration docs to refresh
cat RNode_Firmware_CE/FIRMWARE_INTEGRATION_STATUS.md
cat Reticulum/RNODECONF_INTEGRATION_STATUS.md

# Quick validation
rnodeconf /dev/ttyUSB0 --info

# Continue work
# (Refer to appropriate .md file for next steps)
```

## Communication with AI Sessions

When you need help in a future session:

### Share Context
1. Share both integration status docs:
   ```
   RNode_Firmware_CE/FIRMWARE_INTEGRATION_STATUS.md
   Reticulum/RNODECONF_INTEGRATION_STATUS.md
   ```

2. Share your current commit:
   ```bash
   git -C RNode_Firmware_CE log -1
   git -C Reticulum log -1
   ```

3. Share your issue or blockers:
   ```bash
   git -C RNode_Firmware_CE status
   rnodeconf /dev/ttyUSB0 --info
   # Error output if applicable
   ```

### Quick Debugging Command
```bash
# Captures full context for debugging
cat > debug_context.txt << 'EOF'
=== RNode Firmware CE ===
EOF
git -C RNode_Firmware_CE log -1 >> debug_context.txt
git -C RNode_Firmware_CE status >> debug_context.txt
echo "" >> debug_context.txt

echo "=== Reticulum ===" >> debug_context.txt
git -C Reticulum log -1 >> debug_context.txt
git -C Reticulum status >> debug_context.txt
echo "" >> debug_context.txt

echo "=== Device Info ===" >> debug_context.txt
rnodeconf /dev/ttyUSB0 --info >> debug_context.txt 2>&1

cat debug_context.txt
```

## Key Integration Points

### Command Protocol
- **Definition**: Firmware `Framing.h` ↔ rnodeconf `KISS class`
- **Processing**: Firmware command handling ↔ rnodeconf `readLoop()`
- **Status**: In sync on current branch

### EEPROM & Validation
- **Firmware**: EEPROM storage and checksums
- **rnodeconf**: EEPROM reading and validation
- **Status**: Fully functional

### WiFi Feature
- **Firmware**: Currently removed (pending restoration)
- **rnodeconf**: Gracefully stubbed with try/except
- **Status**: Ready for restoration (no rnodeconf changes needed)

### Statistics
- **Firmware**: Sends stats via new commands
- **rnodeconf**: Receives and stores stats
- **Status**: Handlers in place, display UI pending

## Next Steps Tracking

Create a `SESSION_NOTES.md` in your local repo root:

```markdown
# Session Notes

## Latest Session
- **Date**: [When you worked]
- **What Done**: [What was accomplished]
- **Current Status**: [Where things stand]
- **Next Steps**: [What to do next]
- **Blockers**: [Any issues blocking progress]

## For Next Session
[Anything you should remember]

## Commit References
[Last commits on both repos]
```

This helps you remember context between sessions.

## Success Indicators

When everything is working:

✅ Device detects immediately
✅ EEPROM validates
✅ Signature validates
✅ TNC mode switches smoothly
✅ Reticulum initializes
✅ RNode interface appears
✅ Application (meshchat/nomadnet) connects
✅ No errors in logs

## Need Help?

1. **Check the docs first**: See Documentation Quick Reference above
2. **Follow test procedures**: Run appropriate phase from TESTING_AND_VALIDATION.md
3. **Capture context**: Run debug_context.txt command above
4. **Share with AI session**: Provide the debug context and current status

Your session can then quickly understand:
- What's been done
- Current state
- What's being worked on
- What the blocker is
- How to fix it

Good luck with development! 🚀
