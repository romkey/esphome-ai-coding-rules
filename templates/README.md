# PROJECT

[![CI](https://github.com/romkey/REPO/actions/workflows/ci.yaml/badge.svg)](https://github.com/romkey/REPO/actions/workflows/ci.yaml)
[![Lint](https://github.com/romkey/REPO/actions/workflows/lint.yaml/badge.svg)](https://github.com/romkey/REPO/actions/workflows/lint.yaml)
[![ESPHome](https://img.shields.io/badge/ESPHome-packages-18BCF2?logo=esphome&logoColor=white)](https://esphome.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

One paragraph: what this is and why you'd want it.

> **AI disclosure:** This project was written by AI under human oversight,
> following [these rules](https://github.com/romkey/esphome-ai-coding-rules/blob/main/RULES.md).

## What's here

| Path | What it is |
|------|------------|
| `packages/NAME.yaml` | ... |
| `examples/esp32.yaml`, `esp32-c3.yaml`, `esp32-s3.yaml` | Example devices wiring the packages together |
| `docs/configuration.md` | Full configuration reference |

## Technical details

Hardware, wiring table, I2C addresses, datasheet links.

## Using the packages in your own config

```yaml
packages:
  NAME: github://romkey/REPO/packages/NAME.yaml@v0.1.0
```

See [docs/configuration.md](docs/configuration.md) for every option.

## Building

Requires Docker.

```bash
cp examples/secrets.yaml.example examples/secrets.yaml   # then edit it
docker compose run --rm validate
docker compose run --rm build
docker compose run --rm lint
```

The first build downloads the toolchains into a Docker volume; later builds
reuse them and only recompile what changed.

## Flashing

To flash a new board, build the firmware images:

```bash
docker compose run --rm firmware
```

Then open https://web.esphome.io in Chrome or Edge, connect the board over
USB and upload `dist/<name>.factory.bin`. After that, update over the
network (OTA). The images contain your Wi-Fi credentials; don't share them.

## License

[MIT](LICENSE), except the manufacturer datasheets in [datasheets/](datasheets/),
which belong to their manufacturers and are not covered by this license; see
each datasheet's `-license.txt`.
