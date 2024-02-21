import os
import shutil
import torch
import uuid

from kserve import Model, ModelServer
from kserve.errors import InvalidInput
from minio import Minio
from typing import Dict
from ultralytics import YOLO

TEMP_MODEL_DIR = "/tmp/yolov8"
E2E_EOS_ENDPOINT = "objectstore.e2enetworks.net"
INPUT_FILE_PATH = f"{TEMP_MODEL_DIR}/inputs/file." + "{ext}"
MODEL_OUTPUT_DIR = f"{TEMP_MODEL_DIR}/outputs/"
OUTPUT_FILE_PATH = f"{MODEL_OUTPUT_DIR}file.avi"
OUTPUT_OBJECT_PATH = "yolov8/outputs/{file_name}"


class Yolov8(Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False
        self.torch_device = "cuda" if torch.cuda.is_available() else "cpu"
        self.source_model = "yolov8n.pt"
        self.load()

    def load(self):
        self.model = YOLO(self.source_model)
        self.minio_client = Minio(
            E2E_EOS_ENDPOINT,
            access_key=os.getenv("access_key", ""),
            secret_key=os.getenv("secret_key", ""),
        )
        self.bucket_name = os.getenv("bucket_name", "")
        self.ready = True

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        print("payload:", payload)

        if not payload.get("input"):
            raise InvalidInput("\"input\" is required")

        # download video from eos bucket
        shutil.rmtree(TEMP_MODEL_DIR, ignore_errors=True)
        input_object_path = payload["input"]
        input_file_path = INPUT_FILE_PATH.format(ext=input_object_path.strip().split(".")[-1])
        self.minio_client.fget_object(self.bucket_name, input_object_path, input_file_path)

        # Run inference on the source
        results = self.model(
            source=input_file_path,
            stream=True,
            save=True,
            name=MODEL_OUTPUT_DIR,
        )  # generator of Results objects
        _ = list(results)

        # upload to eos bucket
        obj = self.minio_client.fput_object(
                    self.bucket_name,
                    OUTPUT_OBJECT_PATH.format(file_name=self._generate_output_file_name()),
                    OUTPUT_FILE_PATH,
                )

        shutil.rmtree(TEMP_MODEL_DIR, ignore_errors=True)

        return {"output_file_path": [obj.object_name]}

    def _generate_output_file_name(self):
        return f"output_{uuid.uuid4().hex[:8]}.avi"


if __name__ == "__main__":
    model = Yolov8("yolov8")
    ModelServer().start([model])
