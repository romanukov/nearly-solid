from dataclasses import dataclass
from typing import Optional

from ns.entities.details import EntityDetails

RelationsDict = dict[str, tuple[str, type]]


@dataclass
class RelationVector:
    from_key: str
    from_entity: EntityDetails
    to_key: Optional[str]
    to_entity: EntityDetails

    def __hash__(self):
        return hash((self.from_key, self.from_entity, self.to_key, self.to_entity))

    def __eq__(self, other):
        if not isinstance(other, RelationVector):
            return False
        return (
            self.from_key == other.from_key and
            self.from_entity == other.from_entity and
            self.to_key == other.to_key and
            self.to_entity == other.to_entity
        )

    def __neg__(self):
        return RelationVector(
            from_key=self.to_key,
            from_entity=self.to_entity,
            to_key=self.from_key,
            to_entity=self.from_entity,
        )

    def __str__(self):
        return f'RelationVector[{self.from_entity.type.__name__}.{self.from_key} --> ' \
               f'{self.to_entity.type.__name__}.{self.to_key}]'


@dataclass
class RelationPair:
    keys: tuple[str, str]
    entities: tuple[EntityDetails, EntityDetails]

    def __hash__(self):
        relation1 = self.keys[0], self.entities[0].__hash__()
        relation2 = self.keys[1], self.entities[1].__hash__()
        return hash(frozenset({relation1, relation2}))

    def __eq__(self, other):
        if not isinstance(other, RelationPair):
            return False
        self_relation1 = self.keys[0], self.entities[0].__hash__()
        self_relation2 = self.keys[1], self.entities[1].__hash__()

        other_relation1 = other.keys[0], other.entities[0].__hash__()
        other_relation2 = other.keys[1], other.entities[1].__hash__()
        return (
            self_relation1 == other_relation1 and self_relation2 == other_relation2
            or
            self_relation1 == other_relation2 and self_relation2 == other_relation1
        )

    def __str__(self):
        relation1_entity, relation1_key = self.entities[0], self.keys[0]
        relation2_entity, relation2_key = self.entities[1], self.keys[1]
        return f'RelationPair[{relation1_entity.type.__name__}.{relation1_key} <--> ' \
               f'{relation2_entity.type.__name__}.{relation2_key}]'


@dataclass
class EntitiesData:
    entities: list[EntityDetails]

    def get(self, cls: type) -> EntityDetails:
        for entity in self.entities:
            if entity.type == cls or entity.type == cls.__name__:
                return entity
        raise KeyError(f'Entity for <{cls}> was not found')

    @property
    def to_one_relations(self) -> list[RelationVector]:
        result = []
        for entity in self.entities:
            for relation in entity.to_one_relations:
                name, relation_type = relation.name, relation.type
                field_name, cls = name, relation_type
                relation = self.get(cls)
                relation_pair = RelationVector(
                    from_key=field_name,
                    from_entity=entity,
                    to_key=None,
                    to_entity=relation,
                )
                result.append(relation_pair)
        return result

    @property
    def to_many_relations(self) -> list[RelationVector]:
        result = []
        for entity in self.entities:
            for relation in entity.to_many_relations:
                name, relation_type = relation.name, relation.type
                field_name, cls = relation_type
                relation = self.get(cls)
                relation_pair = RelationVector(
                    from_key=field_name,
                    from_entity=entity,
                    to_key=None,
                    to_entity=relation,
                )
                result.append(relation_pair)
        return result

    def get_relation(self, from_: EntityDetails, to: EntityDetails, to_many: bool = False) -> Optional[RelationVector]:
        search_list = self.to_many_relations if to_many else self.to_one_relations
        for relation in search_list:
            if relation.from_entity == from_ and relation.to_entity == to:
                return relation

    @property
    def just_foreign_keys(self) -> set[RelationVector]:
        result = set()
        for relation in self.to_one_relations:
            reverse_one_relation = self.get_relation(relation.to_entity, relation.from_entity)
            reverse_many_relation = self.get_relation(relation.to_entity, relation.from_entity, to_many=True)
            if not reverse_one_relation and not reverse_many_relation:
                result.add(relation)
        for relation in self.to_many_relations:
            reverse_one_relation = self.get_relation(relation.to_entity, relation.from_entity)
            reverse_many_relation = self.get_relation(relation.to_entity, relation.from_entity, to_many=True)
            if not reverse_one_relation and not reverse_many_relation:
                result.add(-relation)
        return result

    @property
    def one_to_one_relations(self) -> set[RelationPair]:
        result = set()
        for relation in self.to_one_relations:
            reverse_relation = self.get_relation(relation.to_entity, relation.from_entity)
            if reverse_relation:
                relation = RelationPair(
                    keys=(reverse_relation.from_key, relation.from_key),
                    entities=(reverse_relation.from_entity, relation.from_entity),
                )
                result.add(relation)
        return result

    @property
    def many_to_one_relations(self) -> list[RelationVector]:
        result = []
        for relation in self.to_one_relations:
            reverse_relation = self.get_relation(relation.to_entity, relation.from_entity, to_many=True)
            if reverse_relation:
                relation_pair = RelationVector(
                    from_key=reverse_relation.from_key,
                    from_entity=reverse_relation.from_entity,
                    to_key=relation.from_key,
                    to_entity=relation.from_entity,
                )
                result.append(relation_pair)
        return result

    @property
    def many_to_many_relations(self) -> set[RelationPair]:
        result = set()
        for relation in self.to_many_relations:
            reverse_relation = self.get_relation(relation.to_entity, relation.from_entity, to_many=True)
            if reverse_relation:
                relation = RelationPair(
                    keys=(reverse_relation.from_key, relation.from_key),
                    entities=(reverse_relation.from_entity, relation.from_entity),
                )
                result.add(relation)
        return result
