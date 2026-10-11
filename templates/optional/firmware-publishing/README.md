# Optional: publish installable firmware

For **applications** (a device people flash as-is), not libraries of
packages. Adds prebuilt firmware to each GitHub Release and a web installer
on GitHub Pages, so people can flash from a browser without ESPHome.

## Add it to a project

1. Copy `firmware/` and `web/` from here to the repo root.
2. Make one `firmware/<board>.yaml` per supported board. Replace `REPO`.
3. Enable Pages with GitHub Actions as the source, and let release tags
   deploy to it (by default only `main` may):

   ```bash
   gh api -X POST repos/romkey/REPO/pages -f build_type=workflow
   ```

   ```bash
   gh api -X POST repos/romkey/REPO/environments/github-pages/deployment-branch-policies -f name='v*' -f type=tag
   ```
4. Add the installer link and a "Flash from your browser" section to the README.

`.github/workflows/release.yaml` notices `firmware/` and builds, attaches and
publishes it on every release. CI already builds `firmware/` on every push.

## Why separate configs instead of the examples

Examples are built with CI's dummy secrets. Published images must contain no
secrets and must work on anyone's network, so firmware configs:

- have no Wi-Fi credentials. After flashing, people set up their own Wi-Fi
  through any of:
  - the web installer, which asks for it over USB (Improv serial);
  - a phone over Bluetooth: the Home Assistant app finds the device, or
    https://www.improv-wifi.com in Chrome (Improv BLE);
  - the device's fallback hotspot and its captive portal;
- have no fixed API key: Home Assistant provisions one when the device is
  adopted (`dashboard_import`);
- open a 30-minute setup window at power-on (`provisioning:`). If Wi-Fi
  isn't set up and the device isn't adopted by then, setup closes until the
  device is unplugged and replugged, so an unconfigured device isn't left
  open to anyone nearby;
- add the MAC to the hostname so several devices can coexist.

ESPHome doesn't support ESP RainMaker; Improv is its equivalent.

Bluetooth setup adds about 350 KB of firmware. Drop `esp32_improv:` for
chips without Bluetooth (ESP32-S2) or if flash is tight. ESPHome 2026.10
renames it `improv_ble:`; the old name works until 2027.4.0.

Put the setup steps in the README's flashing section: flash from the web
installer, enter Wi-Fi when asked (or use the phone or hotspot), add the
device in Home Assistant, all within 30 minutes; otherwise unplug and
replug it and try again.
