import json

import psycopg2
from strands import Agent, tool
import boto3

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

@tool(description="Get the current user body history information with weight and fat percentage", name="get_current_userinfo")
def get_current_user_history_info():
    user_health_info = {
        "weight_history": [
            {
                "date": "2025-07-01",
                "weight_kg": 78.0
            },
            {
                "date": "2025-07-15",
                "weight_kg": 77.1
            },
            {
                "date": "2025-08-01",
                "weight_kg": 76.2
            },
            {
                "date": "2025-08-10",
                "weight_kg": 75.5
            },
            {
                "date": "2025-08-16",
                "weight_kg": 75.7
            },
            {
                "date": "2025-08-20",
                "weight_kg": 75.8
            },
            {
                "date": "2025-08-24",
                "weight_kg": 75.9
            },
            {
                "date": "2025-08-31",
                "weight_kg": 76.0
            },
            {
                "date": "2025-09-05",
                "weight_kg": 75.6
            },
            {
                "date": "2025-09-10",
                "weight_kg": 75.6
            },
            {
                "date": "2025-09-15",
                "weight_kg": 75.0
            },
            {
                "date": "2025-09-22",
                "weight_kg": 74.8
            },
            {
                "date": "2025-09-28",
                "weight_kg": 74.9
            },
            {
                "date": "2025-10-01",
                "weight_kg": 74.9
            },
            {
                "date": "2025-10-06",
                "weight_kg": 74.4
            },
            {
                "date": "2025-10-13",
                "weight_kg": 74.2
            },
            {
                "date": "2025-10-17",
                "weight_kg": 74.2
            },
            {
                "date": "2025-10-23",
                "weight_kg": 74.3
            },
            {
                "date": "2025-10-28",
                "weight_kg": 74.4
            },
            {
                "date": "2025-11-04",
                "weight_kg": 74.3
            }
        ],
        "body_fat_history": [
            {
                "date": "2025-07-01",
                "percentage": 20.1
            },
            {
                "date": "2025-07-15",
                "percentage": 19.5
            },
            {
                "date": "2025-08-01",
                "percentage": 18.8
            },
            {
                "date": "2025-08-10",
                "percentage": 18.2
            },
            {
                "date": "2025-08-16",
                "percentage": 18.1
            },
            {
                "date": "2025-08-20",
                "percentage": 18.0
            },
            {
                "date": "2025-08-24",
                "percentage": 17.9
            },
            {
                "date": "2025-08-31",
                "percentage": 17.6
            },
            {
                "date": "2025-09-05",
                "percentage": 17.6
            },
            {
                "date": "2025-09-10",
                "percentage": 17.4
            },
            {
                "date": "2025-09-15",
                "percentage": 17.5
            },
            {
                "date": "2025-09-22",
                "percentage": 17.4
            },
            {
                "date": "2025-09-28",
                "percentage": 17.5
            },
            {
                "date": "2025-10-01",
                "percentage": 17.4
            },
            {
                "date": "2025-10-06",
                "percentage": 17.3
            },
            {
                "date": "2025-10-13",
                "percentage": 17.1
            },
            {
                "date": "2025-10-17",
                "percentage": 17.1
            },
            {
                "date": "2025-10-23",
                "percentage": 17.0
            },
            {
                "date": "2025-10-28",
                "percentage": 16.7
            },
            {
                "date": "2025-11-04",
                "percentage": 16.5
            }
        ]
    }

    # 你可以这样访问其中的信息
    # print(f"当前体重: {user_health_info['current_weight_kg']} kg")
    # print(f"喜欢的食物: {', '.join(user_health_info['food_likes'])}")
    return user_health_info

# 获取当前用户信息
@tool(description="Get the current user body information", name="get_current_userinfo")
def get_current_userinfo():
    """

    """
    user_health_info = {
        # 基本身体数据 (Basic Body Data)
        "height_cm": 175,  # 身高 (厘米)
        "current_weight_kg": 75.5,  # 当前体重 (公斤)
        "target_weight_kg": 70.0,  # 目标体重 (公斤)
        "current_body_fat_percentage": 18.2,  # 当前体脂率 (%)
        "target_body_fat_percentage": 15.0,  # 目标体脂率 (%)

        # 历史数据记录 (Historical Data Records)
        "weight_history": [
            {"date": "2025-07-01", "weight_kg": 78.0},
            {"date": "2025-07-15", "weight_kg": 77.1},
            {"date": "2025-08-01", "weight_kg": 76.2},
            {"date": "2025-08-10", "weight_kg": 75.5},
        ],
        "body_fat_history": [
            {"date": "2025-07-01", "percentage": 20.1},
            {"date": "2025-07-15", "percentage": 19.5},
            {"date": "2025-08-01", "percentage": 18.8},
            {"date": "2025-08-10", "percentage": 18.2},
        ],

        # 饮食偏好与限制 (Dietary Preferences and Restrictions)
        "dietary_plan": "低碳水化合物饮食",  # 遵循的饮食计划 (e.g., "均衡饮食", "生酮饮食")
        "daily_calorie_goal": 2000,  # 每日卡路里目标 (千卡)
        "macronutrient_targets": { # 宏量营养素目标
            "protein_g": 150,  # 蛋白质 (克)
            "carbs_g": 100,    # 碳水化合物 (克)
            "fat_g": 88        # 脂肪 (克)
        },
        "food_likes": ["鸡胸肉", "西兰花", "三文鱼", "牛油果", "鸡蛋"], # 喜欢的食物
        "food_dislikes": ["肥肉", "芹菜", "甜腻的糕点"], # 不喜欢的食物
        "allergies_or_intolerances": ["乳糖不耐受"], # 过敏或不耐受
        "meal_preferences": { # 餐食偏好
            "meals_per_day": 3, # 每日餐数
            "preferred_meal_time": ["08:00", "12:30", "18:30"], # 偏好用餐时间
            "snack_preference": True, # 是否吃零食
            "preferred_snacks": ["坚果", "酸奶"] # 偏好的零食
        }
    }

    # 你可以这样访问其中的信息
    # print(f"当前体重: {user_health_info['current_weight_kg']} kg")
    # print(f"喜欢的食物: {', '.join(user_health_info['food_likes'])}")
    return user_health_info


# 获取用户历史对话信息
@tool(description="Get the user's history of conversations", name="get_user_history")
def get_user_history():
    user_history = [
        "你好，我想咨询一下家用安防摄像头。",
        "您好！请问您是想安装在室内还是室外？对功能有什么具体要求吗？",
        "主要装在室外，大门口和后院。夜视功能要好一些，最好能连接手机随时查看。",
        "明白了。那您对存储方式有偏好吗？比如云存储或者本地SD卡存储？",
        "我不太想用云存储，希望能用SD卡存在本地。",
        "好的。根据您的需求，市面上大部分主流品牌的户外摄像头都符合要求。您可以关注一下它们的人形侦测和警报推送功能，这个对家庭安防很实用。",
        "人形侦测和普通的移动侦测有什么区别？",
        "人形侦测可以过滤掉由光线变化、宠物或飞虫等引起的误报，只有在检测到人形时才会向您的手机发送警报，准确性更高。",
        "这个功能好，谢谢你的建议！",
    ]


# 查询摄像头产品的qa文档，查询故障如何解决
@tool(description="Query the Q&A document of the camera product", name="query_camera_qa")
def query_camera_qa(question: str):
    print("question:", question)
    """
    :param question: The question to ask
    :return: The answer to the question
    """
    qa_doc = [
        "Q: 摄像头是否可以安装在室内？",
        "A: 摄像头可以安装在室内，但是建议不要安装在 occupied area 中，以免产生unnecessary noise。",
        "Q: 摄像头是否可以安装在室外？",
        "A: 摄像头可以安装在室外，但是建议不要安装在occupied area 中，以免产生unnecessary noise。",
        "Q: 摄像头是否可以连接手机？",
        "A: 摄像头可以连接手机，但是建议不要使用手机作为主控设备，以免产生unnecessary noise。",
        "Q: 摄像头是否可以存储？",
        "A: 摄像头可以存储，但是建议不要使用SD卡存储，以免产生unnecessary noise。",
        "Q: 摄像头是否可以进行人形侦测？",
        "A: 摄像头可以进行人形侦测，但是建议不要使用手机作为主控设备，以免产生unnecessary noise。",
        "Q: 摄像头是否可以进行移动侦测？",
        "A: 摄像头可以进行移动侦测，但是建议不要使用手机作为主控设备，以免产生unnecessary noise。",
        "Q: 摄像头是否可以进行报警推送？",
        "A: 摄像头可以进行报警推送，但是建议不要使用手机作为主控设备，以免产生unnecessary noise。",
        "Q: 摄像头经常发出噪音如何解决？",
        "A: 摄像头经常发出噪音，可以通过以下方式来解决：",
        "1. 减少使用手机作为主控设备。",
        "2. 减少使用SD卡存储。",
        "3. 减少使用移动侦测。",
        "4. 减少使用人形侦测。",
        "5. 减少使用移动侦测。",
        "6. 减少使用报警推送。",
        "7. 减少使用SD卡存储。",
        "8. 减少使用移动侦测。",
        "9. 减少使用人形侦测。",
    ]
    return qa_doc

# 操作空调，可以传入开关 、温度、风速、模式
@tool(description="Control the air conditioner,action:on/off,temperature:18~32,wind_speed:low/medium/high,mode:cool/heat/dry/ventilate", name="control_air_conditioner")
def control_air_conditioner(action: str, temperature: int , wind_speed: str , mode: str):
    """
    :param action: The action to perform (on, off)
    :param temperature: The temperature to set (in degrees Celsius)
    :param wind_speed: The wind speed to set (low, medium, high)
    :param mode: The mode to set (cool, heat, dry, ventilate)
    :return: The result of the action
    """
    if action == "on":
        print("Mock action Turning on the air conditioner...")
        print(f"Setting temperature to {temperature}°C...")
        print(f"Setting wind speed to {wind_speed}...")
        print(f"Setting mode to {mode}...")
        return "The air conditioner is now on."
    elif action == "off":
        print("Mock action Turning off the air conditioner...")
        return "The air conditioner is now off."
    else:
        return "Invalid action.try again"

# 操作窗帘开关
@tool(description="Control the curtains,action:open/close", name="control_curtains")
def control_curtains(action: str):
    """
    :param action: The action to perform (open, close, stop)
    :return: The result of the action
    """
    if action == "open":
        print("Mock action Opening the curtains...")
        return "The curtains are now open."
    elif action == "close":
        print("Mock action Closing the curtains...")
        return "The curtains are now closed."
    else:
        return "Invalid action.try again"

@tool(
    description="从图片记录食物的热量，需要根据图片来预估食物的重量、种类，和食物的蛋白质、脂肪、碳水化合物的百分比含量。",
    name="record_meal_calories_from_image"
)
def record_meal_calories_from_image(
        food_description: str,
        estimated_weight_g: float,
        protein_percentage: float,
        carbohydrate_percentage: float,
        fat_percentage: float
) -> str:
    """
    根据AI从图片识别出的食物描述、预估总重量和宏量营养素百分比，计算并记录热量。

    :param food_description: AI对食物的文字描述 (例如："一份鸡胸肉沙拉")。
    :param estimated_weight_g: 食物总重量的预估值（克）。
    :param protein_percentage: 蛋白质占总重量的百分比 (例如: 15.5 表示 15.5%)。
    :param carbohydrate_percentage: 碳水化合物占总重量的百分比。
    :param fat_percentage: 脂肪占总重量的百分比。
    :return: 包含记录详情的总结字符串。
    """
    # --- 1. 输入验证 ---
    total_percentage = protein_percentage + carbohydrate_percentage + fat_percentage
    # --- 2. 计算每种营养素的克数 ---
    protein_grams = estimated_weight_g * (protein_percentage / 100)
    carbohydrate_grams = estimated_weight_g * (carbohydrate_percentage / 100)
    fat_grams = estimated_weight_g * (fat_percentage / 100)

    # --- 3. 计算总热量 ---
    # 1克蛋白质 ≈ 4千卡, 1克碳水 ≈ 4千卡, 1克脂肪 ≈ 9千卡
    total_calories = (protein_grams * 4) + (carbohydrate_grams * 4) + (fat_grams * 9)

    # --- 4. 模拟后台记录操作 ---
    print("--- 模拟后台记录操作 (Mock Action: Recording Meal from Image) ---")
    print(f"食物描述 (Food Description): {food_description}")
    print(f"食物总重量 (Total Weight): {estimated_weight_g:.1f}g")
    print(f"计算出的蛋白质克数 (Calculated Protein): {protein_grams:.1f}g")
    print(f"计算出的碳水克数 (Calculated Carbs): {carbohydrate_grams:.1f}g")
    print(f"计算出的脂肪克数 (Calculated Fat): {fat_grams:.1f}g")
    print(f"计算出的总热量 (Calculated Total Calories): {total_calories:.1f} kcal")
    print("--------------------------------------------------")

    # --- 5. 生成并返回总结报告 ---
    summary_report = (
        f"已记录 '{food_description}'：\n"
        f"总重约 {estimated_weight_g:.0f}g，"
        f"热量约 {total_calories:.0f}大卡。\n"
        f"营养成分：蛋白质 {protein_grams:.1f}g, 碳水 {carbohydrate_grams:.1f}g, 脂肪 {fat_grams:.1f}g。"
    )

    return summary_report

# 在知识库搜索
@tool(description="Search the knowledge base ", name="search_bedrock_knowledge_base")
def search_bedrock_knowledge_base(
        query: str
):
    knowledge_base_id = "XEQRSKOZ99"
    number_of_results = 5
    region_name = "us-west-2"
    # 1. 创建 Bedrock Agent Runtime 客户端
    client = boto3.client(
        "bedrock-agent-runtime",
        region_name=region_name
    )

    # 2. 调用 retrieve API
    response = client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={
            'text': query
        },
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': number_of_results
            }
        }
    )

    # 3. 解析并格式化返回结果
    retrieval_results = response.get('retrievalResults', [])

    formatted_results = []
    for result in retrieval_results:
        formatted_results.append({
            # 知识片段的文本内容
            'text': result['content']['text'],
            # 相关性分数（0到1之间，越高越相关）
            'score': result['score'],
            # 知识片段的源文件位置（例如 S3 URI）
            'source_uri': result.get('location', {}).get('s3Location', {}).get('uri')
        })

    return formatted_results

# print(search_bedrock_knowledge_base("s3知识库"))

@tool(
    name="search_faq_database",
    description="当用户询问有关产品问题，包含Hello Doorbell App, Account, Camera & Recording, Wifi或任何常见问题时使用此工具。它会从FAQ知识库中搜索最相关的答案。输入应为一个清晰的问题。"
)
def search_faq(query: str, top_k: int = 5):
    """
    此函数接收一个用户查询，将其向量化，然后在PostgreSQL数据库中
    执行向量相似度搜索，返回最相关的top_k条FAQ。

    :param query: 用户的自然语言查询字符串。
    :param top_k: 希望返回的最相关结果的数量，默认为3。
    :return: 一个格式化的字符串，包含找到的FAQ；如果未找到则返回提示信息。
    """
    print(f"🔍 接收到查询: '{query}',topk:'{top_k}'正在执行RAG检索...")

    # 步骤 A: 向量化查询
    print("   - 步骤1: 正在将查询向量化...")
    try:
        bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name=BEDROCK_REGION)
        query_embedding = get_titan_embedding(query, bedrock_runtime)
        if query_embedding is None:
            return "错误：查询向量化失败。"
    except Exception as e:
        return f"错误：连接或调用Bedrock时出错 - {e}"

    # 步骤 B: 在数据库中进行向量搜索
    print("   - 步骤2: 正在数据库中执行向量搜索...")
    conn = None
    results = []
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # pgvector 使用 <=> 操作符计算余弦距离
        # 我们需要将Python列表转换为字符串格式 '[1,2,3]'
        embedding_string = str(query_embedding)

        cur.execute(
            f"""SELECT category, question, answer FROM {DB_TABLE}
               ORDER BY embedding <=> %s
               LIMIT %s""",
            (embedding_string, top_k)
        )
        results = cur.fetchall()

    except psycopg2.Error as e:
        print(f"   - 数据库错误: {e}")
        return "错误：查询数据库时发生错误。"
    finally:
        if conn:
            conn.close()

    # 步骤 C: 格式化并返回结果
    print("   - 步骤3: 正在格式化输出结果...")
    if not results:
        print("   - 未找到相关结果。")
        return "抱歉，在知识库中没有找到与您问题直接相关的信息。"

    formatted_output = "根据知识库，找到了以下相关信息：\n\n"
    for i, (category, question, answer) in enumerate(results, 1):
        formatted_output += f"--- 相关条目 {i} ---\n"
        formatted_output += f"【分类】: {category}\n"
        formatted_output += f"【相关问题】: {question}\n"
        formatted_output += f"【答案】: {answer}\n\n"

    print("✅ RAG检索完成。")
    print(formatted_output)
    return formatted_output.strip()

#print(search_faq("电池续航能力？"))