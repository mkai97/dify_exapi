# ***Dify扩充API***
- 通过本项目实现通过接口新增一个用户，便于dify和其他系统进行通信。

## 参数解释
 - ***参数具体格式见 .env.example 文件***
   - ***DIFY_API_URL：*** DIFY的API地址
   - ***ADMIN_USER：*** 二级管理员账号
   - ***ADMIN_PASSWORD：*** 二级管理员密码
   - ***NEW_USERPASSWORD：*** 新用户密码（默认aa123456）


## 启动方法
 ### 1. docker-compose 容器启动（推荐，简单）
 - 1.1. 下载项目代码
 - 1.2. 修改 .env 文件，配置参数
 - 1.3. 启动容器
   - `docker compose up --build -d`
 - 1.4. 访问 http://127.0.0.1:8000/docs 即可见到 API 文档
 - 1.5. 停止容器
   - `docker compose down`
   
 ### 2. 本地源码启动
 - 2.1. 下载项目代码
 - 2.2. 修改 .env 文件，配置参数
 - 2.3. 安装依赖包（要先安装 poetry，请自行安装 `https://python-poetry.org/docs/#installation`）
   - `poetry install`
 - 2.4. 启动项目
   - `poetry run uvicorn main:app --reload`
 - 2.5. 访问 http://127.0.0.1:8000/docs 即可见到 API 文档