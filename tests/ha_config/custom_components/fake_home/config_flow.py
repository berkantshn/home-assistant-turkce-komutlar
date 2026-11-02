"""Made By FALCREB. Sahte entegrasyonun tek adımlı kurulum akışı."""
from homeassistant import config_entries


class FakeHomeFlow(config_entries.ConfigFlow, domain="fake_home"):
    """Soru sormadan tek bir kayıt oluşturur."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id("fake_home")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title="Sahte Ev", data={})
