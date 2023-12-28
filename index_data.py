from pathlib import Path
import argparse
import requests
import tempfile
import os

import qdrant_client
from llama_index.llms import Ollama
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    download_loader,
)

def load_topic_index(filename:str):
    # load the JSON off disk
    json_reader = download_loader("JSONReader")
    loader = json_reader()
    documents = loader.load_data(Path(filename))

    # initialize the vector store
    client = qdrant_client.QdrantClient(
        path="./qdrant_data"
    )
    vector_store = QdrantVectorStore(client=client, collection_name="tana")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    print("Storage context ready")

    # initialize the LLM
    llm = Ollama(model="mistral")
    service_context = ServiceContext.from_defaults(llm=llm,embed_model="local")
    print("Service context ready")

    # create the index; this will embed the documents and store them in the vector store
    #TODO: ensure we are upserting by topic id, otherwise we will have duplicates
    # and will have to drop the index first
    index = VectorStoreIndex.from_documents(documents,service_context=service_context,storage_context=storage_context)
    print("Index ready")
    return index
 

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Specify a file name', required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    filename = args.file
    if not filename:
        filename = "data/tana_dump.json"

    print("Sending data to topic dumper API...")

    # throw Tana json export at the topic dumper API
    url = "http://localhost:8000/topics"

    headers = {'Content-type': 'application/json'}
    with open(filename, 'rb') as f:
        response = requests.post(url, data=f, headers=headers)

    if response.status_code != 200:
        print("Error sending data to topic dumper API:")
        print(response.text)
        exit(1)

    # save output to a temporary file
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'topics.json')
        # use path
        with open(path, "w") as f:
            f.write(response.text)
        
        index = load_topic_index(path)

    # query the index to test liveness
    query_engine = index.as_query_engine()
    response = query_engine.query("What do you know about Tana?")
    print(response)
