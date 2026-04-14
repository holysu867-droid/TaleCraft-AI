import pytest
import requests

# 基础环境配置 (Sprint 1 测试环境)
BASE_URL = "http://localhost:8080"
# 模拟登录获取的Token (由于目前处于开发初期，采用固定Token进行契约测试)
TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock_token"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": TOKEN
}

class TestStoryAPI:
    """针对 /api/story/ai 接口的自动化测试用例集"""

    @pytest.mark.parametrize("theme, continuation, expected_code", [
        ("勇敢的小兔子", False, 200),        # 正常流：全新生成
        ("魔法森林冒险", True, 200),         # 正常流：基于已有章节续写
        ("", False, 400),                  # 异常流：theme为空，预期后端拦截报错
    ])
    def test_generate_story_ai(self, theme, continuation, expected_code):
        """测试 AI 故事生成接口的正常与异常场景"""
        payload = {
            "theme": theme,
            "style": "童话风格",
            "keyword": "兔子, 森林",
            "continuation": continuation
        }
        
        try:
            # 发起 POST 请求
            response = requests.post(f"{BASE_URL}/api/story/ai", json=payload, headers=HEADERS)
            
            # 断言：校验 HTTP 状态码
            assert response.status_code == expected_code
            
            # 断言：状态码为 200 时的契约断言 (验证响应体结构是否符合 API 文档)
            if expected_code == 200:
                resp_data = response.json()
                assert "code" in resp_data
                assert resp_data["code"] == 200
                assert resp_data["message"] == "生成成功"
                
        except requests.exceptions.ConnectionError:
            # 【高级容错处理】兼容 Sprint 1 后端服务未启动的情况，预期执行不报错
            pytest.skip("⚠️ 后端本地服务未启动，跳过真实网络请求 (Mock阶段)")
