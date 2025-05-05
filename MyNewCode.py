from __future__ import print_function
import sys
import math
import ctypes
import random
import tkinter

from fsdk import FSDK
from PIL import Image, ImageOps
from tk import MainWindow, Style
import App as fs
import win
import mysql.connector

LIVENESS = 0.2  # liveness threshold
drawFeatures = False
trackerMemoryFile = "tracker70.dat"

print('Initializing FSDK... ', end='')
FSDK.ActivateLibrary(
    "HpYQSPxnv1/t3i2MSYJM4jbAF70h1a0BhTmdh+irLaGhKhyIb5g4bqYY7zCZf01IoAqZ+mawfFoncLf7VfxxLn453HuHb38SRTk1yMTMQ2RoAnrXi7ZG01IEWv9Ix6LL+KD6kdVG6JRMuFvaV2yfYp+ntEiCYP8K9bkEKbAaA/s=")
FSDK.Initialize()
print('OK\nLicense info:', FSDK.GetLicenseInfo())

FSDK.InitializeCapturing()
print('Looking for video cameras... ', end='')
camList = FSDK.ListCameraNames()

if not camList:
    print('Please attach a camera.')

print(camList[0].devicePath)

camera = camList[0]  # choose the first camera (0)
print("using '%s'" % camera)
formatList = FSDK.ListVideoFormats(camera)
print(*formatList, sep='\n')

vfmt = formatList[0]  # choose the first format: vfmt.Width, vfmt.Height, vfmt.BPP
print('Selected camera format:', vfmt)
FSDK.SetVideoFormat(camera, vfmt)

print("Trying to open '%s'... " % camera, end='')
camera = FSDK.OpenVideoCamera(camera)
print('OK', camera.handle)

try:
    fsdkTracker = FSDK.Tracker.FromFile(trackerMemoryFile)
except:
    fsdkTracker = FSDK.Tracker()  # creating a FSDK Tracker

fsdkTracker.SetParameters(  # set realtime face detection parameters
    HandleArbitraryRotations=False,
    DetermineFaceRotationAngle=False,
    InternalResizeWidth=256,
    FaceDetectionThreshold=5,
    RecognizeFaces=True,
    DetectFacialFeatures=True
)
fsdkTracker.SetParameter('DetectLiveness', True);  # enable liveness
fsdkTracker.SetParameter('SmoothAttributeLiveness', True);  # use smooth minimum function for liveness values
fsdkTracker.SetParameter('AttributeLivenessSmoothingAlpha', 1);  # smooth minimum parameter, 0 -> mean, inf -> min
fsdkTracker.SetParameter('LivenessFramesCount', 15);  # minimal number of frames required to output liveness attribute

need_to_exit = False


def onDestroy():
    global need_to_exit
    need_to_exit = True


root = tkinter.Tk()
root.title('Passive Liveness')
root.protocol('WM_DELETE_WINDOW', onDestroy)

window = MainWindow(root)

detectedStyle = Style(color='#0000FF', width=2, fill='')
fakeStyle = Style(color='#FF0000', width=2, fill='')
liveStyle = Style(color='#00FF00', width=2, fill='')
faceStyle = Style(color='#FFFFFF', width=5, fill='')
featureStyle = Style(color='#FFFF60', width=2, fill='#FFFF60')
textGreen = Style(color='#00FF00', width=1, fill='')
textRed = Style(color='#FF0000', width=1, fill='')
textShadow = Style(color='#808080', width=1, fill='')


def dot_center(dots):  # calc geometric center of dots
    return sum(p.x for p in dots) / len(dots), sum(p.y for p in dots) / len(dots)


class LowPassFilter:  # low pass filter to stabilize frame size

    def __init__(self, a=0.35):
        self.a, self.y = a, None

    def __call__(self, x):
        self.y = self.a * x + (1 - self.a) * (self.y or x)
        return self.y


scor = ''

liveness_score = 0


class FaceLocator:

    def __init__(self, fid):
        self.lpf = LowPassFilter()
        self.center = self.angle = self.frame = None
        self.fid = fid
        self.faceOval = self.livenessOval = self.shadow = self.name = None
        self.countdown = 35
        self.features = []
        self.liveness = None

    def doesIntersect(self, state):
        (x1, y1, x2, y2), (xx1, yy1, xx2, yy2) = self.frame, state.frame
        return not (x1 >= xx2 or x2 < xx1 or y1 >= yy2 or y2 < yy1)

    def drawShape(self):
        window.deleteObject(self.faceOval)

        self.faceOval = window.drawOval(self.center, *self.frame, style=faceStyle)

        if self.liveness is not None:
            self.livenessOval = window.drawOval(self.center, *self.frame,
                                                style=liveStyle if self.liveness >= LIVENESS else fakeStyle)

    def draw(self):
        sampleNum = 0
        try:

            ff = fsdkTracker.GetFacialFeatures(0, self.fid)

            if self.lpf is None:
                self.lpf = LowPassFilter()

            xl, yl = dot_center([ff[k] for k in FSDK.FSDKP_LEFT_EYE_SET])
            xr, yr = dot_center([ff[k] for k in FSDK.FSDKP_RIGHT_EYE_SET])
            w = self.lpf((xr - xl) * 2.8)
            h = w * 1.4
            self.center = (xr + xl) / 2, (yr + yl) / 2 + w * 0.05
            self.angle = math.atan2(yr - yl, xr - xl) * 180 / math.pi
            self.frame = -w / 2, -h / 2, w / 2, h / 2

            if drawFeatures:
                for i in self.features:
                    window.deleteObject(i)

                self.features = [window.drawCircle((p.x, p.y), 1, style=featureStyle) for p in ff]

            self.liveness = fsdkTracker.GetTrackerFacialAttribute(0, self.fid, 'Liveness')
            self.liveness = FSDK.GetValueConfidence(self.liveness, 'Liveness')

            window.deleteObject(self.shadow)
            window.deleteObject(self.name)

            #

            print()

            name1 = fsdkTracker.GetName(self.fid)

            name = f'{name1}\nLIVENESS: {self.liveness * 100:.2f}%'

            scor = self.liveness * 100
            global liveness_score
            liveness_score = self.liveness * 100

            # if scor > 60:
            # sampleNum = sampleNum + 1
            # print(sampleNum)
            # print(name1 +" Hai")
            # else:
            # root.destroy()

            # fsdkTracker.Free()
            # camera.Close()

            # FSDK.FinalizeCapturing()

            # FSDK.Finalize()

            self.shadow = window.drawText((self.center[0] - w // 3 + 2, self.center[1] - h // 3 + 2), name,
                                          style=textShadow),
            self.name = window.drawText((self.center[0] - w // 3, self.center[1] - h // 3), name,
                                        style=textGreen if self.liveness > LIVENESS else textRed)

            self.drawShape()
            self.countdown = 35
        except FSDK.AttributeNotDetected:
            pass
        except FSDK.Exception:
            self.countdown -= 1

            if self.countdown <= 8:
                self.frame = [v * 0.95 for v in self.frame]

            self.drawShape()

        return self.countdown > 0


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


sampleNum = 0

trackers = {}

while not need_to_exit:
    img = camera.GrabFrame()
    img = img.Resize(window.getScaleFor(img.width, img.height))
    window.drawImage(Image.frombytes('RGB', (img.width, img.height), img.ToBytes(FSDK.FSDK_IMAGE_COLOR_24BIT)))

    faces = frozenset(fsdkTracker.FeedFrame(0, img))  # recognize all faces in the image
    for face_id in faces.difference(trackers):  # create new trackers
        trackers[face_id] = FaceLocator(face_id)

    #img.Free()

    missed = []
    for face_id, tracker in trackers.items():  # iterate over current trackers
        if face_id in faces:
            tracker.draw()  # fsdkTracker.GetFacialFeatures(face_id)) # draw existing tracker
            ss = fsdkTracker.GetName(face_id)
            print(ss)

            print(liveness_score)
            sampleNum = sampleNum + 1



            if sampleNum > 100:
                uname, Email, Phone, Accountno = fs.loginvales1()
                #uname ="san"
                #Email ="sangeeth5535@gmail.com"

                if (uname == ss):
                    if int(liveness_score) > 50:
                        print('ok')
                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='25newfacebankdb')
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT * FROM multitb where username='" + ss + "' and Account='" + Accountno + "'")
                        data = cursor.fetchone()

                        if data:
                            import random

                            n = random.randint(1111, 9999)

                            sendmsg(Phone, "Your OTP" + str(n))

                            mmmsg = "Your OTP" + str(n);

                            import smtplib
                            from email.mime.multipart import MIMEMultipart
                            from email.mime.text import MIMEText
                            from email.mime.base import MIMEBase
                            from email import encoders

                            fromaddr = "projectmailm@gmail.com"
                            toaddr = Email

                            # instance of MIMEMultipart
                            msg = MIMEMultipart()

                            # storing the senders email address
                            msg['From'] = fromaddr

                            # storing the receivers email address
                            msg['To'] = toaddr

                            # storing the subject
                            msg['Subject'] = "Alert"

                            # string to store the body of the mail
                            body = mmmsg

                            # attach the body with the msg instance
                            msg.attach(MIMEText(body, 'plain'))

                            # creates SMTP session
                            s = smtplib.SMTP('smtp.gmail.com', 587)

                            # start TLS for security
                            s.starttls()

                            # Authentication
                            s.login(fromaddr, "qmgn xecl bkqv musr")

                            # Converts the Multipart msg into a string
                            text = msg.as_string()

                            # sending the mail
                            s.sendmail(fromaddr, toaddr, text)

                            # terminating the session
                            s.quit()

                            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                           database='25newfacebankdb')

                            cursor = conn.cursor()
                            cursor.execute(
                                "insert into temptb values('','" + Accountno + "','" + ss + "','" + str(n) + "')")
                            conn.commit()
                            conn.close()

                else:
                    print('No')


                    import os

                    outFileName = 'static/out.jpg'

                    try:
                        if img.width > 0 and img.height > 0:
                            hbitmap = img.GetHBitmap()
                            saimg = FSDK.Image(hbitmap)
                            saimg.SaveToFile(outFileName, quality=85)
                            print("Image saved to", outFileName)

                            if os.path.exists(outFileName):
                                # Now send email
                                from email.mime.multipart import MIMEMultipart
                                from email.mime.text import MIMEText
                                from email.mime.base import MIMEBase
                                from email import encoders
                                import smtplib

                                fromaddr = "projectmailm@gmail.com"
                                toaddr = Email

                                msg = MIMEMultipart()
                                msg['From'] = fromaddr
                                msg['To'] = toaddr
                                msg['Subject'] = "Face Verification"
                                body = "Unknown User Accessed Your Account"
                                msg.attach(MIMEText(body, 'plain'))

                                filename = "out.jpg"
                                with open(outFileName, "rb") as attachment:
                                    p = MIMEBase('application', 'octet-stream')
                                    p.set_payload(attachment.read())
                                    encoders.encode_base64(p)
                                    p.add_header('Content-Disposition', f"attachment; filename={filename}")
                                    msg.attach(p)

                                s = smtplib.SMTP('smtp.gmail.com', 587)
                                s.starttls()
                                s.login(fromaddr, "qmgn xecl bkqv musr")
                                s.sendmail(fromaddr, toaddr, msg.as_string())
                                s.quit()
                            else:
                                print("Image was not saved. Email not sent.")

                        else:
                            print("Invalid image. Skipping image save and email.")

                    except Exception as e:
                        print("Exception during image save or email:", e)

                    finally:
                        img.Free()

                    



        else:
            missed.append(face_id)

    for mt in missed:  # find and remove trackers that are not active anymore
        st = trackers[mt]
        if any(st.doesIntersect(trackers[tr]) for tr in faces if tr != mt) or not st.draw():
            del trackers[mt]
    if sampleNum > 100:
        #print('Please wait while freeing resources... ', flush=True)

        #root.destroy()

        #fsdkTracker.Free()
        #camera.Close()

        #FSDK.FinalizeCapturing()

        #FSDK.Finalize()
        break
    window.update_idletasks()
    window.update()

#print('Please wait while freeing resources... ', flush=True)

root.destroy()

fsdkTracker.Free()
camera.Close()

FSDK.FinalizeCapturing()

FSDK.Finalize()
