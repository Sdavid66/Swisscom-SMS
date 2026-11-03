"""Plateforme notify pour l'envoi de SMS via Swisscom."""
from __future__ import annotations

import logging

from homeassistant.components.notify import ATTR_TARGET, BaseNotificationService
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
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
        """Envoie `message` a chaque numero de `target`.

        Tous les numeros sont tentes : un numero refuse n'empeche pas l'envoi
        aux suivants. Les echecs sont ensuite remontes a l'appelant en une
        seule erreur, pour que l'automatisation et sa trace les signalent.
        """
        targets = kwargs.get(ATTR_TARGET)
        if not targets:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="no_target",
            )

        if isinstance(targets, str):
            targets = [targets]

        failures: list[str] = []
        for number in targets:
            try:
                await self._client.async_send(number, message)
                _LOGGER.debug("SMS envoye a %s", number)
            except SwisscomSmsError as err:
                _LOGGER.debug("Echec de l'envoi du SMS : %s", err)
                reason = f"HTTP {err.status}" if err.status else "no response"
                failures.append(f"{number} ({reason})")

        if failures:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="send_failed",
                translation_placeholders={
                    "failed": str(len(failures)),
                    "total": str(len(targets)),
                    "details": ", ".join(failures),
                },
            )
