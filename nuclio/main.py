import json
import base64
from PIL import Image
import io
from model_handler import ModelHandler
import yaml
import cv2
import numpy as np


def init_context(context):
    context.logger.info("Init context...  0%")

    # Read labels
    with open("/opt/nuclio/function.yaml", 'rb') as function_file:
        functionconfig = yaml.safe_load(function_file)

    labels_spec = functionconfig['metadata']['annotations']['spec']
    labels = {item['id']: item['name'] for item in json.loads(labels_spec)}

    # Read the DL model
    model = ModelHandler(labels)
    context.user_data.model = model

    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run yolo-v4-tf model")
    data = event.body
    # buf = io.BytesIO(base64.b64decode(data["image"]))
    # image = Image.open(buf)
    threshold = float(data.get("threshold", 0.5))
    img_decode = base64.b64decode(data["image"])
    image = cv2.imdecode(np.fromstring(img_decode, np.uint8), cv2.IMREAD_COLOR)

    results = context.user_data.model.infer(image, threshold)

    return context.Response(body=json.dumps(results), headers={},
                            content_type='application/json', status_code=200)
