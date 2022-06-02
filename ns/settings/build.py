from inspect import getmembers

from ns.settings.base.interfaces import ISettingsMagic
from ns.settings.const import ALLOWED_BUILTIN_TYPES
from ns.settings.errors import SettingsError, SettingsErrorCodes
from ns.settings.fields import ConfigField
from ns.settings.parser import ISettingsParser, EnvSettingsParser


class SettingsBuilder:
    parser: ISettingsParser = EnvSettingsParser()

    def build(self, cls: type):
        cls: ISettingsMagic
        members: dict[str, any] = dict(getmembers(cls))
        settings_fields = {}
        type_annotations = cls.__annotations__
        for member_key, member_value in members.items():
            if not isinstance(member_value, ConfigField):
                continue
            if member_key.startswith('_'):
                raise SettingsError(SettingsErrorCodes.SETTING_KEY_IS_REQUIRED, key=member_key)
            if not member_value.key:
                member_value.key = member_key
            cast = type_annotations[member_key] if member_key in type_annotations else str
            if cast not in ALLOWED_BUILTIN_TYPES:
                raise SettingsError(SettingsErrorCodes.SETTING_TYPE_IS_NOT_ALLOWED, key=member_key)
            setting_value = self.parser.get_setting(member_key, cast=cast)
            member_value.cast = cast
            settings_fields[member_key] = member_value
            setattr(cls, member_key, setting_value)
        cls.__settings_fields__ = settings_fields
