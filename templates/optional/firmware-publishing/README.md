# Optional: publish installable firmware

For **applications** (a device people flash as-is), not libraries of
packages. Adds prebuilt firmware to each GitHub Release and a web installer
on GitHub Pages, so people can flash from a browser without ESPHome.

## Add it to a project

1. Copy `firmware/` and `web/` from here to the repo root.
2. Make one `firmware/<board>.yaml` per supported board. Replace `REPO`.
3. Enable Pages with GitHub Actions as the source:
   `gh api -X POST repos/romkey/REPO/pages -f build_type=workflow`
4. Add the installer link and a "Flash from your browser" section to the README.

`.github/workflows/release.yaml` notices `firmware/` and builds, attaches and
publishes it on every tag. CI already builds `firmware/` on every push.

## Why separate configs instead of the examples

Examples are built with CI's dummy secrets. Published images must contain no
secrets, so firmware configs:

- have no Wi-Fi credentials: after flashing, the web installer configures
  Wi-Fi over Improv, or the device opens a fallback hotspot;
- have no fixed API key: Home Assistant provisions one when the device is
  adopted (`dashboard_import`);
- add the MAC to the hostname so several devices can coexist.
