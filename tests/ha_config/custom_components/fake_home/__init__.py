"""Made By FALCREB. Test için sahte ev: gerçek cihazla konuşmaz, durumu bellekte tutar."""
from homeassistant.components.intent import async_register_timer_handler
from homeassistant.helpers import device_registry as dr

from .fake import DOMAINS, REGISTRY

DOMAIN = "fake_home"


async def async_setup(hass, config):
    """Testin durum hazırlaması için fake_home.set servisini kaydeder."""

    async def set_state(call):
        # Bir sahte varlığın durumunu ve özniteliklerini doğrudan ayarlar.
        entity = REGISTRY[call.data["entity_id"]]
        entity.apply_fake(call.data.get("state"), call.data.get("attrs") or {})

    hass.services.async_register(DOMAIN, "set", set_state)
    return True


async def async_setup_entry(hass, entry):
    """Sahte uydu cihazını ve tüm platformları yükler."""
    device = dr.async_get(hass).async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, "uydu")},
        name="Test Uydusu",
    )
    # Zamanlayıcı niyetleri, zamanlayıcı destekleyen bir cihaz ister.
    async_register_timer_handler(hass, device.id, lambda event, timer: None)
    await hass.config_entries.async_forward_entry_setups(entry, DOMAINS)
    return True
