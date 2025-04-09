import os
import httpx
from typing import Dict, Any, Optional
import logging

from dotenv import load_dotenv
from fastapi import HTTPException

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=".env")
apiurl = os.getenv("DIFY_API_URL")
print(apiurl, "目标服务器地址")

class HTTPClient:
    def __init__(self, base_url: str = apiurl or "http://0.0.0.0:5001"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        通用 HTTP 请求方法
        :param method: 请求方法 (GET, POST, PUT, DELETE)
        :param endpoint: 接口路径 (e.g., "/console/api/workspaces/current/members/invite-email")
        :param params: URL 查询参数 (GET 请求用)
        :param json_data: JSON 请求体 (POST/PUT 请求用)
        :param headers: 自定义请求头
        :return: 接口返回的 JSON 数据
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()  # 检查 HTTP 错误
            logger.info(f"请求成功: {url} -> {response.status_code}")
            self.client.aclose()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"请求失败: {url} -> {e.response.status_code} {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"目标服务器返回错误: {e.response.text}",
            )
        except httpx.RequestError as e:
            logger.error(f"请求失败: {url} -> {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"请求目标服务器失败: {str(e)}",
            )
        except Exception as e:
            logger.error(f"未知错误: {url} -> {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"未知错误: {str(e)}",
            )

    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()