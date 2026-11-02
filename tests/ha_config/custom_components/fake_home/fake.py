"""Made By FALCREB. Tüm sahte varlıklar: isimler genel ve kurmacadır."""
from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
)
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.components.cover import CoverEntity, CoverEntityFeature
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.components.lock import LockEntity
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.components.scene import Scene
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.vacuum import (
    StateVacuumEntity,
    VacuumActivity,
    VacuumEntityFeature,
)
from homeassistant.components.weather import WeatherEntity

DOMAINS = [
    "alarm_control_panel", "binary_sensor", "climate", "cover", "fan", "light",
    "lock", "media_player", "scene", "sensor", "switch", "vacuum", "weather",
]
REGISTRY = {}


class Fake:
    """Ortak davranış: durumu bellekte tutar, sahte servisle değiştirilebilir."""

    _attr_should_poll = False

    def setup_fake(self, domain, slug, name):
        self.entity_id = f"{domain}.{slug}"
        self._attr_unique_id = f"fake_{slug}"
        self._attr_name = name
        REGISTRY[self.entity_id] = self

    def apply_fake(self, state, attrs):
        if state is not None:
            self.fake_state(state)
        for key, value in attrs.items():
            setattr(self, f"_attr_{key}", value)
        self.async_write_ha_state()

    def fake_state(self, state):
        self._attr_is_on = state == "on"


class FakeLight(Fake, LightEntity):
    _attr_supported_color_modes = {ColorMode.RGB, ColorMode.COLOR_TEMP}
    _attr_color_mode = ColorMode.RGB
    _attr_min_color_temp_kelvin = 2000
    _attr_max_color_temp_kelvin = 6500

    def __init__(self, slug, name):
        self.setup_fake("light", slug, name)
        self._attr_is_on = False
        self._attr_brightness = 255
        self._attr_rgb_color = (255, 255, 255)

    async def async_turn_on(self, **kw):
        self._attr_is_on = True
        if ATTR_BRIGHTNESS in kw:
            self._attr_brightness = kw[ATTR_BRIGHTNESS]
        if ATTR_RGB_COLOR in kw:
            self._attr_color_mode = ColorMode.RGB
            self._attr_rgb_color = kw[ATTR_RGB_COLOR]
        if ATTR_COLOR_TEMP_KELVIN in kw:
            self._attr_color_mode = ColorMode.COLOR_TEMP
            self._attr_color_temp_kelvin = kw[ATTR_COLOR_TEMP_KELVIN]
        self.async_write_ha_state()

    async def async_turn_off(self, **kw):
        self._attr_is_on = False
        self.async_write_ha_state()


class FakeSwitch(Fake, SwitchEntity):
    def __init__(self, slug, name):
        self.setup_fake("switch", slug, name)
        self._attr_is_on = False

    async def async_turn_on(self, **kw):
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kw):
        self._attr_is_on = False
        self.async_write_ha_state()


class FakeFan(Fake, FanEntity):
    _attr_supported_features = (
        FanEntityFeature.SET_SPEED | FanEntityFeature.TURN_ON | FanEntityFeature.TURN_OFF
    )

    def __init__(self, slug, name):
        self.setup_fake("fan", slug, name)
        self._attr_percentage = 0

    def fake_state(self, state):
        self._attr_percentage = 50 if state == "on" else 0

    @property
    def is_on(self):
        return bool(self._attr_percentage)

    async def async_turn_on(self, percentage=None, preset_mode=None, **kw):
        self._attr_percentage = percentage if percentage is not None else 50
        self.async_write_ha_state()

    async def async_turn_off(self, **kw):
        self._attr_percentage = 0
        self.async_write_ha_state()

    async def async_set_percentage(self, percentage):
        self._attr_percentage = percentage
        self.async_write_ha_state()


class FakeCover(Fake, CoverEntity):
    _attr_supported_features = (
        CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE
        | CoverEntityFeature.STOP | CoverEntityFeature.SET_POSITION
    )

    def __init__(self, slug, name, device_class):
        self.setup_fake("cover", slug, name)
        self._attr_device_class = device_class
        self._attr_current_cover_position = 0

    def fake_state(self, state):
        self._attr_current_cover_position = 100 if state == "open" else 0

    @property
    def is_closed(self):
        return self._attr_current_cover_position == 0

    async def async_open_cover(self, **kw):
        self._attr_current_cover_position = 100
        self.async_write_ha_state()

    async def async_close_cover(self, **kw):
        self._attr_current_cover_position = 0
        self.async_write_ha_state()

    async def async_set_cover_position(self, position, **kw):
        self._attr_current_cover_position = position
        self.async_write_ha_state()

    async def async_stop_cover(self, **kw):
        self.async_write_ha_state()


class FakeClimate(Fake, ClimateEntity):
    _attr_temperature_unit = "°C"
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF | ClimateEntityFeature.FAN_MODE
    )
    _attr_fan_modes = ["auto", "low", "medium", "high"]
    _attr_target_temperature_step = 0.5

    def __init__(self, slug, name, current):
        self.setup_fake("climate", slug, name)
        self._attr_current_temperature = current
        self._attr_target_temperature = 20
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_fan_mode = "auto"

    def fake_state(self, state):
        self._attr_hvac_mode = HVACMode(state)

    async def async_set_temperature(self, **kw):
        self._attr_target_temperature = kw["temperature"]
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode):
        self._attr_fan_mode = fan_mode
        self.async_write_ha_state()

    async def async_turn_on(self):
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self):
        await self.async_set_hvac_mode(HVACMode.OFF)


class FakeMedia(Fake, MediaPlayerEntity):
    _attr_supported_features = (
        MediaPlayerEntityFeature.PAUSE | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.NEXT_TRACK | MediaPlayerEntityFeature.PREVIOUS_TRACK
        | MediaPlayerEntityFeature.VOLUME_SET | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.VOLUME_STEP | MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
    )

    def __init__(self, slug, name):
        self.setup_fake("media_player", slug, name)
        self._attr_state = MediaPlayerState.PLAYING
        self._attr_volume_level = 0.5
        self._attr_is_volume_muted = False
        self._attr_media_title = "1"

    def fake_state(self, state):
        self._attr_state = MediaPlayerState(state)

    async def _set(self, **attrs):
        for key, value in attrs.items():
            setattr(self, f"_attr_{key}", value)
        self.async_write_ha_state()

    async def async_turn_on(self):
        await self._set(state=MediaPlayerState.PLAYING)

    async def async_turn_off(self):
        await self._set(state=MediaPlayerState.OFF)

    async def async_media_pause(self):
        await self._set(state=MediaPlayerState.PAUSED)

    async def async_media_play(self):
        await self._set(state=MediaPlayerState.PLAYING)

    async def async_media_next_track(self):
        await self._set(media_title="sonraki")

    async def async_media_previous_track(self):
        await self._set(media_title="onceki")

    async def async_set_volume_level(self, volume):
        await self._set(volume_level=volume)

    async def async_mute_volume(self, mute):
        await self._set(is_volume_muted=mute)


class FakeSensor(Fake, SensorEntity):
    def __init__(self, slug, name, device_class, unit, value):
        self.setup_fake("sensor", slug, name)
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_native_value = value

    def fake_state(self, state):
        self._attr_native_value = state


class FakeBinary(Fake, BinarySensorEntity):
    def __init__(self, slug, name, device_class):
        self.setup_fake("binary_sensor", slug, name)
        self._attr_device_class = device_class
        self._attr_is_on = False


class FakeLock(Fake, LockEntity):
    def __init__(self, slug, name):
        self.setup_fake("lock", slug, name)
        self._attr_is_locked = True

    def fake_state(self, state):
        self._attr_is_locked = state == "locked"

    async def async_lock(self, **kw):
        self._attr_is_locked = True
        self.async_write_ha_state()

    async def async_unlock(self, **kw):
        self._attr_is_locked = False
        self.async_write_ha_state()


class FakeAlarm(Fake, AlarmControlPanelEntity):
    _attr_supported_features = AlarmControlPanelEntityFeature.ARM_AWAY
    _attr_code_arm_required = False

    def __init__(self, slug, name):
        self.setup_fake("alarm_control_panel", slug, name)
        self._attr_alarm_state = AlarmControlPanelState.ARMED_AWAY

    def fake_state(self, state):
        self._attr_alarm_state = AlarmControlPanelState(state)

    async def async_alarm_disarm(self, code=None):
        self._attr_alarm_state = AlarmControlPanelState.DISARMED
        self.async_write_ha_state()

    async def async_alarm_arm_away(self, code=None):
        self._attr_alarm_state = AlarmControlPanelState.ARMED_AWAY
        self.async_write_ha_state()


class FakeVacuum(Fake, StateVacuumEntity):
    _attr_supported_features = (
        VacuumEntityFeature.START | VacuumEntityFeature.RETURN_HOME | VacuumEntityFeature.STATE
    )

    def __init__(self, slug, name):
        self.setup_fake("vacuum", slug, name)
        self._attr_activity = VacuumActivity.DOCKED

    def fake_state(self, state):
        self._attr_activity = VacuumActivity(state)

    async def async_start(self):
        self._attr_activity = VacuumActivity.CLEANING
        self.async_write_ha_state()

    async def async_return_to_base(self, **kw):
        self._attr_activity = VacuumActivity.RETURNING
        self.async_write_ha_state()


class FakeScene(Fake, Scene):
    def __init__(self, slug, name):
        self.setup_fake("scene", slug, name)

    async def async_activate(self, **kw):
        # Etkinleştirmeyi sahte lambanın açılmasıyla gözlemlenebilir yapar.
        await REGISTRY["light.abajur"].async_turn_on()


class FakeWeather(Fake, WeatherEntity):
    _attr_native_temperature_unit = "°C"

    def __init__(self, slug, name):
        self.setup_fake("weather", slug, name)
        self._attr_condition = "partlycloudy"
        self._attr_native_temperature = 18

    def fake_state(self, state):
        self._attr_condition = state


ENTITIES = {
    "light": lambda: [
        FakeLight("salon_lambasi", "Salon Lambası"),
        FakeLight("avize", "Avize"),
        FakeLight("mutfak_lambasi", "Mutfak Lambası"),
        FakeLight("abajur", "Abajur"),
        FakeLight("tavan_isigi", "Tavan Işığı"),
        FakeLight("ara_isigi", "Ara Işığı"),
        FakeLight("ikinci_lamba", "İkinci Lamba"),
    ],
    "switch": lambda: [
        FakeSwitch("kahve_makinesi", "Kahve Makinesi"),
        FakeSwitch("priz", "Priz"),
    ],
    "fan": lambda: [FakeFan("tavan_fani", "Tavan Fanı")],
    "cover": lambda: [
        FakeCover("salon_perdesi", "Salon Perdesi", "curtain"),
        FakeCover("panjur", "Panjur", "shutter"),
        FakeCover("garaj_kapisi", "Garaj Kapısı", "garage"),
    ],
    "climate": lambda: [FakeClimate("salon_klimasi", "Salon Kliması", 23)],
    "media_player": lambda: [
        FakeMedia("televizyon", "Televizyon"),
        FakeMedia("hoparlor", "Hoparlör"),
    ],
    "sensor": lambda: [
        FakeSensor("salon_sicaklik", "Salon Sıcaklık Sensörü", "temperature", "°C", 23.5),
        FakeSensor("salon_nem", "Salon Nem Sensörü", "humidity", "%", 45),
        FakeSensor("mutfak_nem", "Mutfak Nem Sensörü", "humidity", "%", 60),
    ],
    "binary_sensor": lambda: [
        FakeBinary("salon_penceresi", "Salon Penceresi", "window"),
        FakeBinary("mutfak_hareket", "Mutfak Hareket Sensörü", "motion"),
    ],
    "lock": lambda: [FakeLock("on_kapi", "Ön Kapı")],
    "alarm_control_panel": lambda: [FakeAlarm("ev_alarmi", "Ev Alarmı")],
    "vacuum": lambda: [FakeVacuum("robot_supurge", "Robot Süpürge")],
    "scene": lambda: [FakeScene("film_gecesi", "Film Gecesi")],
    "weather": lambda: [FakeWeather("hava", "Ev Havası")],
}


def make_setup(domain):
    """Her platform dosyası için kurulum fonksiyonu üretir."""

    async def async_setup_entry(hass, entry, add_entities):
        add_entities(ENTITIES[domain]())

    return async_setup_entry
