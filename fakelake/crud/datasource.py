from typing import Callable, Any, List

from fakelake.models import models, schemas
from fakelake.models.schemas import DataSourceOutSchema
from fakelake.storage.db import DbHelper
from fakelake.settings import global_settings
from fakelake.crud.common import VersionDatasourceDict
from fakelake.database_processor.process import DatasourceSchemaProcessor


def get_all_datasource(query: schemas.ListAllInSchema, owner_id: int) -> list:
    _query = DbHelper.get_session().query(models.DatasourceModel).order_by(models.DatasourceModel.updated_at.desc())

    if global_settings().current_user.user_name != "admin":
        # 这里按照chatgpt的解释使用更简洁的filter_by,出现不等式再用filter
        _query = _query.filter_by(models.DatasourceModel.owner_id == str(owner_id))

    if query.workspace_id:
        _query = _query.filter_by(models.DatasourceModel.workspace_id == query.workspace_id)

    if query.searchContent:
        _query = _query.filter_by(models.DatasourceModel.name.contains(query.searchContent))

    _version_ds_dict = VersionDatasourceDict.get(int(global_settings().product_info.product_type)).keys()
    print("_version" * 10, _version_ds_dict)

    _query = _query.filter_by(models.DatasourceModel.type.in_(_version_ds_dict))

    """
    这段代码定义了一个名为transformer的函数，它是一个可调用对象，接受一个参数items，并返回一个由
    DataSourceOutSchema对象组成的列表。这里使用了类型注解来说明transformer的类型，它是一个可调用对象，
    接受任意类型的参数，返回一个列表，其中每个元素都是DataSourceOutSchema对象。
   
    具体而言，transformer是一个匿名函数，它接受一个参数items，这个参数是一个可迭代对象（比如列表），
    然后使用列表推导式对每个item进行转换，创建一个DataSourceOutSchema对象的实例。
    最终，transformer返回一个包含转换后对象的列表。

    这种设计通常用于将数据库查询的结果转换为特定的输出格式。在这个例子中，transformer将查询结果中的
    item转换为DataSourceOutSchema对象，并将这些对象放入一个列表中，以便后续使用。
    """

    transformer: Callable[[Any], List[DataSourceOutSchema]] = lambda items: [schemas.DataSourceOutSchema(
        id=item.id,
        datasource_name=item.name,
        type=item.type,
        connection_params=item.connection_params,
        description=item.description,
        workspace_id=item.workspace_id,
        owner_id=item.owner_id,
        created_at=item.created_at,
        updated_at=item.updated_at
    ) for item in items]

    return DbHelper.custom_query_by_paginate(_query, query.page, query.size, transformer=transformer)


def get_datasource(datasource_id: int) -> Any:
    ds = DbHelper.find_one_or_none(models.DatasourceModel, {"datasource_id": datasource_id})
    datasource_out = schemas.DataSourceOutSchema(
        id=ds.id,
        name=ds.name,
        type=ds.type,
        connection_params=ds.connection_params,
        datasource_name=ds.datasource_name,
        description=ds.description,
        workspace_id=ds.workspace_id,
        owner_id=ds.owner_id,
        created_at=ds.created_at,
        updated_at=ds.updated_at
    )
    return datasource_out


def datasource_name_existed(name: str, owner_id: int, workspace_id: int) -> bool:
    _query = DbHelper.get_session().query(models.DatasourceModel).filter_by(
        models.DatasourceModel.name == name,
        models.DatasourceModel.owner_id == str(owner_id),
        models.DatasourceModel.workspace_id == workspace_id
    )

    return _query.one_or_none()


def datasource_existed(datasource_id: int) -> bool:
    # 为什么需要个is None,难道它没有值不会自己返回吗？还要另外加防止错误？
    # return DbHelper.find_one_or_none(models.DatasourceModel, {"id": id}) is None
    return DbHelper.find_one_or_none(models.DatasourceModel, {"datasource_id": datasource_id})


def create_datasource(schema_datasource: schemas.DataSourceSchema):
    datasource = models.DatasourceModel()
    datasource.name = schema_datasource.name
    datasource.type = schema_datasource.type
    datasource.connection_params = schema_datasource.connection_params
    datasource.description = schema_datasource.description
    datasource.workspace_id = schema_datasource.workspace_id
    datasource.owner_id = schema_datasource.owner_id

    return DbHelper.create(datasource)


def update_datasource(datasource_id: int, schema_datasource: schemas.DataSourceOutSchema) -> bool:
    result = DbHelper.update(models.DatasourceModel, {"datasource_id": datasource_id}, schema_datasource)
    return result


def delete_datasource(datasource_id: int) -> bool:
    res = DbHelper.delete(models.DatasourceModel, {"datasource_id": datasource_id})
    return res


# 做咩啊！？哪里用这东西的==
def check_datasource_count() -> bool:
    if global_settings().product_info.product_type in [2, 5, 8]:
        return False

    all_datasource = DbHelper.find_all(models.DatasourceModel)
    if len(all_datasource) >= global_settings().product_info.datasource_count:
        return True

    return False


# 获取数据源类型,干嘛用的啊
def get_datasource_type() -> Any:
    version_datasource = VersionDatasourceDict.get(global_settings().product_info.product_type, 0)
    v_s = []
    for k, v in version_datasource:
        v_s.append({"name": v, "value": k})
    return v_s


def get_db_schema(datasource_id: int) -> Any:
    datasource = get_datasource(datasource_id)
    db_schema_processor = DatasourceSchemaProcessor(datasource)
    return db_schema_processor.get_schemas()


def get_datasource_dbs(datasource_id: int) -> List:
    datasource = get_datasource(datasource_id)
    db_schema_processor = DatasourceSchemaProcessor(datasource)
    return db_schema_processor.get_datasource_dbs()


def get_schema_by_name(datasource_id: int, db_name: str) -> List:
    datasource = get_datasource(datasource_id)
    db_schema_processor = DatasourceSchemaProcessor(datasource)
    return db_schema_processor.get_db_schemas(db_name)


def get_schema_tables(datasource_id: int, db_name: str, schema_name: str) -> List:
    datasource = get_datasource(datasource_id)
    db_schema_processor = DatasourceSchemaProcessor(datasource)
    return db_schema_processor.get_schema_tables(db_name, schema_name)


def get_table_fields(datasource_id: int, db_name: str, schema_name: str, table_name: str) -> List:
    datasource = get_datasource(datasource_id)
    db_schema_processor = DatasourceSchemaProcessor(datasource)
    return db_schema_processor.get_table_fields(db_name, schema_name, table_name)











