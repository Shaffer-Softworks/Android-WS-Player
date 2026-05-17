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
            self._abort_if_unique_id_configured()

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
        return AndroidWsPlayerOptionsFlow()

class AndroidWsPlayerOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            device_id = user_input[CONF_DEVICE_ID].strip()
            new_title = user_input["name"].strip()

            if not device_id:
                errors["base"] = "invalid_device_id"
            else:
                for entry in self.hass.config_entries.async_entries(DOMAIN):
                    if (
                        entry.entry_id != self.config_entry.entry_id
                        and entry.unique_id == device_id
                    ):
                        errors[CONF_DEVICE_ID] = "already_configured"
                        break

            if not errors:
                data = dict(self.config_entry.data)
                data[CONF_DEVICE_ID] = device_id

                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    title=new_title or self.config_entry.title,
                    data=data,
                    unique_id=device_id,
                )

                return self.async_create_entry(
                    title="",
                    data={
                        CONF_EVENT_TYPE: user_input.get(
                            CONF_EVENT_TYPE, DEFAULT_EVENT_TYPE
                        ).strip(),
                    },
                )

        schema = vol.Schema(
            {
                vol.Required("name", default=self.config_entry.title): str,
                vol.Required(
                    CONF_DEVICE_ID, default=self.config_entry.data[CONF_DEVICE_ID]
                ): str,
                vol.Optional(
                    CONF_EVENT_TYPE,
                    default=self.config_entry.options.get(
                        CONF_EVENT_TYPE,
                        self.config_entry.data.get(CONF_EVENT_TYPE, DEFAULT_EVENT_TYPE),
                    ),
                ): str,
            }
        )

        return self.async_show_form(
            step_id="init", data_schema=schema, errors=errors
        )
