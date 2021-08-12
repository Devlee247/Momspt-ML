# MomsPT ML Part

'맘스피티'에서 체형분석을 위한 머신러닝 파트입니다.

## Language
`Python`

## Development Environment

`ubuntu 18.04` `CUDA 11.4` `CUDNN 8.2`

## Tech Stack

`python` `Blender` `flask`

## Architecture
`Web Application Server` `Docker Container Base`

서비스 서버로부터 사용자의 영상 정보가 담긴 Request가 들어오게 됩니다.<br>
해당 영상을 분석하여 데이터를 추출하고, 체형을 3D로 변환하여 파일을 Response로 제공합니다.


![image01](https://user-images.githubusercontent.com/64190071/129139159-d26cdaea-ec35-49ec-b593-5604712f19c2.png)


## Tasks
`2D Human Pose Estimation` `3D Human Pose Estimation` `3D Shape Reconstruction` `Motion Capture`

SMPL models and layer is from SMPL-X model.

<img width="300" alt="image02" src="https://user-images.githubusercontent.com/64190071/129139801-3cfea146-ef33-4f9e-92eb-a948b6f0608f.png">
<img width="173" alt="image03" src="https://user-images.githubusercontent.com/64190071/129139803-7c62227f-9499-4b9a-9b35-60a6312d7c19.png">


![](https://user-images.githubusercontent.com/64190071/129138263-a3ee6d5e-b9e2-41d4-8a38-e3a04c25b314.gif)


## Key features currently implemented

사용자로부터 제자리에서 시계방향으로 회전하는 영상을 받아 Keypoints 및 Body Shape(3D Mesh)를 추출해내고, 이를 이용하여 3D model 파일로 변환합니다.

### Extracting User's 3D Keypoints & 3D Mesh (Vertices)
  - 영상으로부터 사용자의 3D Keypoints 좌표와 3D Mesh 값을 추출
  <img height="300" alt="image02" src="https://user-images.githubusercontent.com/64190071/129141755-ab04fe4d-706f-49bc-bd75-00448ef7fd20.jpeg">


### Convert data(Keypoints & Mesh) into 3D Model
  - 사용자로부터 얻어진 데이터를 통해 3D model 파일로 변환(.glb, .fbx, .glTF)
  <img height="300" alt="image02" src="https://user-images.githubusercontent.com/64190071/129141781-f1468439-e23b-448b-b59d-fbef584021e4.gif">
