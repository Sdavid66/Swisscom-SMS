"""Flux de configuration UI pour Swisscom SMS."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CONF_CLIENT_ID, CONF_NAME, DEFAULT_NAME, DOMAIN


class SwisscomSmsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Gere l'ajout et la reconfiguration d'un compte Swisscom SMS."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Etape initiale : saisie du client_id."""
        errors: dict[str, str] = {}

        if user_input is not None:
            client_id = user_input[CONF_CLIENT_ID].strip()
            name = (user_input.get(CONF_NAME) or DEFAULT_NAME).strip() or DEFAULT_NAME

            if not client_id:
                errors["base"] = "invalid_client_id"
            else:
                await self.async_set_unique_id(client_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=name,
                    data={CONF_CLIENT_ID: client_id, CONF_NAME: name},
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): str,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    async def async_step_reconfigure(self, user_input=None) -> ConfigFlowResult:
        """Permet de mettre a jour le client_id d'une entree existante."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            client_id = user_input[CONF_CLIENT_ID].strip()
            if not client_id:
                errors["base"] = "invalid_client_id"
            else:
                return self.async_update_reload_and_abort(
                    entry,
                    unique_id=client_id,
                    data={**entry.data, CONF_CLIENT_ID: client_id},
                )

        schema = vol.Schema({vol.Required(CONF_CLIENT_ID): str})
        return self.async_show_form(
            step_id="reconfigure", data_schema=schema, errors=errors
        )
