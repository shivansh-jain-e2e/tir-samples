import os
import sys
import threading
import time
from e2enetworks.cloud import tir
from minio import Minio
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from langchain_text_splitters import SentenceTransformersTokenTextSplitter

EMBEDDING_MODEL_NAME = "e5-mistral-7b-instruct"
LOGS_BYTE_STREAM_SIZE = 1024

EOS_URL = os.getenv("EOS_URL", None)
EOS_SECRET_KEY = os.getenv("EOS_SECRET_KEY", None)
EOS_ACCESS_KEY = os.getenv("EOS_ACCESS_KEY", None)
EOS_BUCKET_NAME = os.getenv("EOS_BUCKET_NAME", None)
EOS_PREFIX = os.getenv("EOS_PREFIX", "")

TIR_API_KEY = os.getenv("TIR_API_KEY", None)
TIR_ACCESS_TOKEN = os.getenv("TIR_ACCESS_TOKEN", None)
TIR_PROJECT_ID = os.getenv("TIR_PROJECT_ID", None)
TIR_TEAM_ID = os.getenv("TIR_TEAM_ID", None)

QDRANT_HOST = os.getenv("QDRANT_HOST", None)
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", None)


def validate_variables():
    assert EOS_URL, "EOS URL is not set"
    assert EOS_SECRET_KEY, "EOS Secret Key is not set"
    assert EOS_ACCESS_KEY, "EOS Access Key is not set"
    assert EOS_BUCKET_NAME, "EOS Bucket Name is not set"

    assert TIR_API_KEY, "TIR API Key is not set"
    assert TIR_ACCESS_TOKEN, "TIR Access Token is not set"
    assert int(TIR_PROJECT_ID), "TIR Project ID is not an integer"
    assert int(TIR_TEAM_ID), "TIR Team ID is not an integer"

    assert QDRANT_HOST, "QDRANT URL is not set"
    assert QDRANT_API_KEY, "QDRANT API Key is not set"
    assert QDRANT_COLLECTION_NAME, "QDRANT Collection Name is not set"


def check_bucket_existence():
    global bucket_exists
    try:
        minio_client = Minio(
            EOS_URL,
            access_key=EOS_ACCESS_KEY,
            secret_key=EOS_SECRET_KEY,
        )
        bucket_exists = minio_client.bucket_exists(EOS_BUCKET_NAME)
    except Exception as e:
        print(e)
        bucket_exists = False


def validate_eos():
    global bucket_exists
    bucket_exists = None

    # Start a thread to check bucket existence
    bucket_check_thread = threading.Thread(target=check_bucket_existence)
    bucket_check_thread.start()

    # Wait for the thread to complete or timeout
    timeout = 15  # Timeout in seconds
    bucket_check_thread.join(timeout)

    # Check if the thread is still alive (not completed within timeout)
    if bucket_check_thread.is_alive():
        print("Took too long to check bucket existence. Terminating program.")
        # You can choose to terminate the program here if needed
        sys.exit(1)
    else:
        if bucket_exists:
            print("Bucket exists")
        else:
            assert False, "Bucket Does NOT EXIST"


def validate_qdrant():
    qdrant_client = QdrantClient(host=QDRANT_HOST, port=6333, api_key=QDRANT_API_KEY)
    collection_exists = qdrant_client.collection_exists(QDRANT_COLLECTION_NAME)
    assert collection_exists, "Collection Does NOT EXIST"


def get_object_text(minio_client: Minio, object):
    try:
        response = minio_client.get_object(bucket_name=EOS_BUCKET_NAME, object_name=object.object_name)
        log_text = ""
        for data in response.stream(amt=LOGS_BYTE_STREAM_SIZE):
            log_text = f"{log_text}{data.decode('utf-8')}"
        return log_text
    except Exception as e:
        print(f"Skipping File -> {object.object_name} -> error={e}")
    finally:
        response.close()
        response.release_conn()


def chunk_text(text: str):

    text_splitter = SentenceTransformersTokenTextSplitter()
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector(tir_client: tir.ModelAPIClient, text: str):
    data = {"prompt": text}
    response = tir_client.infer(model_name=EMBEDDING_MODEL_NAME, data=data)
    try:
        vector = response.outputs[0].data
        return vector
    except Exception as e:
        print(e)


def insert_vector(client: QdrantClient, vector: list, text: str, id: int, chunk_id: int):
    points = []

    new_id = int(time.time())
    print("id = ",new_id)
    print("count = ",id)

    point = PointStruct(
        vector=vector,
        id=new_id,
        payload={"data": text, "chunk_id": chunk_id}
    )

    points.append(point)

    try:
        res = client.upsert(collection_name=QDRANT_COLLECTION_NAME,wait=False, points=points)
        print(res)
    except Exception as e:
        print(e)


def run():

    validate_variables()
    validate_eos()
    validate_qdrant()

    minio_client = Minio(
        EOS_URL,
        access_key=EOS_ACCESS_KEY,
        secret_key=EOS_SECRET_KEY,
    )

    tir.init(api_key=TIR_API_KEY, access_token=TIR_ACCESS_TOKEN)
    tir_client = tir.ModelAPIClient(project=TIR_PROJECT_ID, team=TIR_TEAM_ID)

    qdrant_client = QdrantClient(host=QDRANT_HOST, port=6333, api_key=QDRANT_API_KEY)

    id = 1

    for object_name in minio_client.list_objects(EOS_BUCKET_NAME, recursive=True, prefix=EOS_PREFIX):

        text = get_object_text(minio_client, object_name)

        if not text:
            print("no text found")
            continue

        chunks = chunk_text(text)

        for chunk in chunks:
            chunk_id = 0

            vector = get_vector(tir_client, chunk)

            if not vector:
                print("no vector found")
                continue

            insert_vector(qdrant_client, vector, text, id, chunk_id)

            id += 1
            chunk_id += 1


if __name__ == "__main__":
    run()
