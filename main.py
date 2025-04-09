import os

from dotenv import load_dotenv
from fastapi import FastAPI, Query

from dify_exapi.exapi import dify_exapi

load_dotenv(dotenv_path=".env")

app = FastAPI()


@app.get("/")
async def root():
    """
        启动服务并返回启动信息。
    """

    return {
        "message": "The service has started successfully!",
        "version": "1.0",
        'tips': "Please visit /docs to see the API documentation."}


@app.get("/addMembers")
async def add_members(
        role: str = Query("normal", description="角色: editor 或 normal"),
        emails: str = Query(..., description="邮箱（单个账号激活）"),
        language: str = Query("zh-Hans", description="语言"), ):
    """
        添加成员。
    """
    print(role, emails, language)

    return await dify_exapi(role, emails, language)
