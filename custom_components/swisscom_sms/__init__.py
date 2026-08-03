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
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import slugify

from .api import SwisscomSmsClient
from .const import CONF_CLIENT_ID, CONF_NAME, DATA_HASS_CONFIG, DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)

# L'integration se configure uniquement depuis l'interface : aucune cle YAML
# n'est acceptee sous `swisscom_sms:`.
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Memorise la configuration YAML globale.

    `discovery.async_load_platform` doit recevoir la configuration reelle de
    Home Assistant : lui passer un dictionnaire vide empecherait les
    plateformes `notify:` declarees en YAML d'etre configurees si cette
    integration charge le composant notify en premier.
    """
    hass.data[DATA_HASS_CONFIG] = config
    return True


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
            hass.data.get(DATA_HASS_CONFIG, {}),
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
