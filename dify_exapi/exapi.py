import os

from dotenv import load_dotenv
from fastapi import HTTPException

from dify_exapi.http_client import HTTPClient

http_client = HTTPClient()

load_dotenv(dotenv_path=".env")


async def dify_exapi(
        role: str,
        emails: str,
        language: str,
):
    if not role or not emails:
        raise HTTPException(status_code=400, detail="role and emails are required")
    try:
        # 调用封装的请求方法
        response = await http_client.request(
            method="POST",
            endpoint="/console/api/login",
            json_data={
                "email": os.getenv("ADMIN_USER"),
                "password": os.getenv("ADMIN_PASSWORD"),
                "language": "zh-Hans",
                "remember_me": True,
            },
        )
        admin_token = response.get("data").get("access_token")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        # 调用封装的请求方法
        response = await http_client.request(
            method="POST",
            endpoint="/console/api/workspaces/current/members/invite-email",
            headers={
                "Authorization": f"Bearer {admin_token}"
            },
            json_data={
                "role": role,
                "emails": emails.split(","),
                "language": language,
            },
        )
        reg_user = response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(reg_user, "reguser")
    if reg_user.get("result") == "success":
        invitation_results = reg_user.get("invitation_results")  # 获取邀请结果
        for result in invitation_results:
            # status 为success 并且 url 不能包含 /signin
            if result.get("status") == "success" and "/signin" not in result.get("url"):
                await reg_current_user(result.get("email"), result.get("url"), admin_token)


async def reg_current_user(email, url, admin_token):
    token = ""
    #  从 url 字符串取出token
    token = url.split("token=")[1]
    try:
        # 调用封装的请求方法
        response = await http_client.request(
            method="GET",
            endpoint="/console/api/activate/check",
            headers={
                "Authorization": f"Bearer {admin_token}"
            },
            params={
                "email": email,
                "token": token
            },
        )
        # {
        #     "is_valid": true,
        #     "data": {
        #         "workspace_name": "admin's Workspace",
        #         "workspace_id": "ec7d3d9e-e21a-4b6d-9edd-b4642f8a3c8e",
        #         "email": "1234@qq.com"
        #     }
        # }
        reg_user = response
        if reg_user.get("is_valid"):
            # /console/api/login
            reg_user_info = await http_client.request(
                method="POST",
                endpoint="/console/api/login",
                json_data={
                    "email": reg_user.get("data").get("email"),
                    "password": os.getenv("ADMIN_PASSWORD", "aa123456"),
                    "language": "zh-Hans",
                    "remember_me": True,
                    "invite_token": token
                },
            )
        return reg_user_info

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
