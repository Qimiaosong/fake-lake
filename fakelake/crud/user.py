from datetime import datetime
from typing import Any

from fakelake.crud.utils import generate_password
from fakelake.models import models
from fakelake.storage.db import DbHelper
from fakelake.models.schemas import (ListAllInSchema, UserOutSchema, UserSchema)
from fakelake.settings import global_settings
from fakelake.submitter.utils import ComputeEngineType


def get_all(query: ListAllInSchema) -> list:
    _query = DbHelper.get_session().query(models.UserModel).join(models.UserWorkspaceRoleModel).filter_by(
        models.UserWorkspaceRoleModel.workspace_id == query.workspace_id
    ).order_by(models.UserModel.updated_at.desc())

    def _get_workspaces(item) -> dict:
        wps = {}
        for user_workspace_role in item.user_workspace_roles:
            wp = user_workspace_role.workspace
            roles = [{"id": uw_role.role.id, "name": uw_role.role.name} for uw_role in wp.workspace_user_roles if uw_role.user_id == item.id]
            if wp.id not in wps:
                wps[wp.id] = {"id": wp.id, "name": wp.name, "roles": roles}
            else:
                wps[wp.id]["roles"] = roles

        print("wps"*10, wps)
        return wps

    transformer = lambda items: [UserOutSchema(
                                id=item.id,
                                name=item.name,
                                password=item.password,
                                license=item.license,
                                workspaces=list(_get_workspaces(item).values()),
                                owner_id=item.owner_id,
                                created_at=item.created_at,
                                updated_at=item.updated_at
    ) for item in items]

    return DbHelper.custom_query_by_paginate(_query, query.page, query.size, transformer=transformer)


def get_by_id(user_id: int) -> Any:
    user = DbHelper.find_one_or_none(models.UserModel, {"user_id": user_id})
    user_value = {"id": user.id, "name": user.name, "password": user.password, "pg_password": user.pg_password,
                  "license": user.license, "owner_id": user.owner_id, "created_at": user.created_at,
                  "updated_at": user.updated_at}
    wps = {}

    # 收集用户在不同工作空间中拥有的角色，并将结果组织成一个包含工作空间ID和角色ID列表的字典
    for user_workspace_role in user.user_workspace_roles:
        wp = user_workspace_role.workspace
        roles = [uw_role.role.id for uw_role in wp.workspace_user_roles if uw_role.user_id == user.id]
        if wp.id not in wps:
            wps[wp.id] = set(roles)
        else:
            wps[wp.id].update(roles)

    user_value["workspaces"] = [{"id": key, "roles": list(values)} for key, values in wps.items()]
    print("user_value"*10, user_value)

    return user_value


def name_existed(name: str) -> bool:
    return DbHelper.find_one_or_none(models.UserModel, {"name": name})


def id_existed(user_id: int) -> bool:
    return DbHelper.find_one_or_none(models.UserModel, {"id": user_id})


def create(userinfo: UserSchema):
    user = models.UserModel(
        name=userinfo.name,
        password=userinfo.password,
        owner_id=userinfo.owner_id,
        pg_password=userinfo.pg_password if userinfo.pg_password else generate_password(),
    )

    u = AuthCasdoor()

    uwrs = []
    for wp in userinfo.workspaces:
        cur_roles = {}
        for role_id in wp.roles:
            uwrs.append(models.UserWorkspaceRoleModel(user=user, workspace_id=wp.id, role_id=role_id))
            cur_role = DbHelper.find_one_or_none(models.RoleModel, {"id": role_id})
            cur_roles[cur_role.role_type] = cur_role
        wp_name = workspace.get_by_id(wp.id).name

        is_admin = False
        if 0 in cur_roles.keys() or 1 in cur_roles.keys():
            is_admin = True

        AuthPg.create_grant_user(wp_name, user.name, user.pg_password, is_admin)
        u.create_user(userinfo.name, userinfo.password, is_admin)

        if global_settings().compute_engine.mode == ComputeEngineType.HADOOP:
            AuthHadoop.create_user(groupname=wp_name, username=user.name, password=user.pg_password,
                                   host="all" if is_admin else "dev")
            AuthHadoop.copy_users(hosts="local")

        # 在casdoor里创建用户？
        u.create_user(userinfo.name, userinfo.password, True if 0 in cur_roles.keys() or 1 in cur_roles.keys() else False)

        if len(cur_roles) > 0:
            print("cur_roles"*10, cur_roles)
            cur_role = next(iter(sorted(cur_roles.items())))[1]

            for mod, pers in cur_role.data_permission.items():
                AuthCasbin().add_policy(user.name, workspace=wp_name, role=cur_role.name,
                                        module_name=mod, module_permissions=pers)

    return DbHelper.create(user) if not uwrs else DbHelper.create_all(uwrs)


def update(user_id: str, userinfo: UserSchema):
    new_user = DbHelper.find_one_or_none(models.UserModel, {"id": user_id})
    new_user.name = userinfo.name
    new_user.password = userinfo.password
    new_user.updated_at = datetime.now()

    # uwrs = []
    # 这是授权啥？
    authCasbin = AuthCasbin()

    uwrs = DbHelper.get_session().query(models.UserWorkspaceRoleModel).filter_by(
        models.UserWorkspaceRoleModel.user_id == user_id).all()

    # remove_policy又是干嘛的？
    for uwr in uwrs:
        authCasbin.remove_policy(uwr.user.name, uwr.workspace.name, uwr.role.name)

    DbHelper.delete(models.UserWorkspaceRoleModel, {"user_id": user_id})

    # uwrs = []
    for wp in userinfo.workspaces:
        is_admin = False
        for role_id in wp.roles:
            uwrs.append(models.UserWorkspaceRoleModel(user=new_user, workspace_id=wp.id, role_id=role_id))
            wp_name = workspace.get_by_id(wp.id).name

            # 获取用户在当前工作空间中的角色信息
            cur_role = DbHelper.get_session().query(models.UserWorkspaceRoleModel).join(models.RoleModel).filter_by(
                models.UserWorkspaceRoleModel.user_id == user_id,
                models.UserWorkspaceRoleModel.workspace_id == wp.id
            ).order_by(models.RoleModel.role_type.asc()).first()

            # 收集用户在所有工作空间中的角色信息，并且判断是否在某个工作空间中具有管理员权限
            if cur_role.role.role_type in [0, 1]:
                is_admin = True

            for mod, pers in cur_role.role.data_permission.items():
                authCasbin.add_policy(
                    new_user.name,
                    workspace=wp_name,
                    role=cur_role.role.name,
                    module_name=mod,
                    module_permissions=pers
                )

        AuthPg.create_grant_user(wp_name, new_user.name, new_user.pg_password, is_admin)

        if global_settings().compute_engine.mode == ComputeEngineType.HADOOP:
            AuthHadoop.create_user(groupname=wp_name, username=new_user.name,
                                   password=new_user.pg_password, hosts="all" if is_admin else "dev")
            AuthHadoop.copy_users(hosts="local")

    return DbHelper.create_all(uwrs)


def delete(user_id: str):
    uwrs = DbHelper.get_session().query(models.UserWorkspaceRoleModel).filter_by(
        models.UserWorkspaceRoleModel.user_id == user_id
    ).all()

    u = AuthCasdoor()
    for uwr in uwrs:
        AuthPg.delete_revoke_user(uwr.workspace.name, uwr.user.name,
                                  True if uwr.role.role_type == 0 else False)

        if global_settings().compute_engine.mode == ComputeEngineType.HADOOP:
            AuthHadoop.delete_user(groupname=uwr.workspace.name, uwr=uwr.user.name,
                                   hosts="all" if uwr.role.role_type == 0 else "dev")
            AuthHadoop.copy_users(hosts="local")

        AuthCasbin().remove_policy(uwr.user.name, uwr.workspace.name, uwr.role.name)
        u.delete_user(uwr.user.name, uwr.user.password)

    return DbHelper.delete(models.UserModel, {"id": user_id})


def login(userinfo: LoginSchema) -> Any:
    user = DbHelper.find_one_or_none(models.UserModel, {"name": userinfo.name})
    if user.password != userinfo.password:
        return False, "password error"
    return True, {"token": generateToken(userinfo.name), "user_id": user.id, "name": user.name}


def logout(cookies: Dict) -> Any:
    pass


def get_permission(user_id: int, workspace_id: int) -> Any:
    pass


def setLicense(userinfo: UserSchema) -> Any:
    pass


def getLicense() -> str:
    pass


def get_license() -> Any:
    pass


def get_ssourer(code: str) -> Any:
    pass


def sync_ssouser() -> Any:
    pass


def get_redirect_uri() -> Any:
    pass


def job_statistics(start_time, end_time, current_user_id: int, current_workspace_id: int) -> Any:
    pass


def about() -> Any:
    pass

























