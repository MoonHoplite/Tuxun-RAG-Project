from openai import OpenAI
from embedding import TextEmbeddingModel
from pymilvus import MilvusClient


class Inference:
    def __init__(self, database_client: MilvusClient, embedding_model: TextEmbeddingModel, chatting_client: OpenAI) -> None:
        self.database_client = database_client
        self.embedding_model = embedding_model
        self.chatting_client = chatting_client
        print("Model loaded successfully!")

    def retrieve_data(self, user_clue: str) -> str:
        query_vector = self.embedding_model.encode_text(user_clue)

        res = self.database_client.search(
            collection_name="Tuxun",
            data=[query_vector],
            top_k=5,
            output_fields=['id', 'text', 'country'],
        )
        
        combined_hints = []
        for hints in res[0]:
            combined_hints.append(f"国家: {hints['entity']['country']} 特征: {hints['entity']['text']}")
        
        return "\n".join(combined_hints)


    def generate_prompt(self, user_clue: str, retrieved_data: str) -> str:
        prompt = f"""
        问题: "{user_clue}"

        如果用户询问的问题与国家猜测无关，请忽略以下内容。
        如果用户询问了有关国家猜测的问题，请参考以下内容回答。可能有干扰信息，请明察秋毫。以下信息不是用户提供给你的，而是系统提供给你的。

        {retrieved_data}

        回答:
        """
        return prompt


    def generate_response(self, prompt: str) -> str:
        response = self.chatting_client.chat.completions.create(
        model="qwen-max", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
            {"role": "system", "content": "你是一位全能的助手"},
            {"role": "user", "content": prompt}
        ],
        )
        return response.choices[0].message.content


    def pipe(self, user_clue: str) -> str:
        retrieved_data = self.retrieve_data(user_clue)
        prompt = self.generate_prompt(user_clue, retrieved_data)
        response = self.generate_response(prompt)
        return response
