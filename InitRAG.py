import pandas as pd
import boto3
import psycopg2
import json
# """ 环境和sql准备
#     -- 1. 创建一个新的数据库 (如果需要)
#     CREATE DATABASE your_faq_db;
#
#     -- 2. 连接到你新创建的数据库
#     -- 在 psql 命令行中，你可以使用: \c your_faq_db
#
#     -- 3. 在新数据库中安装 pgvector 扩展 (必须步骤)
#     -- 这需要你有相应的权限，通常是超级用户
#     CREATE EXTENSION IF NOT EXISTS vector;
#
#     -- 4. 创建用于存储 FAQ 和向量的表
#     -- Titan Embeddings G1 - Text 生成的向量维度是 1536
#     CREATE TABLE faq_embeddings (
#         id SERIAL PRIMARY KEY,
#         category TEXT,
#         question TEXT,
#         answer TEXT,
#         combined_text TEXT NOT NULL,
#         embedding vector(1536) -- 关键：使用 vector 类型，维度为 1536
#     );
# """

# --- 1. 配置信息 (已更新) ---

# AWS Bedrock 配置
BEDROCK_REGION = "us-east-1"  # 请替换为您的区域
MODEL_ID = "amazon.titan-embed-text-v1"  # <--- 已更新为 G1 Text 模型

# PostgreSQL 配置
DB_NAME = "test_rag"
DB_USER = "postgres"
DB_PASSWORD = "quanquan"
DB_HOST = "database-1.cluster-cr00ue0w4k6z.ap-southeast-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_TABLE = "faq_embeddings" # (请确保此表的 embedding 列是 vector(1536))

# Excel 文件配置
EXCEL_FILE_PATH = "C:/Users/Administrator/Desktop/FAQ.xlsx"

def get_titan_embedding(text, bedrock_client):
    """使用Titan模型为单个文本生成向量。"""
    try:
        body = json.dumps({"inputText": text})
        response = bedrock_client.invoke_model(
            body=body,
            modelId=MODEL_ID,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get("body").read())
        return response_body.get("embedding")
    except Exception as e:
        print(f"调用 Bedrock 出错: {e}")
        return None

# --- 3. 主流程 ---

def main():
    print("--- 脚本开始 ---")
    # 不再需要 register_adapter

    # 步骤 1: 读取并准备数据 (保持不变)
    print(f"正在读取和处理 Excel 文件: {EXCEL_FILE_PATH}...")
    try:
        df = pd.read_excel(EXCEL_FILE_PATH, header=1)
        df['Category'] = df['Category'].ffill()
        df.dropna(subset=['Questions'], inplace=True)

        df['Category'] = df['Category'].fillna('').astype(str)
        df['Questions'] = df['Questions'].fillna('').astype(str)
        df['Answers'] = df['Answers'].fillna('').astype(str)

        df['combined_text_for_embedding'] = df['Category'] + " - " + df['Questions'] + " - " + df['Answers']

        print(f"数据处理完成，共 {len(df)} 条有效记录。")
    except FileNotFoundError:
        print(f"错误：文件 '{EXCEL_FILE_PATH}' 未找到。")
        return
    except Exception as e:
        print(f"处理 Excel 文件时出错: {e}")
        return

    # 步骤 2: 生成向量 (保持不变)
    print(f"正在连接 AWS Bedrock (模型: {MODEL_ID}) 并生成向量...")
    bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name=BEDROCK_REGION)

    df['embedding'] = df['combined_text_for_embedding'].apply(lambda text: get_titan_embedding(text, bedrock_runtime))

    df.dropna(subset=['embedding'], inplace=True)

    print(f"向量生成完成，共获得 {len(df)} 个 1536 维向量。")

    # 步骤 3: 存入 PostgreSQL (已修改)
    print("正在连接 PostgreSQL 并写入数据...")
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        print("数据库连接成功。")

        for index, row in df.iterrows():
            # <--- 关键修改：手动将向量列表转换为字符串
            embedding_vector_as_string = str(row['embedding'])

            cur.execute(
                f"""INSERT INTO {DB_TABLE} (category, question, answer, embedding)
                   VALUES (%s, %s, %s, %s)""",
                (
                    row['Category'],
                    row['Questions'],
                    row['Answers'],
                    embedding_vector_as_string # 直接传入格式化好的字符串
                )
            )

        conn.commit()
        print(f"成功将 {len(df)} 条记录及其向量写入数据库表 '{DB_TABLE}'。")

    except psycopg2.Error as e:
        print(f"数据库操作出错: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("数据库连接已关闭。")

    print("--- 脚本执行完毕 ---")

if __name__ == "__main__":
    main()

