import face_recognition
import os


class FaceRecog():
    def compare_faces(path: str):
        image = face_recognition.load_image_file(path)
        face_locations = face_recognition.face_locations(image)

        if (len(face_locations) > 0):
            print("POZNÁN OBLIČEJ!!!!")
            unknown_picture = face_recognition.load_image_file(path)
            unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

            directory = "./assets/"
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                if (os.path.isfile(f)):
                    print(f)
                    known_picture = face_recognition.load_image_file(f)
                    known_face_encoding = face_recognition.face_encodings(known_picture)[0]
                    result = face_recognition.compare_faces(
                        [known_face_encoding], unknown_face_encoding)
                    if (result[0] == True):
                        #os.remove(path)
                        print("ROZPOZNÁNO")
                        return [result[0], filename]
            print("NEROZPOZNÁNO")
            return [False]
        else:
            print("NEVIDÍM XICHT!")
            return [False]
