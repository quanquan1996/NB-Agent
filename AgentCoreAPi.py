from strands import Agent
from bedrock_agentcore import BedrockAgentCoreApp

# 1. 导入 CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

from NBAgent import nb_agent

app = BedrockAgentCoreApp()

# 2. 添加 CORS 中间件到你的 app
#    这应该在定义路由/入口点之前完成
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的请求。为了安全，生产环境中应替换为你的前端域名，例如 ["http://localhost:3000", "https://your-frontend-domain.com"]
    allow_credentials=True,  # 允许发送 cookies
    allow_methods=["*"],  # 允许所有 HTTP 方法 (GET, POST, etc.)
    allow_headers=["*"],  # 允许所有请求头
)


@app.entrypoint
async def agent_invocation(payload):
    """Handler for agent invocation"""
    user_message = payload.get(
        "prompt", "No prompt found in input, please guide customer to create a json payload with prompt key"
    )
    #return {"result":nb_agent(user_message).message}
    stream = nb_agent.stream_async(user_message)
    async for event in stream:
        print(event)
        yield (event)

if __name__ == "__main__":
    app.run()