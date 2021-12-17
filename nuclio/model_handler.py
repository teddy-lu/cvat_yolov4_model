# Copyright (C) 2020-2021 Intel Corporation
#
# SPDX-License-Identifier: MIT

import os
import numpy as np

import cv2


class ModelHandler:
    def __init__(self, labels):
        base_dir = os.path.abspath(os.environ.get("MODEL_PATH",
                                                  "/opt/nuclio/yolo-weight"))
        self.model_cfg = os.path.join(base_dir, "yolo-obj.cfg")
        self.model_weight = os.path.join(base_dir, "yolo-obj_best.weights")
        self.labels = labels

    def infer(self, image, threshold):

        (H, W) = image.shape[:2]

        net = cv2.dnn.readNetFromDarknet(cfgFile=self.model_cfg, darknetModel=self.model_weight)
        ln = np.array(net.getLayerNames())
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
        print(ln)

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        boxes = []
        confidences = []
        classIDs = []
        # 置信度大于.5的边界框数据保留下来
        # confidence_thre = 0.5
        # 非最大抑制的阈值。
        nms_thre = 0.3

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > threshold:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, threshold, nms_thre)

        listLayer = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                listLayer.append({
                    "confidence": str(confidences[i]),
                    "label": self.labels[classIDs[i]],
                    "points": [int(x), int(y), int(x + w), int(y + h)],
                    "type": "rectangle",
                })

        return listLayer
