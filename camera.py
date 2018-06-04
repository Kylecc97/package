from skimage.feature import hog
import cv2
import dlib
import sys
import os
import numpy as np
from sklearn.externals import joblib
import xgboost as xgb

current_dir = "/home/lyx/Documents/face_recognition/GUI"
data_dict = dict()
validation_dict = dict()
test_dict = dict()

sys.path.append("/users/lyx/PycharmProjects/face/")
expression_dic = {'0':'angry','1':'disgust','2':'fear','3':'happy','4':'neutral','5':'sad','6':'surprise'}
current_dir = "/home/lyx/Documents/face_recognition/GUI"


image_height = 48
image_width = 48
img_dir = current_dir + '/test/'
predict_path = "/home/lyx/Documents/face_recognition/background/shape_predictor_68_face_landmarks.dat"

images = []
labels_list = []
landmarks = []
hog_features = []
hog_images = []
nb_images_per_label = list(np.zeros(7))
predictor = dlib.shape_predictor(predict_path)

def get_landmarks(image, rects):
    return np.matrix([[p.x, p.y] for p in predictor(image, rects[0]).parts()])


def get_npy():
    for file in os.listdir(img_dir):
        file_path = img_dir + file
        image = cv2.imread(file_path)
        if image is None:
            continue
        image = cv2.resize(image, (48, 48))
        image = image[:, :, 0]
        features, hog_image = hog(image, orientations=7, pixels_per_cell=(16, 16),
                                  cells_per_block=(1, 1), visualise=True)
        if features is None:
            continue
        images.append(image)
        hog_features.append(features)
        hog_images.append(hog_image)
        face_rects = [dlib.rectangle(left=1, top=1, right=47, bottom=47)]
        face_landmarks = get_landmarks(image, face_rects)
        landmarks.append(face_landmarks)


    print(hog_features)
    print(landmarks)

    np.save(current_dir + '/hog_test' + '.npy', hog_features)
    np.save(current_dir + '/landmarks_test' + '.npy', landmarks)

def evaluate(model, X, Y,flag):
    predicted_Y = model.predict(X)
    print(predicted_Y)
    if flag:
        for i in predicted_Y:
            if int(i) == 0:
                print("表情为正常")
            elif int(i) == 1:
                print("表情为开心")
            elif int(i) == 2:
                print("表情为伤心")
            elif int(i) == 3:
                    print("表情为惊讶")
            elif int(i) == 4:
                print("表情为恐惧")
            elif int(i) == 5:
                print("表情为厌恶")
            else:
                print("表情为生气")




def operate_img(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
    #print(img.shape)
    img = np.asanyarray(img, np.float32)
    # print(img.shape)
    img = img[:, :]
    # print(x.shape)
    img = np.reshape(img, [-1, 2304])
    get_npy()
    model = joblib.load("/home/lyx/Documents/face_recognition/background/xg_model.bin")
    test_dict['X'] = np.load(current_dir + '/landmarks_test' + '.npy')
    test_dict['X'] = np.array([x.flatten() for x in test_dict['X']])

    test_dict['X'] = np.concatenate((test_dict['X'], np.load(current_dir + '/hog_test' + '.npy')), axis=1)
    test_dict['Y'] = np.load(current_dir + '/labels_test' + '.npy')
    test = test_dict
    test['X'] = xgb.DMatrix(test['X'])
    test_accuracy = evaluate(model, test['X'], test['Y'], True)



def video_face_recognition(camera_num=0):

    # landmark  dat
    predictor_path = "/home/lyx/Documents/face_recognition/background/shape_predictor_68_face_landmarks.dat"
    # 初始化landmark
    predictor = dlib.shape_predictor(predictor_path)
    # 初始化dlib人脸检测器
    detector = dlib.get_frontal_face_detector()
    # 初始化显示窗口
    win = dlib.image_window()
    # opencv加载视频文件
    #cap = cv2.VideoCapture('xxx.mp4')
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("Unable to connect to camera !")
    #model = face_expression.init()
    while cap.isOpened():
        ret, cv_img = cap.read()
        if cv_img is None:
            break
        # RGB TO BGR
        img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        #print(img)
        dets = detector(img, 0)
        #print("Number of faces detected: {}".format(len(dets)))
        shapes = []
        for i, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                i, d.left(), d.top(), d.right(), d.bottom()))
            shape = predictor(img, d)
            shapes.append(shape)
        # Draw the face landmarks on the screen.
        win.clear_overlay()
        win.set_image(img)
        if len(shapes) != 0:
            for i in range(len(shapes)):
                win.add_overlay(shapes[i])
        win.add_overlay(dets)
        faces = dlib.full_object_detections()
        for det in dets:
            faces.append(predictor(img, det))
        dlib.save_face_chips(img, faces, "shuai")
        current_path = os.getcwd()
        cv_img = cv2.imread(img_dir + "/shuai1.jpg")
        #print(current_path + "shuai.jpg")
        operate_img(img)
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    num_face = 0
    video_face_recognition()
