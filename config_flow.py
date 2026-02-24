from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_DEVICE_ID,
    CONF_EVENT_TYPE,
    DEFAULT_EVENT_TYPE,
)

class AndroidWsPlayerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            device_id = user_input[CONF_DEVICE_ID].strip()

            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured()  # avoid duplicates :contentReference[oaicite:5]{index=5}

            title = user_input["name"].strip()
            data = {
                CONF_DEVICE_ID: device_id,
                CONF_EVENT_TYPE: user_input.get(CONF_EVENT_TYPE, DEFAULT_EVENT_TYPE).strip(),
            }
            return self.async_create_entry(title=title, data=data)

        schema = vol.Schema(
            {
                vol.Required("name", default="Kitchen Tablet"): str,
                vol.Required(CONF_DEVICE_ID, default="kitchen_tablet"): str,
                vol.Optional(CONF_EVENT_TYPE, default=DEFAULT_EVENT_TYPE): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AndroidWsPlayerOptionsFlow(config_entry)

class AndroidWsPlayerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # Update entry title (friendly name shown in UI)
            new_title = user_input["name"].strip()
            if new_title and new_title != self.config_entry.title:
                self.hass.config_entries.async_update_entry(self.config_entry, title=new_title)

            # Store other tunables in options
            return self.async_create_entry(
                title="",
                data={
                    CONF_EVENT_TYPE: user_input.get(CONF_EVENT_TYPE, DEFAULT_EVENT_TYPE).strip(),
                },
            )

        schema = vol.Schema(
            {
                vol.Required("name", default=self.config_entry.title): str,
                vol.Optional(
                    CONF_EVENT_TYPE,
                    default=self.config_entry.options.get(
                        CONF_EVENT_TYPE, self.config_entry.data.get(CONF_EVENT_TYPE, DEFAULT_EVENT_TYPE)
                    ),
                ): str,
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
