from strands import Agent
# 正确的方式
from strands.types.content import ContentBlock
from bedrock_agentcore import BedrockAgentCoreApp
from fastapi.middleware.cors import CORSMiddleware
import base64  # 2. 导入 base64 库用于解码

from NBAgent import nb_agent

app = BedrockAgentCoreApp()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.entrypoint
async def agent_invocation(payload: dict):
    """
    处理Agent调用的句柄，现已支持文本、图片和视频输入。

    为了传递多模态内容，payload应包含一个 "content" 键，其值为一个列表，
    列表中的每一项都是一个独立的 ContentBlock。

    示例 Payload:
    {
      "content": [
        {"text": "请描述这张图片和这个视频"},
        {"image": {"format": "png", "source": {"bytes": "base64_encoded_string_goes_here"}}},
        {"video": {"format": "mp4", "source": {"bytes": "base64_encoded_string_goes_here"}}}
      ]
    }
    """

    # 3. 准备一个列表来构建 Agent 的输入
    agent_input: list[ContentBlock] = []

    # 4. 检查新的 "content" 键，用于处理多模态输入
    if "content" in payload and isinstance(payload.get("content"), list):
        processed_content = []
        for block in payload["content"]:
            # 如果是图片且字节数据是Base64字符串，则进行解码
            if "image" in block and isinstance(block.get("image", {}).get("source", {}).get("bytes"), str):
                try:
                    block["image"]["source"]["bytes"] = base64.b64decode(block["image"]["source"]["bytes"])
                except (ValueError, TypeError):
                    # 如果解码失败，可以返回错误或跳过
                    print(f"Warning: Failed to decode base64 for image block: {block}")
                    continue

            # 如果是视频且字节数据是Base64字符串，则进行解码
            if "video" in block and isinstance(block.get("video", {}).get("source", {}).get("bytes"), str):
                try:
                    block["video"]["source"]["bytes"] = base64.b64decode(block["video"]["source"]["bytes"])
                except (ValueError, TypeError):
                    print(f"Warning: Failed to decode base64 for video block: {block}")
                    continue

            processed_content.append(block)

        agent_input = processed_content

    # 5. 为了向后兼容，继续支持旧的 "prompt" 文本输入格式
    elif "prompt" in payload:
        agent_input = [{"text": str(payload["prompt"])}]

    # 6. 将构建好的输入传递给 Agent
    # nb_agent.stream_async 可以同时接受字符串和 ContentBlock 列表
    stream = nb_agent.stream_async(agent_input)
    async for event in stream:
        print(event)
        yield (event)

if __name__ == "__main__":
    app.run()