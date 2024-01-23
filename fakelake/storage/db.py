from typing import Dict, Any

from fastapi_sqlalchemy import db
from loguru import logger

from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate


class DbHelper:
    # @staticmethod静态方法属于类，适合数学运算或工具函数
    @staticmethod
    def create(model, commit: bool = True) -> bool:
        try:
            logger.info(f"insert into {model}")
            db.session.add(model)
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def create_all(model, commit: bool = True):
        try:
            logger.info(f"insert into {model}")
            db.session.add_all(model)
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def update(model, properties: Dict[str, Any], values: Dict[str, Any] = None, commit: bool = True):
        try:
            logger.info(f"update {model}, filter param is {properties}")
            db.session.query(model).filter_by(**properties).update(values)
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def delete(model, properties: Dict[str, Any], commit: bool = True) -> bool:
        try:
            logger.info(f"delete {model}, filter param is {properties}")
            db.session.query(model).filter_by(**properties).delete()
            if commit:
                db.session.commit()
            return True
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def find_all(model) -> list:
        logger.info(f"get {model} all data")
        return db.session.query(model).all()

    @staticmethod
    def find_one_or_none(model, properties: Dict[str, Any]):
        logger.info(f"find {model} data, and param is {properties}")
        return db.session.query(model).filter_by(**properties).one_or_none()

    @staticmethod
    def find_list(model, properties: Dict[str, Any]):
        logger.info(f"find {model} data, and param is {properties}")
        return db.session.query(model).filter_by(**properties).all()

    @staticmethod
    def execute(statement, params=None) -> Any:
        return db.session.execute(statement, params)

    @staticmethod
    def custom_query_by_paginate(query, page: int, page_size: int, transformer=None) -> Any:
        if page == 0 and page_size == 0:
            res = query.all()
            return Page(items=res, total=len(res))
        return paginate(query, params=Params(page=page, size=page_size), transformer=transformer)

    @staticmethod
    def get_session():
        return db.session
