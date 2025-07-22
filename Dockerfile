# 步骤 1: 使用官方推荐的 ARM64 Python 基础镜像
# 这确保了与 Amazon Bedrock AgentCore Runtime 的兼容性 [cite: 878, 895, 1008]。
FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# 步骤 2: 设置工作目录
WORKDIR /app

# 步骤 3: 复制依赖文件
# 将你的 requirements.txt 文件复制到容器中。
COPY requirements.txt ./

# 步骤 4: 安装依赖
# 使用 uv 高效地安装所有必要的 Python 包。
RUN pip install --no-cache-dir -r requirements.txt

# 步骤 5: 复制你的应用代码
# 将你项目中的所有文件（包括你的主应用文件和 NBAgent 模块）复制到容器中。
COPY . .

# 步骤 6: 暴露端口
# AgentCore Runtime 要求应用在 8080 端口上监听 HTTP 请求 [cite: 303, 617, 857, 1011]。
EXPOSE 8080

# 步骤 7: 定义启动命令
# 使用 uvicorn 来运行你的异步应用 (BedrockAgentCoreApp)。
# --host 0.0.0.0 是必须的，以便容器外部可以访问服务 [cite: 302, 397, 857]。
# 假设你的 Python 文件名为 "main.py"，并且 app 实例也叫 "app"。
CMD ["uvicorn", "AgentCoreApp:app", "--host", "0.0.0.0", "--port", "8080"]