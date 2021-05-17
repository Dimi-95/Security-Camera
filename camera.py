from datetime import datetime
from cv2 import *
import numpy as np
import os
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

fromaddr = "dimipythontestemail@gmail.com"
toaddr = "dkasderidis95@gmail.com"

video = VideoCapture(0)
_, frame = video.read()
last_frame = frame
threshold = 250000

record_buffer_max = 15
record_buffer = 0

fourcc = VideoWriter_fourcc(*"XVID")
numFiles = len(next(os.walk("C:\\Users\\Kas\\Desktop\\Programming Projects\\Security Camera\\Motion detection\\output_files"))[2])
output = VideoWriter("C:\\Users\\Kas\\Desktop\\Programming Projects\\Security Camera\\Motion detection\\output_files\\" + str(numFiles) +".mp4", fourcc, 30.0, (int(video.get(3)), int(video.get(4))))

while True:
    now = datetime.now()
    _, frame = video.read()
    net_difference = 0.0

    gray_curr = cvtColor(frame, COLOR_BGR2GRAY)
    gray_last = cvtColor(last_frame, COLOR_BGR2GRAY)

    diff = subtract(gray_curr, gray_last)

    w = np.size(diff, 0)
    h = np.size(diff, 1)
    
    for i in range (0, w):
        for j in range (0, h):
            if i % 5 == 0 & j % 5 == 0:
                x = diff[i, j]

                net_difference += (x)
    imshow("Difference", diff)

    if net_difference > threshold:
        record_buffer = record_buffer_max

    rectangle(frame, (int(video.get(3)) - 254, int(video.get(4) - 70)), (int(video.get(3)) - 30, int(video.get(4) - 35)), (0, 0, 0), -10)
    putText(frame, now.strftime("%d/%m/%Y %H:%M:%S"), (int(video.get(3)) - 250, int(video.get(4) - 50)), FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    if record_buffer < 0:
        putText(frame, "Not Moving", (20, 20), FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    else:
        putText(frame, "Moving", (20, 20), FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        output.write(frame)
    record_buffer -= 1
    if record_buffer < -100:
        record_buffer = -100

    imshow("Frame", frame)
    last_frame = frame
    #("C:\\Users\\Kas\\Desktop\\Programming Projects\\Security Camera\\Motion detection\\output_files\\" + str(numFiles) +".avi")
    print(str(numFiles))


    if waitKey(1) & 0xFF == ord("q"):
        break

video.release()
output.release()
destroyAllWindows()

if len(str(numFiles)) >= 0:
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "Test"
  
    # string to store the body of the mail 
    body = "Bonjure²"
  
    #   attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
    # open the file to be sent  
    filename = str(numFiles) + ".mp4"
    attachment = open("C:\\Users\\Kas\\Desktop\\Programming Projects\\Security Camera\\Motion detection\\output_files\\" + str(numFiles) +".mp4", "rb") 
  
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
  
    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
  
    # encode into base64 
    encoders.encode_base64(p) 
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
    #   attach the instance 'p' to instance 'msg' 
    msg.attach(p) 
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication 
    s.login(fromaddr, "[Insert Password here]") 
  
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
  
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
    # terminating the session 
    s.quit() 





