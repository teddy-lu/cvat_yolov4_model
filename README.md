# cvat_yolov4_model  
中文文档：[README](./README_CN.md)
___

A Semi-automatic and Automatic Annotation Toolkit for cvat 

First of all you should download the project  [CVAT](https://github.com/openvinotoolkit/cvat)  and deploy to local

Install according to the guide [CVAT && nuclio](https://openvinotoolkit.github.io/cvat/docs/administration/basics/installation/)

After the above has been completed

1. Put the training yolov4 weight file (train with darknet)「 *.weights 」and config file「 *.cfg 」into directory yolo-weight
2. Build this project into docker image and then you can use for automatic annotation

Because I created the project under the project [CVAT](https://github.com/openvinotoolkit/cvat)  so the docker image is

```shell
./deploy_cpu.sh ./openvino/omz/public/yolo-v4-tf/
```

If you find that the NODE PORT is 0, then you have to check your build if there is something wrong. Normally, there will be two output as below  
![pic1](./pic/pic1.png)

Below is an example, single and multiple product image recognition.

![pic1](./pic/pic2.gif)
![pic1](./pic/pic3.gif)
