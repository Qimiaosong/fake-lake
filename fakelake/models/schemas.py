from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field


class ListAllInSchema(BaseModel):
    workspace_id: Optional[int] = Field(description="工作空间ID")
    searchContent: str = Field(description="搜索内容", default="")
    page: int = Field(description="页码", default=1)
    size: int = Field(description="每页数量", default=50)


class UserWorkspaceSchema(BaseModel):
    id: str = Field(description="工作空间ID")
    name: Optional[str] = Field(description="工作空间名称")
    roles: List = Field(description="对应的角色的ID集")


class UserSchema(BaseModel):
    name: str = Field(description="用户名")
    password: Optional[str] = Field(description="密码")
    workspaces: Optional[List[UserWorkspaceSchema]] = Field(default=[], description="工作空间")
    license: Optional[str] = Field(description="用户授权license")
    owner_id: Optional[str] = Field(description="创建者用户id")
    pg_password: Optional[str] = Field(description="postgresql用户密码")


class RoleSchema(BaseModel):
    name: str = Field(description="角色名")
    data_permission: Optional[Dict] = Field(description="数据权限")
    role_type: Optional[int] = Field(description="角色类型")
    owner_id: int = Field(description="创建者用户id")


class UserOutSchema(UserSchema):
    id: int = Field(description="数据入湖任务ID")
    created_at: datetime = Field(description="数据入湖任务创建时间")
    updated_at: datetime = Field(description="数据入湖任务更新时间")


# 当创建一个新的数据源时需要提供的信息的结构
class DataSourceSchema(BaseModel):
    name: str = Field(description="数据源名称")
    type: int = Field(description="数据源类型：0 - mysql")
    connection_params: Dict = Field(description="数据库连接信息")
    description: str = Field(description="数据源描述信息")
    workspace_id: int = Field(description="数据源所属工作空间ID")
    owner_id: int = Field(description="数据源创建者ID")


# 当数据源成功创建之后，返回给客户端的数据的结构
class DataSourceOutSchema(DataSourceSchema):
    id: int = Field(description="数据源ID")
    created_at: datetime = Field(description="数据源创建时间")
    updated_at: datetime = Field(description="数据源更新时间")

