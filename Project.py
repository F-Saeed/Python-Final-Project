import PIL
import inspect
import zipfile
import pytesseract
import cv2 as cv
import numpy as np

from zipfile import ZipFile
from PIL import Image, ImageDraw
from IPython.display import display
from ipywidgets import interact

def cropped_face_lst(faces):
    ''' Crops out faces from given image
    :param faces: A list of coordinates of faces in the image being used
    :return cropped_lst: A list with cropped images of faces
    '''
    
    # Set our drawing context
    drawing=ImageDraw.Draw(img)
    
    #Empty list which will contain the cropped face images
    cropped_lst = []
    
    for x,y,w,h in faces:
        #cropping along coordinates (x,y,x+w,y+h)
        cropped = img.crop((x,y,x+w,y+h))
        
        #List of images with cropped faces
        cropped_lst.append(cropped)
    
    #Finally lets return this
    return cropped_lst

def thumb_lst(lst):
    '''Converting images in a list to thumbnails
    param lst: A list of images
    return thumb_lst: A list of modified thumbnail images
    '''
    thumb_lst = []
    for image in lst:
        size =(80,80)
        image.thumbnail(size)
        thumb_lst.append(image)
    
    return thumb_lst

def height_mult(num_images):
    '''determining height multiplier of contact sheet
    param num_images: number of images in the contact sheet
    return height_mult: A multiplier depending on the number of images in the contact sheet 
    '''
    if num_images > 0 and num_images <= 5:
        height_mult = 1
    elif num_images > 5 and num_images <= 10:
        height_mult = 2
    elif num_images > 10 and num_images <= 15:
        height_mult = 3
    elif num_images > 15 and num_images <= 20:
        height_mult = 4 
    elif num_images > 20 and num_images <= 25:
        height_mult = 5
    elif num_images > 25 and num_images <= 30:
        height_mult = 6         
    return height_mult        
                    
# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('readonly/haarcascade_eye.xml')

count = 0
handle = ZipFile('readonly/images.zip')

#list of file names
names_lst = handle.namelist()

#Type your keyword here
inp = input("Enter Keyword: ").lower()

for zipfile in handle.infolist():
    file = handle.open(zipfile)
    
    #list of file names
    names_lst = handle.namelist()
    
    #opening the file as an image file
    img = Image.open(file).convert('RGB')
    open_cv_img = np.array(img) 
    # Convert RGB to BGR
    faces = cv.cvtColor(open_cv_img, cv.COLOR_RGB2BGR)
    
    text = pytesseract.image_to_string(img)
    
    if inp in text.lower():
        faces_gray = cv.cvtColor(faces, cv.COLOR_BGR2GRAY)
        #cv_img_bin=cv.threshold(faces_gray,180,250,cv.THRESH_BINARY)[1]
        faces_detect = face_cascade.detectMultiScale(faces_gray, scaleFactor =1.3, minNeighbors = 5)              
        face_lst = cropped_face_lst(faces_detect)
        #number of images in face_lst
        num_images = len(face_lst)
            
        if num_images != 0:
                
      
            #modifying face_lst images to be represented as thumbnails
            face_lst = thumb_lst(face_lst)
        
            #Creating Contact Sheet by using same code as module 3    
            first_image=face_lst[0].resize((80,80))
        
            #height_mult = height_mult(num_images)
                 
            contact_sheet=PIL.Image.new(first_image.mode, (first_image.width * 8, first_image.height * 1))
            x=0
            y=0
    
            for img in face_lst:
                contact_sheet.paste(img, (x, y) )
                if x+first_image.width == contact_sheet.width:
                    x=0
                    y=y+first_image.height
                else:
                    x=x+first_image.width
                
            print("Results found in file {}".format(names_lst[count]))
            display(contact_sheet)

            
        else:
            print("Results found in file {}".format(names_lst[count]))
            print("But there were no faces in that file")
            
    count += 1