from fastapi import APIRouter, Body, Depends, Request
from loguru import logger

from fakelake.api.depend import get_current_userinfo
from fakelake.api.common import FakelakeStatusCode, FakelakeStatusMsg
from fakelake.api.utils import response
from fakelake.crud import data_analysis, remote_script
from fakelake.models.schemas import (DataAnalysisSchema, GetScriptContent, ListScriptsSchema)

router = APIRouter()
_tags = ["DataAnalysis"]


@router.get("/getTablesByEnv/{env_id}", tags=_tags, dependencies=[Depends(get_current_userinfo)])
async def get_tables_by_env(env_id: int):
    try:
        res = data_analysis.get_fakelaketable(env_id)
        if res:
            return response(FakelakeStatusCode.QUERY_SUCCESS,
                            FakelakeStatusMsg.QUERT_SUCESS, res)
        return response(FakelakeStatusCode.QUERY_FAILED,
                        FakelakeStatusMsg.QUERY_FAILED)
    except Exception as e:
        logger.exception(e)
        return response(FakelakeStatusCode.FAIL,
                        FakelakeStatusMsg.FAIL, e)

