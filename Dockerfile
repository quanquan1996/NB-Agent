# 步骤 1: 使用官方推荐的 ARM64 Python 基础镜像
FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# 步骤 2: 设置工作目录
WORKDIR /app

# 步骤 3: 复制依赖文件
COPY requirements.txt ./

# 步骤 4: 安装依赖 (关键修改在这里)
# 使用 --system 标志告诉 uv 将包安装到容器的全局环境中。
RUN uv pip install --no-cache-dir --system -r requirements.txt

# 步骤 5: 复制你的应用代码
COPY . .

# 步骤 6: 暴露端口
EXPOSE 8080
# 步骤 7: 定义启动命令
# 使用 uvicorn 来运行你的异步应用 (BedrockAgentCoreApp)。
# --host 0.0.0.0 是必须的，以便容器外部可以访问服务 [cite: 302, 397, 857]。
# 假设你的 Python 文件名为 "main.py"，并且 app 实例也叫 "app"。
CMD ["uvicorn", "AgentCoreApp:app", "--host", "0.0.0.0", "--port", "8080"]