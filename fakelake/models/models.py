from datetime import datetime

from sqlalchemy import (JSON, Column, DateTime, ForeignKey, Integer, String, Text, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseModel:
    fields = None

    def __new__(cls):
        if not cls.fields:
            cls.fields = [attr.key for attr in cls.__mapper__.attrs]
        return object.__new__(cls)

    def __iter__(self):
        return next(self)

    def __next__(self):
        for key in self.__class__.fields:
            val = getattr(self, key)
            yield key, val


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, comment="用户名，不可重复")
    password = Column(String, comment="密码")
    license = Column(String, nullable=True, comment="用户license")
    owner_id = Column(Integer, ForeignKey('user.id'), comment="用户所属的用户id")
    created_at = Column(DateTime, default=datetime.now)
    pg_password = Column(String, comment="postgresql用户密码")
    updated_at = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    user_workspace_roles = relationship('UserWorkspaceRoleModel', back_populates='user')


class RoleModel(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True, comment="角色名，不可重复")
    data_permission = Column(JSON, default={}, comment="数据权限信息")
    role_type = Column(Integer, default=0, comment="角色类型")
    owner_id = Column(Integer, ForeignKey('user.id'), comment="角色所属的用户id")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    role_user_workspace = relationship('UserWorkspaceRoleModel', back_populates='role')


class WorkspaceModel(Base):
    __tablename__ = "workspace"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True, comment="工作空间名，不可重复")
    owner_id = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    workspace_user_roles = relationship('UserWorkspaceRoleModel', back_populates='workspace')


class UserWorkspaceRoleModel(Base):
    __tablename__ = 'user_workspace_role'
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspace.id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)

    user = relationship('UserModel', back_populates='user_workspace_roles')
    workspace = relationship('WorkspaceModel', back_populates='workspace_user_roles')
    role = relationship('RoleModel', back_populates='role_user_workspace')


class ConfigModel(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True, comment="配置名，不可重复")
    config_info = Column(Text, default="", comment="配置信息")
    owner_id = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now, default=datetime.now)


class DatasourceModel(BaseModel, Base):
    __tablename__ = "datasource"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="数据源ID")
    name = Column(String, comment="数据源名称，不可重复")
    type = Column(Integer, comment="数据源类型，0 - mysql")
    connection_params = Column(JSON, default={}, comment="数据源连接信息")
    description = Column(Text, comment="数据源描述信息")
    workspace_id = Column(Integer, ForeignKey('workspace.id'), comment="数据源所属工作空间ID")
    owner_id = Column(Integer, ForeignKey('user.id'), comment="数据源所属用户ID")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now, default=datetime.now)








