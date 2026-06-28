"""Client HTTP minimal pour l'API Swisscom Messaging (envoi de SMS)."""
from __future__ import annotations

import asyncio
import logging
import uuid

import aiohttp

from .const import API_URL, REQUEST_TIMEOUT, SCS_VERSION

_LOGGER = logging.getLogger(__name__)


class SwisscomSmsError(Exception):
    """Erreur renvoyee lors de l'envoi d'un SMS."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class SwisscomSmsClient:
    """Petit wrapper autour de l'endpoint POST /messaging/sms."""

    def __init__(self, session: aiohttp.ClientSession, client_id: str) -> None:
        self._session = session
        self._client_id = client_id

    def _headers(self) -> dict[str, str]:
        return {
            "SCS-Version": SCS_VERSION,
            "client_id": self._client_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "SCS-Request-ID": str(uuid.uuid4()),
        }

    async def async_send(self, to: str, text: str) -> None:
        """Envoie un SMS au numero `to`. Leve SwisscomSmsError en cas d'echec.

        Un numero valide commence par 0, 00 ou + et contient 7 a 15 chiffres
        (les numeros locaux en 0 sont prefixes +41 par defaut cote Swisscom).
        """
        number = to.replace(" ", "").strip()
        payload = {"to": number, "text": text}

        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                async with self._session.post(
                    API_URL, json=payload, headers=self._headers()
                ) as resp:
                    # L'API repond 201 sans corps en cas de succes.
                    if resp.status == 201:
                        _LOGGER.debug("SMS accepte pour %s", number)
                        return

                    body = await resp.text()
                    raise SwisscomSmsError(
                        f"L'API Swisscom a refuse l'envoi vers {number} "
                        f"(HTTP {resp.status}): {body or 'aucun detail'}",
                        status=resp.status,
                    )
        except TimeoutError as err:
            raise SwisscomSmsError(
                f"Delai depasse lors de l'envoi du SMS vers {number}"
            ) from err
        except aiohttp.ClientError as err:
            raise SwisscomSmsError(
                f"Erreur reseau lors de l'envoi du SMS vers {number}: {err}"
            ) from err
