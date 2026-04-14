import pytest
import requests

BASE_URL = "http://localhost:8080"
TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock_token"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": TOKEN
}

class TestAudioAPI:
    """针对 /api/audio 接口的自动化测试用例集"""

    @pytest.mark.parametrize("speechRate, expected_code", [
        (1.0, 200),   # 正常值：标准语速
        (0.5, 200),   # 边界值：API文档规定的最低语速
        (2.0, 200),   # 边界值：API文档规定的最高语速
        (2.5, 400),   # 异常值：超出 0.5~2 范围，预期后端应拦截
        (-1.0, 400),  # 异常值：非法负数语速
    ])
    def test_audio_generation_rate_boundary(self, speechRate, expected_code):
        """测试语音生成接口中 speechRate (语速) 字段的边界值"""
        payload = {
            "storyIds": ["story_001"],
            "voiceIds": ["voice_001"],
            "style": "温柔",
            "prompt": "讲睡前故事的语气",
            "speechRate": speechRate
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/audio", json=payload, headers=HEADERS)
            assert response.status_code == expected_code
            
        except requests.exceptions.ConnectionError:
            pytest.skip("⚠️ 后端本地服务未启动，跳过真实网络请求 (Mock阶段)")

    def test_audio_without_token(self):
        """安全风险拦截：测试无 Authorization 请求头时是否被拦截"""
        payload = {
            "storyIds": ["story_001"],
            "voiceIds": ["voice_001"],
            "speechRate": 1.0
        }
        headers_no_token = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(f"{BASE_URL}/api/audio", json=payload, headers=headers_no_token)
            # 预期后端网关拦截并返回 401 Unauthorized
            assert response.status_code == 401
            
        except requests.exceptions.ConnectionError:
            pytest.skip("⚠️ 后端本地服务未启动，跳过真实网络请求 (Mock阶段)")
