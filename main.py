from inference import Inference
from pymilvus import MilvusClient
from embedding import TextEmbeddingModel
from openai import OpenAI


if __name__ == '__main__':
    database_client = MilvusClient("data/milvus_demo.db")
    embedding_model = TextEmbeddingModel()
    
    API_KEY = "sk-4eef92640d7d4aac9e06cf769dbd883a"
    chatting_client = OpenAI(   
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    pipe = Inference(database_client, embedding_model, chatting_client)
    
    print("请开始输入问题，输入exit退出")
    while True:
        user_clue = input()
        if user_clue == "exit":
            print("Goodbye!")
            break
        response = pipe.pipe(user_clue)
        print(response)
    