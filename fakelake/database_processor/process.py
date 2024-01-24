from fakelake.models import models
from fakelake.database_processor.datasource.mysql import MysqlSchema
from fakelake.database_processor.datasource.kafka import KafkaSchema


class DatasourceSchemaProcessorFactory:
    @staticmethod
    def create_process(datasource_type: int) -> any:
        if datasource_type == 0:
            return MysqlSchema()
        elif datasource_type == 1:
            return KafkaSchema()
        # elif datasource_type == 2:
        #     return MaxComputeSchema()
        # elif datasource_type == 3:
        #     return PostgresSchema()
        # elif datasource_type == 4:
        #     return DorisSchema()
        # elif datasource_type == 5:
        #     return OracleSchema()
        else:
            raise ValueError("Unsupported datasource type")


class DatasourceSchemaProcessor:
    def __init__(self, datasource: models.DatasourceModel) -> None:
        self._ds = datasource
        self.processor = DatasourceSchemaProcessorFactory.create_process(datasource.type)

    # 获取所有数据库和对应表数据？
    def get_schemas(self) -> list:
        return self.processor.get_schemas(self._ds)

    # 获取所有数据库？
    def get_datasource_dbs(self) -> list:
        return self.processor.get_databases(self._ds)

    # 获取所有数据库信息？
    def get_db_schemas(self, db_name: str) -> list:
        return self.processor.get_db_schemas(self._ds, db_name)

    # 获取数据库的所有表
    def get_schema_tables(self, db_name: str, schema_name: str) -> list:
        return self.processor.get_schema_tables(self._ds, db_name, schema_name)

    # 获取数据库表的所有字段
    def get_table_fields(self, db_name:str, schema_name: str, table_name: str) -> list:
        return self.processor.get_table_fields(self._ds, db_name, schema_name, table_name)