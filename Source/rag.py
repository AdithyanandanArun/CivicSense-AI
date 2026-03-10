from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings
import os

index = None
PERSIST_DIR = "storage"


def build_index():
    global index

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    if os.path.exists(PERSIST_DIR):
        print("Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        print("Index loaded.")
    else:
        print("Building new index (first run, may take a while)...")

        documents = SimpleDirectoryReader(
            "schemes",
            recursive=True
        ).load_data()

        index = VectorStoreIndex.from_documents(documents)

        index.storage_context.persist(persist_dir=PERSIST_DIR)

        print("Index built and saved.")


def query_schemes(query):
    query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(query)
    return str(response)