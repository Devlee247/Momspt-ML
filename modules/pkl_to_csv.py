import joblib
import numpy as np
import csv

# pkl file을 open한다.
def open_pkl(file_path):
    with open(file_path, 'rb') as f:
        data = joblib.load(f)
    return data

# open한 pkl data로부터 joints3d 정보만을 추출한다
def get_joints3d_data(data):
    # data에 'joints3d'가 있는지 확인한다.
    if not data[1]['joints3d'].any():
        return False
    return data[1]['joints3d']

# (49,3)의 keypoints를 입력받아 가공하여 angle 정보로 변환한다
def keypoints_to_angle(pose_landmarks):
    assert len(pose_landmarks) == 49, 'Unexpected number of predicted pose landmarks: {}'.format(len(pose_landmarks))
    joint = np.zeros((49,3))
    for j, lm in enumerate(pose_landmarks):
        joint[j] = [lm[0], lm[1], lm[2]]

    # Compute angles between joints
    v1 = joint[[0,1,2,3,0,1,5,6,0,1,8,9,10,0,1,8,12,13], :] # [18,3]
    v2 = joint[[1,2,3,4,1,5,6,7,1,8,9,10,11,1,8,12,13,14], :]
    v = v2 - v1 # [18,3]

    # Normalize v
    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

    # Get angle using arcos of dot product
    angle = np.arccos(np.einsum('nt,nt->n',
        v[[0,1,2,4,5,6,8,9,10,11,13,14,15,16],:],
        v[[1,2,3,5,6,7,9,10,11,12,14,15,16,17],:])) # [14,]

    angle = np.degrees(angle)
    pose_angles = np.around(angle, 5).flatten().astype(np.str).tolist()
    
    return pose_angles

def list_to_csv(csv_path, data):
    csv_file = open(csv_path, 'w')
    csv_out_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for data_row in data:
        csv_out_writer.writerow(data_row)

def pkl_to_csv(DATA_PATH, CSV_OUTPUT_PATH):
    data = open_pkl(DATA_PATH)
    frames_with_pred_joints3d = get_joints3d_data(data)
    temp = []
    for pose_landmarks in frames_with_pred_joints3d:
        temp.append(keypoints_to_angle(pose_landmarks))
    list_to_csv(CSV_OUTPUT_PATH, temp)