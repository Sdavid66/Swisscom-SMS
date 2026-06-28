"""Integration Swisscom SMS pour Home Assistant.

Expose un service `notify.<nom>` (par defaut `notify.swisscom_sms`) qui envoie
un SMS via l'API Swisscom Messaging aux numeros passes dans `target`.
"""
from __future__ import annotations

import logging

from homeassistant.components.notify import DOMAIN as NOTIFY_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import slugify

from .api import SwisscomSmsClient
from .const import CONF_CLIENT_ID, CONF_NAME, DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure une entree (un client_id Swisscom)."""
    session = async_get_clientsession(hass)
    client = SwisscomSmsClient(session, entry.data[CONF_CLIENT_ID])

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    name = entry.data.get(CONF_NAME) or entry.title or DEFAULT_NAME

    # Chargement de la plateforme notify (service legacy supportant `target`).
    hass.async_create_task(
        discovery.async_load_platform(
            hass,
            Platform.NOTIFY,
            DOMAIN,
            {CONF_NAME: name, "entry_id": entry.entry_id},
            {},
        )
    )

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Recharge l'entree apres une reconfiguration."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Decharge l'entree et retire le service notify associe."""
    name = entry.data.get(CONF_NAME) or entry.title or DEFAULT_NAME
    hass.services.async_remove(NOTIFY_DOMAIN, slugify(name))
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return True
