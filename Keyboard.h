// Copyright (C) 2024, Mark Qvist

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#ifndef KEYBOARD_H
  #define KEYBOARD_H

  #include <Wire.h>

  // Poll the I2C keyboard every 50ms
  #define KEYBOARD_POLL_INTERVAL 50

  unsigned long last_keyboard_poll = 0;

  void keyboard_init() {
    Wire.begin(I2C_SDA, I2C_SCL);
  }

  void kiss_indicate_key(uint8_t key) {
    serial_write(FEND);
    serial_write(CMD_KEYBOARD);
    serial_write(KEYBOARD_CMD_KEY);
    escaped_serial_write(key);
    serial_write(FEND);
  }

  // Read any pending key presses from the I2C keyboard MCU and transmit
  // each one as a KISS frame over the serial link.
  void keyboard_read() {
    if (millis() - last_keyboard_poll >= KEYBOARD_POLL_INTERVAL) {
      last_keyboard_poll = millis();
      Wire.requestFrom((uint8_t)KEYBOARD_ADDR, (uint8_t)1);
      while (Wire.available()) {
        uint8_t key = Wire.read();
        if (key != 0x00) {
          kiss_indicate_key(key);
        }
      }
    }
  }

#endif
