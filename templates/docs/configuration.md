# Configuration

<!-- One section per package or component. -->

## `packages/example.yaml`

Reports the chip's internal temperature.

**Requires:** nothing.

| Substitution | Default | Meaning |
|--------------|---------|---------|
| `example_name` | `Chip Temperature` | Entity name |
| `example_id` | `example_chip_temperature` | Sensor id; change if included twice |
| `example_update_interval` | `60s` | Sampling interval |
| `example_entity_category` | `diagnostic` | `""` to show on the main device card |

```yaml
packages:
  example: github://romkey/REPO/packages/example.yaml@v0.1.0
```

## `packages/status-led.yaml`

Blinks an LED on warnings and errors.

**Requires:** `status_led_pin`.

| Substitution | Default | Meaning |
|--------------|---------|---------|
| `status_led_pin` | (required) | GPIO the LED is on |
| `status_led_inverted` | `false` | `true` for an active-low LED |

```yaml
substitutions:
  status_led_pin: GPIO4

packages:
  status_led: github://romkey/REPO/packages/status-led.yaml@v0.1.0
```
