from sentence_transformers import SentenceTransformer


PATH = "model"
DEFAULT_MODEL = "maidalun1020/bce-embedding-base_v1"
    
    
class TextEmbeddingModel:
    """
    TextEmbeddingModel is a class for encoding text data into embedding vectors.
    
    Args:
    - model_name_or_path: str
        The model name or path for the SentenceTransformer model.
        Default is the model in "model" directory.
    
    Methods:
    - encode_text(text: str) -> list:
        Encode the input text into an embedding vector.
    """
    def __init__(self, model_name_or_path: str = PATH) -> None:
        try:
            self.model = SentenceTransformer(model_name_or_path, local_files_only=True)
            print("Embedding Model loaded successfully.")
        except:
            print("Model failed to load, will use default embedding model instead.")
            self.model = SentenceTransformer(DEFAULT_MODEL)
            print("Default model loaded successfully.")

    def encode_text(self, text: str) -> list:
        return self.model.encode(text)