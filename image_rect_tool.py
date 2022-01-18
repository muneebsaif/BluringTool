import cv2
import os
import numpy as np
from pynput.keyboard import Key, Listener

drawing = False # true if mouse is pressed
ix,iy = -1,-1
def just_print_for_all(event, x, y, flags, param):
	global ix,iy,drawing
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing = True
		ix,iy = x,y
	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			topLeft = (ix,iy)
			bottomRight = (x,y)
			x, y = topLeft[0], topLeft[1]
			w, h = bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]
			ROI = img[y:y+h, x:x+w]
			blur = cv2.GaussianBlur(ROI, (41,41), 0) 
			img[y:y+h, x:x+w] = blur
			# cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
	elif event == cv2.EVENT_LBUTTONUP:
		drawing = False




foldername=input("Enter Directory of images (if same directory then enter 'q'):\t")
ls=os.listdir(os.path.join(os.getcwd(),foldername))
ls_sorted=sorted(ls, key=lambda x: int("".join([i for i in x if i.isdigit()])))
deletefolder="deleted"
if not os.path.exists(os.path.join(os.getcwd(),deletefolder)):
	os.mkdir(os.path.join(os.getcwd(),deletefolder))
ind=0
over=False
try:
	rf=open("index.txt",'r')
	a=int(rf.readline())
	rf.close()
except:
	a=0

while not over:
	if ind<=a:
		ind+=1
		continue
	name=ls_sorted[ind]
	windowname=name
	# cv2.namedWindow(windowname,cv2.WND_PROP_FULLSCREEN)
	# cv2.setWindowProperty(windowname, cv2.WND_PROP_FULLSCREEN, cv2.CV_WINDOW_FULLSCREEN)
	cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
	# cv2.setWindowProperty(windowname,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
	cv2.setMouseCallback(windowname, just_print_for_all)
	if name.split(".")[-1] not in ['jpg','png','jpeg']:
		ind+=1
		continue
	if foldername=='q':
		name=os.path.join(os.getcwd(),name)#[1,2,3]
	else:
		name=os.path.join(os.getcwd(),foldername,name)
	try:
		img=cv2.imread(name)
	except:
		print(name)
		ind+=1
	while True:
		cv2.imshow(windowname,img)
		key=cv2.waitKey(1)
		if key==ord('d'):
			cv2.imwrite(name,img)
			f=open("index.txt",'w')
			f.write(str(ind))
			f.close()
			ind+=1
			break
		elif key==ord('a'):
			cv2.imwrite(name,img)
			f=open("index.txt",'w')
			f.write(str(ind))
			f.close()
			ind-=1
			break
		elif key==ord('o'):
			os.rename(name,os.path.join(os.getcwd(),deletefolder,os.path.split(name)[1]))
			ls_sorted.pop(ind)
			# ind+=1
			f=open("index.txt",'w')
			f.write(str(ind))
			f.close()
			break
		elif key==ord('q'):
			over=True
			break
		elif key==ord('r'):
			img=cv2.imread(name)
	cv2.destroyAllWindows()
print("done")

