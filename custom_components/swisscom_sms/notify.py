"""Plateforme notify pour l'envoi de SMS via Swisscom."""
from __future__ import annotations

import logging

from homeassistant.components.notify import ATTR_TARGET, BaseNotificationService
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .api import SwisscomSmsClient, SwisscomSmsError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> SwisscomSmsNotificationService | None:
    """Renvoie le service notify (uniquement via une entree de configuration)."""
    if discovery_info is None:
        return None

    client: SwisscomSmsClient = hass.data[DOMAIN][discovery_info["entry_id"]]
    return SwisscomSmsNotificationService(client)


class SwisscomSmsNotificationService(BaseNotificationService):
    """Service notify qui envoie un SMS a chaque numero de `target`."""

    def __init__(self, client: SwisscomSmsClient) -> None:
        self._client = client

    async def async_send_message(self, message: str = "", **kwargs) -> None:
        """Envoie `message` aux numeros indiques dans `target`."""
        targets = kwargs.get(ATTR_TARGET)
        if not targets:
            _LOGGER.error(
                "Aucun destinataire : precisez `target` avec un ou plusieurs "
                "numeros de telephone (ex. +41791234567)"
            )
            return

        if isinstance(targets, str):
            targets = [targets]

        for number in targets:
            try:
                await self._client.async_send(number, message)
                _LOGGER.debug("SMS envoye a %s", number)
            except SwisscomSmsError as err:
                _LOGGER.error("Echec de l'envoi du SMS : %s", err)
