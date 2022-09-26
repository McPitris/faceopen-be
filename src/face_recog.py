import cv2
import face_recognition
import os

class FaceRecog():
    def compare_faces(path:str):
        img = cv2.imread(
            path)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]
        # cv2.imshow("Img1", img)

        directory = "../assets/"
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if(os.path.isfile(f)):
                print(f)
                img2 = cv2.imread(f)
                rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
                img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
                result = face_recognition.compare_faces([img_encoding], img_encoding2)
                if(result[0] == True):
                    os.remove(path)
                    return result
        return [False]
            
        # cv2.waitKey(0)
