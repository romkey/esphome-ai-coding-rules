# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-11

### Added

- RULES.md: AI conduct, layout, YAML, examples, Home Assistant conventions,
  custom components, Docker, git and pre-commit, GitHub workflows, releases,
  documentation, license.
- Buildable template project with ESP32, ESP32-C3 and ESP32-S3 examples,
  example sensor and UI packages, and shared base config with encrypted
  API/OTA, fallback hotspot and safe mode.
- compose.yaml with validate, build, lint and dashboard services, using the
  ESPHome image's /cache and /build volumes for incremental builds.
- CI with uv, ccache, toolchain and build caches, weekly ESPHome beta build,
  and unit tests; lint via pre-commit; release workflow driven by
  CHANGELOG.md.
- Optional firmware publishing kit: release images and an ESP Web Tools
  installer on GitHub Pages, from secret-free firmware configs.
- Renovate config that also updates `github://` package tags.
- Claude Code plugin `esphome-rules` with `new`, `check`, `release` and
  `rules` skills, and its marketplace.
- Release strategy, Claude Code, configuration and overview docs.
