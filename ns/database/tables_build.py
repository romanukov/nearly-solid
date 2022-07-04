from typing import Optional

from sqlalchemy import Column, Table, MetaData, ForeignKey
from sqlalchemy.orm import relationship, registry

from ns.database.dataclasses import EntitiesData, RelationPair, RelationVector
from ns.database.errors import ErrorCodes, DatabaseError
from ns.database.types_mapping import SA_TYPES_MAPPING
from ns.entities.details import EntityDetails


def get_table_name(entity_data: EntityDetails):
    return entity_data.type.__name__.lower() + 's'


SARelationships = list[tuple[str, relationship]]


class TablesBuilder:
    _tables_columns: dict[str, tuple[EntityDetails, list[Column]]]
    _metadata: MetaData

    def __init__(self, engine):
        self.engine = engine

    def generate_entities_tables(self, entities: list[EntityDetails], create_tables: bool = False):
        entities_data = EntitiesData(entities=entities)
        tables, rels = self.build_tables(entities_data)
        for entity_details, table, rels in tables:
            table.create(self.engine)
        print(tables)
        # self.map_tables(tables, rels, create_tables)

    def map_tables(self, tables: list[tuple[EntityDetails, Table, Optional[SARelationships]]], m2m_tables: list[Table],
                   create=False):
        mapper_registry = registry()
        for entity_data, table, relationships in tables:
            properties = None
            if relationships:
                properties = {}
                for prop_name, relationship_ in relationships:
                    properties[prop_name] = relationship_
            print(table.__dict__)
            if create:
                table.create(self.engine)
            mapper_registry.map_imperatively(entity_data.type, table, properties=properties)
        for table in m2m_tables:
            if create:
                table.create(self.engine)

    def build_tables(self, entities_data: EntitiesData) -> \
            tuple[list[tuple[EntityDetails, Table, Optional[SARelationships]]], list[Table]]:
        self._tables_columns = self._build_primitives(entities_data)
        self._metadata = MetaData()
        foreign_keys: dict[str, list[Column]]
        relationships: dict[str, list[relationship]]
        m2m_tables, foreign_keys, relationships = self._build_fk_and_rels(entities_data)
        for table_name, columns in foreign_keys.items():
            self._tables_columns[table_name][1].extend(columns)
        tables = []
        for table_name, (entity_data, columns) in self._tables_columns.items():
            table = Table(table_name, self._metadata, *columns)
            tables.append((entity_data, table, relationships.get(table_name)))
        return tables, m2m_tables

    def _build_primitives(self, entities_data: EntitiesData) -> dict[str, tuple[EntityDetails, list[Column]]]:
        result = {}
        for entity_data in entities_data.entities:
            table_name = get_table_name(entity_data)
            result[table_name] = entity_data, self._build_primitive(entity_data)
        return result

    def _build_primitive(self, entity_data: EntityDetails) -> list[Column]:
        columns = []
        for field in entity_data.fields:
            field_name = field.name
            field_type = field.type
            column_type = SA_TYPES_MAPPING.get(field_type)
            if not column_type:
                continue
            column_kwargs = {}
            if field_name == entity_data.id_field_key:
                column_kwargs['primary_key'] = True
                print('PRIMARY KEY', field_name)
            column = Column(field_name, column_type, **column_kwargs)
            columns.append(column)
        return columns

    def _build_fk_and_rels(self, entities_data: EntitiesData) -> \
            tuple[list[Table], dict[str, list[Column]], dict[str, list[tuple[str, relationship]]]]:
        tables_columns, tables_rels = ({}, {})

        for relation in entities_data.just_foreign_keys:
            raise DatabaseError(
                ErrorCodes.FOREIGN_KEY_HAS_NO_BACK_REFERENCE,
                from_entity=relation.from_entity.name,
                from_field=relation.from_key,
                to_entity=relation.to_entity.name,
            )

        for relation in entities_data.one_to_one_relations:
            columns, relationships = self.build_o2o(relation)
            for table_name, column in columns.items():
                if table_name not in tables_columns:
                    tables_columns[table_name] = []
                tables_columns[table_name].append(column)
            for table_name, rel in relationships.items():
                if table_name not in tables_rels:
                    tables_rels[table_name] = []
                tables_rels[table_name].append(rel)

        for relation in entities_data.many_to_one_relations:
            columns, relationships = self.build_m2o(relation)
            for table_name, column in columns.items():
                if table_name not in tables_columns:
                    tables_columns[table_name] = []
                tables_columns[table_name].append(column)
            for table_name, rel in relationships.items():
                if table_name not in tables_rels:
                    tables_rels[table_name] = []
                tables_rels[table_name].append(rel)

        tables = []
        for relation in entities_data.many_to_many_relations:
            table, relationships = self.build_m2m(relation)
            for table_name, rel in relationships.items():
                if table_name not in tables_rels:
                    tables_rels[table_name] = []
                tables_rels[table_name].append(rel)
            tables.append(table)

        return tables, tables_columns, tables_rels

    def build_o2o(self, relation: RelationPair) -> tuple[dict[str, Column], dict[str, tuple[str, relationship]]]:
        from_key, to_key = relation.keys
        from_entity, to_entity = relation.entities
        from_table_name, to_table_name = get_table_name(from_entity), get_table_name(to_entity)
        from_pk, to_pk = from_entity.id_field_key, to_entity.id_field_key
        from_field = next(f for f in from_entity.fields if f.name == from_entity.id_field_key)
        to_field = next(f for f in to_entity.fields if f.name == to_entity.id_field_key)
        from_type, to_type = (
            SA_TYPES_MAPPING.get(from_field.type),
            SA_TYPES_MAPPING.get(to_field.type),
        )

        from_column = Column(
            f'{from_key}_{to_pk}', to_type,
            ForeignKey(f'{to_table_name}.{to_pk}'),
        )
        columns = {from_table_name: from_column}

        from_relationship = relationship(to_entity.type, back_populates=to_key, uselist=False)
        to_relationship = relationship(from_entity.type, back_populates=from_key, uselist=False)
        relationships = {
            from_table_name: (from_key, from_relationship),
            to_table_name: (to_key, to_relationship),
        }

        return columns, relationships

    def build_m2o(self, relation: RelationVector) -> tuple[dict[str, Column], dict[str, tuple[str, relationship]]]:
        from_key, to_key = relation.from_key, relation.to_key
        from_entity, to_entity = relation.from_entity, relation.to_entity
        from_table_name, to_table_name = get_table_name(from_entity), get_table_name(to_entity)
        from_pk, to_pk = from_entity.id_field_key, to_entity.id_field_key
        from_field = next(f for f in from_entity.fields if f.name == from_entity.id_field_key)
        to_field = next(f for f in to_entity.fields if f.name == to_entity.id_field_key)
        from_type, to_type = (
            SA_TYPES_MAPPING.get(from_field.type),
            SA_TYPES_MAPPING.get(to_field.type),
        )

        to_column = Column(
            f'{to_key}_{from_pk}', from_type,
            ForeignKey(f'{from_table_name}.{from_pk}'),
        )
        columns = {to_table_name: to_column}

        from_relationship = relationship(to_entity.type, back_populates=to_key, uselist=True)
        to_relationship = relationship(from_entity.type, back_populates=from_key, uselist=False)
        relationships = {
            from_table_name: (from_key, from_relationship),
            to_table_name: (to_key, to_relationship),
        }
        return columns, relationships

    def build_m2m(self, relation: RelationPair) -> tuple[Table, dict[str, tuple[str, relationship]]]:
        from_key, to_key = relation.keys
        from_entity, to_entity = relation.entities
        from_table_name, to_table_name = get_table_name(from_entity), get_table_name(to_entity)
        from_pk, to_pk = from_entity.id_field_key, to_entity.id_field_key
        from_field = next(f for f in from_entity.fields if f.name == from_entity.id_field_key)
        to_field = next(f for f in to_entity.fields if f.name == to_entity.id_field_key)
        from_type, to_type = (
            SA_TYPES_MAPPING.get(from_field.type),
            SA_TYPES_MAPPING.get(to_field.type),
        )

        association_table_name = f'association_from_{from_table_name}_to_{to_table_name}'
        association_from = f'{from_key}_{from_pk}'
        association_to = f'{to_key}_{to_pk}'
        association_table = Table(
            association_table_name, self._metadata,
            Column(association_from, to_type, ForeignKey(f'{to_table_name}.{to_pk}')),
            Column(association_to, from_type, ForeignKey(f'{from_table_name}.{from_pk}')),
        )

        from_relationship = relationship(
            to_entity.type,
            secondary=association_table,
            back_populates=to_key,
            uselist=True,
        )
        to_relationship = relationship(
            from_entity.type,
            secondary=association_table,
            back_populates=from_key,
            uselist=True,
        )
        relationships = {
            from_table_name: (from_key, from_relationship),
            to_table_name: (to_key, to_relationship),
        }
        return association_table, relationships
