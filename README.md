<img src="https://raw.githubusercontent.com/Sdavid66/Swisscom-SMS/main/custom_components/swisscom_sms/brand/icon.png" alt="Swisscom SMS" width="96" align="right">

# Swisscom SMS for Home Assistant

[![Release](https://img.shields.io/github/v/release/Sdavid66/Swisscom-SMS)](https://github.com/Sdavid66/Swisscom-SMS/releases)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-support%20the%20project-orange?logo=buy-me-a-coffee&logoColor=white)](https://buymeacoffee.com/sdavid66)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz)
[![License](https://img.shields.io/github/license/Sdavid66/Swisscom-SMS)](LICENSE)

**Français : [README.fr.md](README.fr.md)**

Send SMS from Home Assistant through the **Swisscom Messaging API**. You provide
your Swisscom `client_id`, and a `notify` service appears in Home Assistant,
ready to use in automations, scripts and scenes.

## Requirements

- A subscription to the **Swisscom Messaging API** (SMS product) on the
  [Swisscom developer portal](https://sms.icp.swisscom.com/home), which gives
  you a **`client_id`**.
- Home Assistant **2026.3.0** or newer, required for the brand icons shipped
  inside the integration.

## Installation

### Through HACS

[![Open your Home Assistant instance and open this repository inside HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Sdavid66&repository=Swisscom-SMS&category=integration)

Until this repository is part of the HACS default store, add it manually:

1. HACS → menu ⋮ → **Custom repositories**.
2. Add `https://github.com/Sdavid66/Swisscom-SMS`, category
   *Integration*.
3. Install **Swisscom SMS**, then restart Home Assistant.

### Manually

Copy `custom_components/swisscom_sms` into the `custom_components` folder of
your Home Assistant configuration, then restart.

## Configuration

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=swisscom_sms)

1. **Settings → Devices & services → Add integration**.
2. Search for **Swisscom SMS**.
3. Enter your Swisscom `client_id` and, optionally, the name of the notify
   service (`Swisscom SMS` by default).

A `notify.swisscom_sms` service is created, named after your choice. Adding a
second entry with another `client_id` creates a second service.

To change the `client_id` later: integration → **Reconfigure**.

## Usage

The service sends one SMS per number listed in `target`. A valid number starts
with `0`, `00` or `+` and contains 7 to 15 digits — local numbers starting with
`0` are prefixed with `+41` by Swisscom.

```yaml
action: notify.swisscom_sms
data:
  message: "The garage door was left open."
  target:
    - "+41791234567"
```

Several recipients:

```yaml
action: notify.swisscom_sms
data:
  message: "Alarm triggered at home!"
  target:
    - "+41791234567"
    - "+41789876543"
```

In an automation:

```yaml
automation:
  - alias: "Water leak alert"
    triggers:
      - trigger: state
        entity_id: binary_sensor.kitchen_leak_detector
        to: "on"
    actions:
      - action: notify.swisscom_sms
        data:
          message: "Water leak detected in the kitchen!"
          target:
            - "+41791234567"
```

## Troubleshooting

Send failures are written to the Home Assistant **logs**
(*Settings → System → Logs*) together with the HTTP status returned by
Swisscom:

| Status | Meaning |
|---|---|
| `400` | Invalid phone number |
| `401` | Missing or incorrect `client_id` |
| `429` | Sending quota exhausted |

The startup warning `We found a custom integration swisscom_sms which has not
been tested by Home Assistant` is **normal** for every custom integration and
can be ignored.

## Known limitations

- **One way only.** The integration sends SMS; it does not receive them and
  reports no delivery receipt.
- **A failure does not stop an automation.** A rejected message is logged as an
  error, but the service call itself succeeds.
- **Legacy notify service.** The integration exposes a `notify.<name>` service
  supporting `target`, not a notify *entity*.
- **The icon only appears once installed.** The HACS dashboard reads its
  thumbnails from `data-v2.hacs.xyz`, which ignores icons shipped inside an
  integration ([hacs/integration#5171](https://github.com/hacs/integration/issues/5171)).

## Disclaimer

This is an independent community project. It is not affiliated with, endorsed
by, or supported by Swisscom. *Swisscom* and the Swisscom logo are trademarks of
Swisscom AG.

## License

[MIT](LICENSE)
