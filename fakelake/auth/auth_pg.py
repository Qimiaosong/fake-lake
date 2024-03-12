from loguru import logger
from sqlalchemy import text

from fakelake.storage.db import DbHelper


class AuthPg:
    @staticmethod
    def create_grant_workspace(workspace: str):
        is_existed = DbHelper.execute(text(f"SELECT 1 FROM pg_roles WHERE rolename = '{workspace}'"))
        if len(is_existed.all()) == 0:
            create_role = text(f'CREATE ROLE "{workspace}" WITH INHERIT')
            DbHelper.execute(create_role)

        is_existed = DbHelper.execute(text(f"SELECT 1 FROM pg_roles WHERE rolename = '{workspace}_admins'"))
        if len(is_existed.all()) == 0:
            create_role_admin = text(f'CREATE ROLE "{workspace}_admins" WITH INHERIT')
            DbHelper.execute(create_role_admin)

        is_existed = DbHelper.execute(text(f"SELECT 1 FROM pg_roles WHERE rolename = '{workspace}_users'"))
        if len(is_existed.all()) == 0:
            create_role_user = text(f'CREATE ROLE "{workspace}_users" WITH INHERIT')
            DbHelper.execute(create_role_user)

        # 给workspace_admins角色授予'base_admin_role'权限
        grant_role_admin = text(f'GRANT base_admin_role TO "{workspace}_admins"')
        DbHelper.execute(grant_role_admin)

        # 给workspace_users角色授予'base_user_role'权限
        grant_role_user = text(f'GRANT base_user_role TO "{workspace}_users"')
        DbHelper.execute(grant_role_user)

    @staticmethod
    def create_grant_user(workspace: str, user: str, password: str, is_admin: bool=False):
        password = CommonUtil.parse_secret_password(password, global_settings().db.secret_key)
        is_existed = DbHelper.execute(text(f"SELECT 1 FROM pg_roles WHERE rolename='{user}'"))
        if is_existed and len(is_existed(all)) == 0:
            create_user = text(f"CREATE USER \"{user}\" WITH PASSWORD '{password}'")
            logger.info(f"CREATE USER \"{user}\" WITH PASSWORD '******'")
            DbHelper.execute(create_user)
        grant_user = text(f'GRANT "{workspace}" TO "{user}"')
        DbHelper.execute(grant_user)
        if is_admin:
            role_name = f"{workspace}_admins"
        else:
            role_name = f"{workspace}_users"
        grant_user = text(f'GRANT "{role_name}" TO {user}')
        DbHelper.execute(grant_user)

    @staticmethod
    def delete_revoke_workspace(workspace: str):
        revoke_role_admin = text(f'REVOKE "{workspace}_admins" FROM base_admin_role')
        DbHelper.execute(revoke_role_admin)

        revoke_role_user = text(f'REVOKE "{workspace}_users" FROM base_user_role')
        DbHelper.execute(revoke_role_user)

        # 检查数据库中是否存在名为{workspace}的角色，如果存在就将其删除
        is_existed = DbHelper.execute(text(f"SELECT 1 FROM pg_roles WHERE rolename = '{workspace}'"))
        if is_existed and len(is_existed.all()) > 0:
            drop_role = text(f'DROP ROLE "{workspace}"')
            DbHelper.execute(drop_role)

        is_existed = DbHelper.execute(text(f"SELECT 1 FROM pg_roles WHERE rolename = '{workspace}_admins'"))
        if is_existed and len(is_existed.all()) > 0:
            drop_role_admin = text(f'DROP ROLE "{workspace}_admins"')
            DbHelper.execute(drop_role_admin)

        is_existed = DbHelper.execute(text(f"SELECT 1 FROM pg_roles WHERE rolename = '{workspace}_users'"))
        if is_existed:
            drop_role_user = text(f'DROP ROLE "{workspace}_users"')
            DbHelper.execute(drop_role_user)

    # 从postgreSQL数据库中删除用户以及撤销与用户相关的角色关联的功能
    @staticmethod
    def delete_revoke_user(workspace: str, user: str, is_admin: bool=False):
        is_existed = DbHelper.execute(text(f"SELECT 1 FROM pg_roles WHERE rolename = '{user}'"))
        if is_existed and len(is_existed.all()) > 0:
            # 撤销在特定工作空间与用户相关联的角色，revoke关键字撤销了用户对工作空间的访问权限
            revoke_user = text(f'REVOKE "{user}" FROM "{workspace}"')
            DbHelper.execute(revoke_user)
            if is_admin:
                role_name = f"{workspace}_admins"
            else:
                role_name = f"{workspace}_users"
            # 从指定的角色中撤销指定用户的权限
            revoke_user = text(f'REVOKE "{user}" FROM "{role_name}"')
            DbHelper.execute(revoke_user)

            drop_user = text(f'DROP USER "{user}"')
            logger.info(drop_user)
            # 删除用户
            DbHelper.execute(drop_user)


















