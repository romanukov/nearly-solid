from dataclasses import dataclass

from ns.entities.const import missing


@dataclass
class EntityDetails:
    name: str  # Имя сущности = название класса
    description: str  # Описание сущности = докстринг класса
    type: type  # Класс сущности, наследник IEntity
    fields: list['FieldDetails']  # Данные полей сущности
    relations: list['Relation']  # Данные о связях с другими сущностями
    id_field_key: str  # Поле ID

    @property
    def id_field(self) -> 'FieldDetails':
        for field in self.fields:
            if field.name == self.id_field_key:
                return field
        raise ValueError(f'ID field of {self.name} entity was not found')

    @property
    def to_one_relations(self) -> list['Relation']:
        return [relation for relation in self.relations if not relation.to_many]

    @property
    def to_many_relations(self) -> list['Relation']:
        return [relation for relation in self.relations if relation.to_many]


@dataclass
class ValueDetails:
    name: str  # Имя объекта-значения = название класса
    description: str  # Описание сущности = докстринг класса
    type: type  # Класс объекта-значения, наследник IValue
    fields: list['FieldDetails']  # Данные полей объекта-значения
    natural_keys: list[str]  # Поля натурального ключа

    @property
    def natural_fields(self) -> list['FieldDetails']:
        return [field for field in self.fields if field.name in self.natural_keys]


@dataclass
class FieldDetails:
    name: str  # Ключ поля
    type: type  # Тип поля: один из примитивных типов или enum
    default_value: any = missing  # Дефолтное значение поля


@dataclass
class Relation:
    name: str  # Ключ поля
    type: type  # Класс сущности, наследник IEntity
    to_many: bool  # Ссылается на массив или на
    is_value: bool = False  # Является ли реляцией на объект-значение
