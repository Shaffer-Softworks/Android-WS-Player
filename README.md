# Android WS Player

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Validate](https://github.com/Shaffer-Softworks/Android-WS-Player/actions/workflows/validate.yaml/badge.svg)](https://github.com/Shaffer-Softworks/Android-WS-Player/actions/workflows/validate.yaml)

Home Assistant custom integration that exposes each Android tablet as a **media player** entity. Play, stop, and volume commands are delivered to your tablet app as Home Assistant bus events.

## Features

- One media player entity per tablet
- Configurable `device_id` and event type per device
- Rename devices from the integration options (gear icon)
- `play_media`, `stop`, and `volume_set` support

## Installation

### HACS (recommended)

1. Install [HACS](https://hacs.xyz/docs/setup/download) if you have not already.
2. Open **HACS → Integrations → ⋮ → Custom repositories**.
3. Add `https://github.com/Shaffer-Softworks/Android-WS-Player` as category **Integration**, then search for **Android WS Player** and install.
4. Restart Home Assistant.
5. Go to **Settings → Devices & services → Add integration** and choose **Android WS Player**.

If this repository is listed in the [HACS default store](https://github.com/hacs/default), you can install it directly without adding a custom repository.

### Manual

1. Copy `custom_components/android_ws_player` into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & services**.

## Configuration

During setup you provide:

| Field | Description |
| --- | --- |
| **Name** | Friendly name shown in Home Assistant (e.g. `Kitchen Tablet`) |
| **Device ID** | Identifier your Android app listens for (e.g. `kitchen_tablet`) |
| **Event type** | HA event name fired for commands (default: `android_ws_player_command`) |

Use the integration **gear icon** to change the name or event type later.

## Android app

Your tablet app should subscribe to the configured event type on the Home Assistant WebSocket API. Each event payload includes:

| Field | Description |
| --- | --- |
| `device_id` | Matches the ID configured in Home Assistant |
| `command` | `play_media`, `stop`, or `set_volume` |
| `url` | Media URL (for `play_media`) |
| `volume` | Level 0.0–1.0 (for `set_volume`) |

Example `play_media` event:

```json
{
  "device_id": "kitchen_tablet",
  "command": "play_media",
  "url": "https://example.com/stream.mp3",
  "media_type": "music"
}
```

## Development

Validation runs on every push via GitHub Actions (`hassfest` + HACS). Brand images are bundled under `custom_components/android_ws_player/brand/` for Home Assistant 2026.3+.

## Support

- [Open an issue](https://github.com/Shaffer-Softworks/Android-WS-Player/issues)

## License

MIT — see [LICENSE](LICENSE).
