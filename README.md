# 📖 TaleVoice 智能童话生成 - 后端 API 自动化测试仓库

-  **课程名称：** 敏捷软件开发 - 第4次作业 Sprint 2 
- **学生姓名：** 杨嘉仪
- **学号：** 2313168
- **本轮角色：** 技术负责人 (Tech Lead) / 代码审查员 (Code Reviewer)

## 🎯 仓库简介 (Introduction)

本仓库是 [TaleVoice 项目](https://github.com/MineGuYan/TaleVoice/tree/gyx) 在 Sprint 2 迭代中，针对后端核心微服务 API 编写的**全链路异步自动化测试代码库**。

在本次 Sprint 中，因前端 UI 仍在持续迭代打磨，为了实现敏捷开发中“前后端解耦与并行开发”的目标，我作为 Tech Lead 引入了 **接口契约驱动** 和 **TDD（测试驱动开发）** 的理念。通过编写严密的自动化集成测试脚本，成功验证了后端代码已 100% 达到 Product Owner (PO) 制定的验收标准，确保了主干代码的高质量合并。

---

## 🛠️ 技术栈与架构 (Tech Stack)

*   **语言与框架：** Python 3.12 / FastAPI
*   **测试框架：** `pytest` / `pytest-asyncio` (全面支持异步并发测试)
*   **HTTP 客户端：** `httpx` (Asynchronous ASGI client)
*   **数据库隔离：** `aiosqlite` (内存型 SQLite，实现测试前后数据纯净无污染)
*   **第三方隔离：** `unittest.mock.patch` (精准 Mock 云端 OSS 服务)

---

## 🚀 核心测试策略 (Testing Strategies)

作为代码审核环节的质量保障网，本套测试用例不仅仅是基础的接口调用，更融入了以下高级测试策略：

1.  **端到端全业务流验证 (E2E CRUD Flow)：** 摒弃孤立的单接口测试，采用模拟用户真实行为的流式测试（例如：注册 -> 登录获取 JWT -> 携带 Token 创建项目 -> 依据 ID 修改 -> 验证删除）。
2.  **环境完全隔离：** 利用 FastAPI 的 `dependency_overrides` 机制，在运行测试时自动将真实的 MySQL 数据库劫持并替换为轻量级的内存 SQLite，测试完毕即焚，不产生任何脏数据。
3.  **高级 Mock 技术：** 针对强依赖外部网络环境的 `/common/upload` 阿里云 OSS 上传接口，利用 Patch 技术拦截底层请求并伪造返回值，保障了 CI/CD 流水线在无网或未配置秘钥环境下的绝对稳定性。
4.  **边界与越权拦截测试：** 覆盖了超大文件上传、非格式后缀、以及修改/删除“非本人拥有的项目 ID”等 403/404 边界场景。

---

## 📁 测试模块说明 (Modules)

| 测试文件 | 覆盖模块 | 核心验证点 |
| :--- | :--- | :--- |
| `test_user.py` | 身份认证模块 | 注册/登录逻辑验证、JWT Token 获取与路由鉴权、个人资料全量更新。 |
| `test_project.py` | 项目管理模块 | 项目 CRUD 闭环、**分页逻辑 (`pageSize`) 验证、模糊搜索关键字匹配**。 |
| `test_voice_sample.py`| 音频样本模块 | 用户私有音频的增删改查、越权操作阻断。 |
| `test_common.py` | 通用上传模块 | **第三方 OSS Mock 拦截**、文件扩展名校验、大文件异常拦截。 |

---

## 💻 本地运行指南 (How to Run)

如果您想在本地执行这些测试用例，请按照以下步骤操作：

**1. 安装必要依赖：**
```bash
pip install pytest pytest-asyncio httpx aiosqlite
```

**2. 运行测试套件：**
在项目根目录下，执行以下命令运行全量测试，并查看详尽的接口调用日志：
```bash
# -s 开启控制台详细输出 (展示 Request/Response Body)
# -v 开启详细用例名称展示
# -W ignore 屏蔽底层库的弃用警告，保持输出纯净
pytest tests/ -s -v -W ignore
```

---

## 🌟 Tech Lead 审查与重构贡献 (Key Contributions)

除了编写上述自动化测试脚本，我在本轮 Sprint 中主导解决了以下影响项目交付的严重架构级障碍：

1.  **修复致命的 API 契约拼写 Bug：** 在代码走查中，拦截了 `ProjectListResponse` 模型中将 `data` 错写为 `date` 的严重失误，避免了前端解析崩溃。
2.  **统一前后端全局响应规范：** 打回了 `Common` 模块中自创的冗余 `UploadResponse` (返回 `code=1`)，重构并强制全栈统一使用 `{"code": 200, "message": "..."}` 的 `ResponseModel` 规范。
3.  **消除底层架构技术债：** 协同组员重构了 `main.py` 中过时的 FastAPI `on_event("startup")` 启动装饰器，采用现代化的 `lifespan` 异步上下文管理器；并全面升级了 Pydantic V2 规范，消除了所有运行时的弃用警告（DeprecationWarning）。
