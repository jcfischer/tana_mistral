import qdrant_client
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
)
from llama_index.llms import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore

import llama_index
llama_index.set_global_handler("simple")

# re-initialize the vector store
client = qdrant_client.QdrantClient(
    path="./qdrant_data"
)
vector_store = QdrantVectorStore(client=client, collection_name="tana")

# get the LLM again
llm = Ollama(model="mistral")
service_context = ServiceContext.from_defaults(llm=llm,embed_model="local")
print("service context ready")
# load the index from the vector store
index = VectorStoreIndex.from_vector_store(vector_store=vector_store,service_context=service_context)
print("index ready")
query_engine = index.as_query_engine(similarity_top_k=20)
response = query_engine.query("Welche Themen habe ich mit Daniela besprochen.")
print(response)