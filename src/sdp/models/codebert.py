import os
import pickle
from typing import Dict, List, Optional

import numpy as np
import torch
from tqdm import tqdm
from transformers import RobertaModel, RobertaTokenizer
from openai import OpenAI
import tiktoken


class CodeBERTEmbedder:
    """CodeBERT embedding helper for chunked Java source code."""

    def __init__(self, model_name: str = "microsoft/codebert-base", device: Optional[str] = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = RobertaTokenizer.from_pretrained(model_name)
        self.model = RobertaModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def chunk_text_by_substring(self, text: str, max_len: int = 512, stride: int = 256):
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + max_len
            chunk_text = " ".join(words[start:end])
            encoded = self.tokenizer(
                chunk_text,
                truncation=True,
                max_length=max_len,
                padding="max_length",
                return_tensors="pt",
            )
            chunks.append(encoded)
            start += stride
        return chunks

    @torch.no_grad()
    def compute_chunk_embeddings(self, texts: List[str], save_path: Optional[str] = None) -> List[List[np.ndarray]]:
        all_chunks: List[List[np.ndarray]] = []
        for text in tqdm(texts, desc="Computing CodeBERT chunk embeddings"):
            chunks = self.chunk_text_by_substring(text)
            chunk_vecs = []
            for ch in chunks:
                inputs = {k: v.to(self.device) for k, v in ch.items()}
                outputs = self.model(**inputs)
                hidden_states = outputs.last_hidden_state
                chunk_vecs.append(hidden_states.squeeze(0).cpu().numpy())
            all_chunks.append(chunk_vecs)

        if save_path is not None:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                for chunk_list in tqdm(all_chunks, desc="Saving CodeBERT chunks"):
                    pickle.dump(chunk_list, f)
        return all_chunks

    def get_all_chunks(self, texts: List[str], chunk_emb_path: str) -> List[List[np.ndarray]]:
        if os.path.exists(chunk_emb_path):
            all_chunks = []
            with open(chunk_emb_path, "rb") as f:
                while True:
                    try:
                        all_chunks.append(pickle.load(f))
                    except EOFError:
                        break
            return all_chunks
        return self.compute_chunk_embeddings(texts, chunk_emb_path)

    @staticmethod
    def pool_embeddings(
        chunk_vecs: List[np.ndarray],
        token_pool: str = "cls",
        chunk_pool: str = "avg",
    ) -> np.ndarray:
        token_vecs = []
        for h in chunk_vecs:
            h_tensor = torch.tensor(h).unsqueeze(0)
            if token_pool == "cls":
                vec = h_tensor[:, 0, :]
            elif token_pool == "mean":
                vec = h_tensor.mean(dim=1)
            elif token_pool == "max":
                vec, _ = h_tensor.max(dim=1)
            else:
                raise ValueError("token_pool must be one of cls, mean, max")
            token_vecs.append(vec.squeeze(0).numpy())

        token_vecs = np.stack(token_vecs, axis=0)
        if chunk_pool == "avg":
            return np.mean(token_vecs, axis=0)
        if chunk_pool == "max":
            return np.max(token_vecs, axis=0)
        if chunk_pool == "min":
            return np.min(token_vecs, axis=0)
        raise ValueError("chunk_pool must be one of avg, max, min")

    @staticmethod
    def prepare_dataset_embeddings(
        all_chunks: List[List[np.ndarray]],
        token_pool: str = "cls",
        chunk_pool: str = "avg",
    ) -> np.ndarray:
        return np.vstack([
            CodeBERTEmbedder.pool_embeddings(chunks, token_pool=token_pool, chunk_pool=chunk_pool)
            for chunks in all_chunks
        ])


def chunk_text_tokenwise(text: str, max_tokens: int = 8192, model_name: str = "text-embedding-3-small") -> List[str]:
    enc = tiktoken.encoding_for_model(model_name)
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunks.append(enc.decode(chunk_tokens))
    return chunks


def get_openai_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    batch_size: int = 32,
) -> List[np.ndarray]:
    client = OpenAI(api_key=api_key, base_url=base_url) if api_key else OpenAI()
    all_embeddings: List[np.ndarray] = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.embeddings.create(model=model, input=batch)
        for item in response.data:
            all_embeddings.append(np.array(item.embedding, dtype=np.float32))

    return all_embeddings


def get_all_openai_chunks(
    texts: List[str],
    batch_size: int = 32,
    max_tokens: int = 8192,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> List[List[np.ndarray]]:
    all_chunks: List[List[np.ndarray]] = []
    for text in texts:
        chunk_texts = chunk_text_tokenwise(text, max_tokens=max_tokens, model_name=model)
        embeddings = get_openai_embeddings(chunk_texts, model=model, api_key=api_key, base_url=base_url, batch_size=batch_size)
        all_chunks.append(embeddings)
    return all_chunks
