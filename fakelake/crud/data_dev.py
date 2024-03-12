import os
from typing import Any

from loguru import logger
from fakelake.settings import global_settings
from fakelake.models import models
from fakelake.storage.db import DbHelper
from fakelake.submitter.submitter import Submitter
from fakelake.submitter.utils import JobType

_settings = global_settings()


def start(id: int, current_user_id: int, current_workspace_id: int) -> Any:
    try:
        datadev = DbHelper.find_one_or_none(models.DataDevModel, {"id": id})
        logger.info(f"current start task publish job, id is : {id}, and name is : {datadev.name}")
        job_name = f"{datadev.name}-{current_user_id}{current_workspace_id}"
        submit_type = "flink" if datadev.sql_engine == 0 else "spark"
        language = "sql"
        content = datadev.sql_info["sql_details"]
        os.makedirs(_settings.compute_engine.work_dir, exist_ok=True)
        with open(f"{_settings.compute_engine.work_dir}/{job_name}.txt", "w") as f:
            f.write(content)

        _savepoint = f"{datadev.job.env.storage_workdir}/{job_name}/flink_savepoint"
        if datadev.job and datadev.job.result and datadev.job.result.get("savepoint_path"):
            _savepoint = f'{_savepoint}/{datadev.job.result["savepoint_path"]}'

        (ip, port) = datadev.job.env.address.split(":")
        submitter = Submitter(config={"ip":ip, "port":port, "env":datadev.job.env.env_config},
                              engine_type=_settings.compute_engine.mode,
                              job_type=JobType.FLINK if datadev.sql_engine == 0 else JobType.SPARK)
        submitter.copyFromLocal(f'{_settings.compute_engine.work_dir}/{job_name}.txt')
        submitter.set_auth(_settings.current_user.real_user_name,
                           _settings.current_user.pg_password,
                           _settings.current_user.workspace_name)
        res, err = submitter.submit(job_name, _settings.flink_jar.path,
                                    _settings.flink_jar.data_dev_class,
                                    f'-Dtaskmanager.numberOfTaskSlots={datadev.sql_info.get("slot", 1)})',
                                    f'-Dtaskmanager.memory.process.size={datadev.sql_info.get("memory_process_size", 1024)}',
                                    f'-Dtaskmanager.memory.task.off-heap.size={datadev.sql_info.get("memory_offheap_size", 1024)}',
                                    '--submit_type', submit_type, '--job_type', datadev.sql_info["job_type"],
                                    '--job.checkpoint_interval', str(datadev.sql_info["checkpoint_interval"]),
                                    '--language', language, '--sql_file_path', f'{datadev.job.env.storage_workdir}/data_dev/{job_name}.txt',
                                    '--flink.checkpoint', f"{datadev.job.env.storage_workdir}/{job_name}/flink_checkpoint",
                                    '-s', _savepoint)

        if submitter.getAppStatus(job_name, is_history=True) == -1 and not res:
            DbHelper.update(models.JobManagerModel, {"id": datadev.job_id}, {"status":3, "result": {"job_id": job_name, "job_type": 0}})
            return 3, err
        else:
            DbHelper.update(models.JobManagerModel, {"id": datadev.job_id}, {"status":0, "result": {"job_id": job_name, "job_type": 0}})
            return 0, err

    except Exception as e:
        logger.exception(f"start date dev job failed, reason is : {e}")
        return 3, err















