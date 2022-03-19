"""Switch platform for integration_blueprint."""
import time
from homeassistant.components.switch import SwitchEntity

import logging
from .const import DEFAULT_NAME, DOMAIN, ICON, SWITCH, SWITCH_ICON
from .entity import PodPointEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    switches = []
    for i in range(len(coordinator.data)):
        switch = PodPointBinarySwitch(coordinator, entry, i)

        switches.append(switch)
    async_add_devices(switches)


class PodPointBinarySwitch(PodPointEntity, SwitchEntity):
    """pod_point switch class."""

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Allow charging (clear schedule)"""
        start_1 = time.time()
        await self.coordinator.api.async_set_schedule(False, self.pod)
        end_1 = time.time()
        start_2 = time.time()
        await self.coordinator.async_request_refresh()
        end_2 = time.time()
        _LOGGER.debug(
            "Turn on timings: total %ss set: %ss update: %ss",
            end_2 - start_1,
            end_1 - start_1,
            end_2 - start_2,
        )

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Block charging (turn on schedule)"""
        await self.coordinator.api.async_set_schedule(True, self.pod)
        await self.coordinator.async_request_refresh()

    @property
    def name(self):
        """Return the name of the switch."""
        return "Charging Allowed"

    @property
    def icon(self):
        """Return the icon of this switch."""
        return SWITCH_ICON

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.charging_allowed
