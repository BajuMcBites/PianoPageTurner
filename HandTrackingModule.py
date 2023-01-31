import cv2
import mediapipe as mp
import keyboard



class HandDetector():

    def __init__(self, mode=False,
                 max_hands=2,
                 detection_confidence=0.5,
                 track_confidence=0.5):

        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode = self.mode,
                                        max_num_hands = self.max_hands,
                                        min_detection_confidence = self.detection_confidence,
                                        min_tracking_confidence = self.track_confidence)

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True, locations = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if (results.multi_hand_landmarks):
            for handLms in results.multi_hand_landmarks:
                if(draw):
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

            if(locations):
                return img, results.multi_hand_landmarks

        return img, None

def getLandmarkList(fileName):
    cap = cv2.VideoCapture(0)
    hand_detector = HandDetector()
    loc = None


    while loc == None:
        success, img = cap.read()

        img, landmarks = hand_detector.findHands(img)

        if(landmarks):
            if keyboard.is_pressed("a"):
                loc = landmarks

        cv2.imshow("Image", img)
        cv2.waitKey(1)

    f = open(fileName, "w")
    for handLms in loc:
        for id, lm in enumerate(handLms.landmark):
            f.write(str(id) + ' ' + str(lm.x) + " " + str(lm.y) + "\n")
    f.close()

#def HookEm():

def readLandmarkFile(filename):
    f = open(filename, "r")
    data = f.read()
    f.close()

    split_data = data.split("\n")

    result = []


    for line in split_data:
        line = line.split(" ")
        if (len(line) == 3):
            result.append([float(line[1]), float(line[2])])

    return result

def parseData(data):
    result = []

    for i in data:
        temp = []
        for k in data:
            temp.append(distance(i,k))
        result.append(temp)

    for i in range(len(data)):
        for k in range(len(data)):
            result[i][k] /= result[0][3]

    return result


def distance(coord1, coord2):
    return pow(pow(coord1[0] - coord2[0], 2) + pow(coord1[1] - coord2[1], 2), 0.5)

def difference(data1, data2):
    result = []

    for i in range(len(data1)):
        for k in range(len(data1[0])):
            result.append(abs(data1[i][k] - data2[i][k]))

    return result


def findHookem(pose_file, CONFIDENCE = 0.2):
    cap = cv2.VideoCapture(0)
    hand_detector = HandDetector()
    x1 = parseData(readLandmarkFile(pose_file))
    count = 0

    while True:
        success, img = cap.read()

        img, landmarks = hand_detector.findHands(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

        x = []
        if(landmarks):
            for handLms in landmarks:
                for id, lm in enumerate(handLms.landmark):
                    x.append([lm.x, lm.y])

        try:
            x = parseData(x)
            if(max(difference(x1, x)) < CONFIDENCE):
                print(count)
                count += 1
                print("HookEm")
        except:
            pass


def main():
    '''
    #getLandmarkList("HookEm4.txt")
    x1 = parseData(readLandmarkFile("HookEm.txt"))
    x2 = parseData(readLandmarkFile("HookEm2.txt"))
    x3 = parseData(readLandmarkFile("HookEm4.txt"))

    print(max(difference(x1,x2)))
    print(max(difference(x1,x3)))
    '''
    findHookem("HookEm4.txt", CONFIDENCE=0.13)

if __name__ == "__main__":
    main()


