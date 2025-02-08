import json
import httpx
from typing import Optional, List, Dict


class HuluAIAsyncClient:
    def __init__(
            self,
            token: str,
            phone: int,
            password: str,
            session_id: Optional[str] = None,
            base_url: str = "https://www.huluai.net/sqx_fast/app"
    ):
        self.base_url = base_url
        self.token = token
        self.phone = phone
        self.password = password
        self.session_id = session_id
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
            'referer': "https://www.huluai.net/",
            'token': self.token
        }
        self.client = httpx.AsyncClient()
        self.hint =  """
            请你现在化身为【全能智多星·AI超能导师】角色！(✧∇✧)╯您精通以下所有领域：
            1️⃣ Office超能专家：掌握Word排版魔法/PPT视觉设计/Excel数据炼金术，能解决从基础操作到VBA自动化等进阶问题
            2️⃣ 软硬件全栈博士：通晓计算机组成原理→硬件配置优化→操作系统内核→软件工程全流程，能用大白话解释复杂技术原理
            3️⃣ 编程宗师：Python全栈开发/Java企业级架构/Web全链路开发（前端三件套+主流框架+后端技术栈+数据库优化），擅长提供最佳实践方案
            
            【回答策略】请严格遵循：
            1️⃣ 思维宫殿：
            1. 深度解析问题本质（识别真实需求）
            2. 构建多维度知识图谱（关联相关知识）
            3. 验证方案可行性（逻辑自洽性检查）
            4. 模拟实施路径（考虑边界条件）(๑•̀ㅂ•́)و✧
            
            2️⃣ 输出规范：
            ▷ 复杂概念用生活化类比解释（如：CPU像厨房主厨，GPU像切菜团队）
            ▷ 分点说明时采用「✦关键要点→🌰生动案例→🚀实操建议」结构
            ▷ 代码示例添加详细注释，重要参数用🌟标记
            ▷ 涉及版本差异时制作对比表格
            
            3️⃣ 交互风格：
            ✅ 专业模式：技术术语准确+引用官方文档
            ✅ 萌化表达：适当使用颜文字（如复杂操作完成后加٩(ˊᗜˋ*)و）
            ✅ 风险预警：对危险操作添加⚠️警示并说明原理
            ✅ 延展学习：每个回答末提供【知识彩蛋】推荐3个相关拓展知识点
            
            4️⃣ 特殊能力：
            ✦ 硬件故障诊断树：通过症状→可能原因→排查流程图
            ✦ 代码诊疗所：输入问题代码→输出修正版+错误原因漫画图解
            ✦ Office秘技宝箱：根据使用场景推荐隐藏功能（如Excel预测工作表）
            ✦ 学习路径图：针对不同水平学习者定制技能升级路线
            
            遇到争议性问题时，请采用：
            [学术观点A]+[业界方案B]+[个人建议C]的黄金三角分析法，并标注各方案适用场景(๑¯◡¯๑)
            
            当涉及操作指导时，请提供：
            1. 准备清单（所需工具/权限/前置知识）
            2. 分步操作流程图（含各步骤预期结果）
            3. 常见翻车场景应急预案
            4. 成果验收标准
            
            最后请记得：
            ✦ 用🤔表情引入深度思考环节
            ✦ 用✨标记容易被忽略的重要细节
            ✦ 复杂流程配合emoji进度条：如「配置环境 🚧→代码调试 🔍→测试运行 🏃♂️→部署上线 🚀」
            ✦ 在安全警告处使用闪烁的⚠️符号
            
            是否准备好展现真正的技术了？请说出您的问题，让我们开启智慧之旅吧！(≧∇≦)/""".replace("\n", "").strip()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def account_login(self) -> Optional[str]:
        """账号登录并返回新token"""
        url = f"{self.base_url}/Login/registerCode"
        data = {'phone': self.phone, 'password': self.password}

        try:
            response = await self.client.post(
                url,
                headers=self.headers,
                data=data,
                timeout=10
            )
            resp_json = response.json()
            if 'token' in resp_json:
                self.token = resp_json['token']
                self.headers['token'] = self.token
                return self.token
            return None
        except httpx.RequestError as e:
            print(f"Login request failed: {str(e)}")
            return None

    async def get_all_sessions(self) -> List[Dict]:
        """获取所有会话历史"""
        url = f"{self.base_url}/user-session/findAll"

        try:
            response = await self.client.get(url, headers=self.headers)
            return response.json().get('data', [])
        except (httpx.RequestError, json.JSONDecodeError) as e:
            print(f"Get sessions failed: {str(e)}")
            return []

    async def get_session_history(self, session_id: str) -> List[Dict]:
        """获取指定会话的聊天记录"""
        url = f"{self.base_url}/user-session/search/{session_id}"

        try:
            response = await self.client.get(url, headers=self.headers)
            return response.json().get('data', {}).get('chatList', [])
        except (httpx.RequestError, json.JSONDecodeError) as e:
            print(f"Get history failed: {str(e)}")
            return []

    async def clear_session_history(self, session_id: str) -> bool:
        """清空指定会话历史"""
        url = f"{self.base_url}/user-session/clearSession/{session_id}"

        try:
            response = await self.client.delete(
                url,
                headers=self.headers,
                params={'sessionId': session_id}
            )
            return response.json().get('msg') == 'success'
        except httpx.RequestError as e:
            print(f"Clear history failed: {str(e)}")
            return False

    async def switch_module(self, session_id: str, module: str) -> bool:
        """切换会话使用的AI模块"""
        url = f"{self.base_url}/user-session/update/{session_id}"
        sys_config = {
            "model": module,
            "contextNum": 10,
            "temperature": 1,
            "maxTokens": 4096,
            "context": "open",
            "maxContextNum": 20,
            "maxTemperature": 2,
            "maxMaxTokens": 4096,
            "vip": 0
        }

        data = {
            "sessionId": session_id,
            "prefix": self.hint,
            "sessionConfig": json.dumps(sys_config)
        }

        try:
            response = await self.client.post(
                url,
                headers=self.headers,
                json=data
            )
            return response.json().get('msg') == 'success'
        except httpx.RequestError as e:
            print(f"Switch module failed: {str(e)}")
            return False

    async def ask_question(self, session_id: str, question: str) -> Optional[str]:
        """发送问题并返回chat_id"""
        url = f"{self.base_url}/user-session/chat/{session_id}"

        try:
            response = await self.client.post(
                url,
                headers=self.headers,
                data={"sessionId": session_id, "prompt": question}
            )
            result = response.json()
            if result.get('msg') == 'success':
                return result['data']['chatId']
            return None
        except httpx.RequestError as e:
            print(f"Ask question failed: {str(e)}")
            return None

    async def get_answer(self, session_id: str, question: str) -> str:
        """获取问题答案（流式响应处理）"""
        chat_id = await self.ask_question(session_id, question)
        if not chat_id:
            return ""

        url = f"{self.base_url}/user-session/chat/{session_id}/{chat_id}"
        result = ""

        try:
            async with self.client.stream(
                    'POST',
                    url,
                    headers=self.headers,
                    data={"sessionId": session_id, "chatId": chat_id}
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith('data:'):
                        try:
                            chunk = json.loads(line[5:])
                            if content := chunk.get('content'):
                                result += content
                        except json.JSONDecodeError:
                            continue
        except httpx.RequestError as e:
            print(f"Get answer failed: {str(e)}")

        return result


# 使用示例
async def main():
    sessionId = "6ca15c46903a47d4b11b5d955*****"
    token = ""
    async with HuluAIAsyncClient(
            token=token,
            phone=12345678910,
            password="password",
            session_id="7ac*********"
    ) as client:
        # 切换模型
        module_list = [
            "gpt-4o",
            "gpt-4.0-0125-preview",
            "gpt-4o-mini",
            "ERNIE-4.0-Turbo-8K",
            "ERNIE-Lite-8K"
        ]
        await client.switch_module(sessionId, module_list[0])

        # 提问并获取答案
        answer = await client.get_answer(sessionId, "请解释量子计算的基本原理")
        print(answer)

        # 获取会话历史
        history = await client.get_session_history("your_session_id")
        print(history)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())