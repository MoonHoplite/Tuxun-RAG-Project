from openai import OpenAI


API_KEY = "sk-4eef92640d7d4aac9e06cf769dbd883a"


client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)



def retrieve_data():
    return ""


def generate_prompt(user_clue: str, retrieved_data: str) -> str:
    prompt = f"""
    线索: "{user_clue}"

    以下是一些提示：

    {retrieved_data}

    回答:
    """
    return prompt


def generate_response(prompt: str) -> str:
    response = client.chat.completions.create(
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {"role": "system", "content": "你是一本地理百科全书"},
        {"role": "user", "content": prompt}
    ],
    )
    return response.choices[0].message.content


def pipe(user_clue: str) -> str:
    retrieved_data = retrieve_data()
    prompt = generate_prompt(user_clue, retrieved_data)
    response = generate_response(prompt)
    return response