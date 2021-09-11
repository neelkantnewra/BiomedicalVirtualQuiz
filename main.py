import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

# Capturing the video
capture = cv2.VideoCapture(1)
capture.set(3, 1280)
capture.set(4,720)  

# Handetector model
detector = HandDetector(detectionCon=0.8,maxHands=1)


# MCQ class for various mcq operation
class MCQ():
    '''
    initialize the question and choice of mcq
    '''
    def __init__(self,data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer  = int(data[5])

        self.useranswer = None

    def update(self,cursor,bboxs):
        '''
        input: cursor , list-->box
        return useranswer
        '''
        for x,bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.useranswer = x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)
    
# import the mcq quiz data
path = "mcq.csv"
with open(path,newline='\n') as f:
    reader = csv.reader(f)
    dataall =list(reader)[1:]

# Create object for each mcq
mcqList =[]
for q in dataall:
    mcqList.append(MCQ(q))

total_question = len(mcqList)
question_number = 0

# run the image loop
while True:
    success, img = capture.read()
    img = cv2.flip(img,1)
    hands,img = detector.findHands(img,flipType=False)

    if question_number < total_question:

        mcq = mcqList[question_number]
        img,bbox = cvzone.putTextRect(img,mcq.question,[200,100],2,2,(0,255,0),(0,0,0),offset=50,border=5)
        img,bbox1 = cvzone.putTextRect(img,mcq.choice1,[200,200],2,2,(0,255,0),(0,0,0),offset=20,border=1)
        img,bbox2 = cvzone.putTextRect(img,mcq.choice2,[200,300],2,2,(0,255,0),(0,0,0),offset=20,border=1)
        img,bbox3 = cvzone.putTextRect(img,mcq.choice3,[200,400],2,2,(0,255,0),(0,0,0),offset=20,border=1)
        img,bbox4 = cvzone.putTextRect(img,mcq.choice4,[200,500],2,2,(0,255,0),(0,0,0),offset=20,border=1)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length,info=  detector.findDistance(lmList[8],lmList[12])
            if length < 30:
                mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
                print(mcq.useranswer)
                if mcq.useranswer is not None:
                    time.sleep(0.3)
                    question_number+=1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.useranswer == mcq.answer:
                score+=1
        score = round((score/total_question)*100,2)
        img,_ = cvzone.putTextRect(img,"Biomedical Quiz is Over",[250,300],2,2,(0,255,0),(0,0,0),offset=50,border=5)
        img,_ = cvzone.putTextRect(img,f"Your Score is {score}%",[700,300],2,2,(0,255,0),(0,0,0),offset=50,border=5)
        cv2.destroyAllWindows()
        
    # Draw Progress Bar
    barValue = 150 + (950//total_question)*question_number
    cv2.rectangle(img,(150,600),(barValue,650),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(150,600),(1100,650),(255,0,0),5)
    img,_ = cvzone.putTextRect(img,f"{question_number}/{total_question}",[1130,635],2,2,offset=20,border=1)

    cv2.imshow('frame', img)
    cv2.waitKey(1) 
