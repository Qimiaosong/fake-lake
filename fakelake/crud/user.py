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


def name_existed(name: str) -> bool:
    return DbHelper.find_one_or_none(models.UserModel, {"name": name})


def id_existed(id: int) -> bool:
    return DbHelper.find_one_or_none(models.UserModel, {"id": id})


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






















