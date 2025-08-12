
from strands import Agent
from strands.models import BedrockModel
from tools import *

# Define a custom tool as a Python function using the @tool decorator


# Create an agent with tools from the strands-tools example tools package
# as well as our custom letter_counter tool
system_prompt = """
你是一个智能助手，帮助操控智能家居以及对应场景和解决一些产品使用的故障，回答尽量详细
"""
bedrock_model = BedrockModel(
    #model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    model_id="us.amazon.nova-lite-v1:0"
)
nb_agent = Agent(model=bedrock_model,tools=[get_current_userinfo,control_curtains,search_faq,control_air_conditioner])
# nb_agent("你哈我是张三")
# nb_agent("我是谁")
#nb_agent("你好，能不能帮我打开窗帘")
#nb_agent("你好，我忘记密码了怎么办")
#nb_agent("你好，我想知道我这个Doorbell电池多久需要更换")
#nb_agent("你好，我想知道危险检测的功能怎么用")
#nb_agent("What is the Danger Alarm feature")
#nb_agent("你好，能不能帮我打开窗帘")
#nb_agent("天气太热了，帮我打开空调，风大一点")
#nb_agent("The weather is too hot. Please turn on the air conditioner for me. Make it windier.")
#nb_agent("你好，我要睡觉了")
#nb_agent("你好，我登录发现我的电话号码已经被用了")