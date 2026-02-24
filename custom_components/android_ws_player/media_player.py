from __future__ import annotations

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import MediaPlayerEntityFeature, MediaType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_IDLE, STATE_PLAYING

from .const import DOMAIN, CONF_DEVICE_ID, CONF_EVENT_TYPE, DEFAULT_EVENT_TYPE

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities([AndroidWsPlayer(hass, entry)], update_before_add=True)

class AndroidWsPlayer(MediaPlayerEntity):
    _attr_supported_features = (
        MediaPlayerEntityFeature.PLAY_MEDIA
        | MediaPlayerEntityFeature.STOP
        | MediaPlayerEntityFeature.VOLUME_SET
    )
    _attr_media_content_type = MediaType.MUSIC

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry

        self._device_id = entry.data[CONF_DEVICE_ID]
        self._event_type = entry.options.get(CONF_EVENT_TYPE, entry.data.get(CONF_EVENT_TYPE, DEFAULT_EVENT_TYPE))

        self._attr_name = entry.title
        self._attr_unique_id = f"{self._device_id}"  # unique per integration domain
        self._attr_volume_level = 1.0
        self._is_playing = False

    @property
    def state(self):
        return STATE_PLAYING if self._is_playing else STATE_IDLE

    @property
    def extra_state_attributes(self):
        return {
            "device_id": self._device_id,
            "event_type": self._event_type,
        }

    async def async_play_media(self, media_type: str, media_id: str, **kwargs):
        self.hass.bus.async_fire(
            self._event_type,
            {
                "device_id": self._device_id,
                "command": "play_media",
                "url": media_id,
                "media_type": media_type,
                "extra": kwargs,
            },
        )
        self._is_playing = True
        self.async_write_ha_state()

    async def async_media_stop(self):
        self.hass.bus.async_fire(
            self._event_type,
            {"device_id": self._device_id, "command": "stop"},
        )
        self._is_playing = False
        self.async_write_ha_state()

    async def async_set_volume_level(self, volume: float):
        self._attr_volume_level = volume
        self.hass.bus.async_fire(
            self._event_type,
            {"device_id": self._device_id, "command": "set_volume", "volume": volume},
        )
        self.async_write_ha_state()
