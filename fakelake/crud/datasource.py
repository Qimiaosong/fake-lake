from fakelake.models import models, schemas


def get_all_datasource(query: schemas.ListAllInSchema, owner_id: int) -> list:
    _query = DbHelper.get_session().query(models.DatasourceModel).order_by(models.DatasourceModel.updated_at.desc())