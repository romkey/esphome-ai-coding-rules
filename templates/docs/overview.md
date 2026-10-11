# PROJECT overview

<!-- Short, factual, for AIs and humans. Keep under ~60 lines. -->

**What:** one sentence.
**Kind:** library | app.
**Hardware:** board(s), sensors, I2C addresses.

## Files

- `packages/NAME.yaml`: one line.
- `examples/esp32*.yaml`: ESP32, C3, S3 examples; all board/pin choices.
- `examples/common/base.yaml`: shared project, network and recovery config.

## Required by packages

- Substitutions: `status_led_pin`.
- Buses/ids: e.g. `i2c` with `id: i2c0`.

## Conventions

- Substitutions prefixed with package name; all have defaults unless listed
  above.
- Rules: https://github.com/romkey/esphome-ai-coding-rules/blob/main/RULES.md
