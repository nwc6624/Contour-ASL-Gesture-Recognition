#-------------------------------------------------------------------------------
# Name:        Contour ASL Gesture Recognition
# Purpose:     N/A
#
# Author:      Noah Caulfield
#
# Created:     31/03/2014
#-------------------------------------------------------------------------------


import sys
import cv2
import cv2.cv as cv
import numpy as np
from time import clock




# function to compare two forms and returns the result of comparing
# Good result <0.1
# Bad result> 0.1
# exact matching =0


def compare_2_formes(Image1,Image2):
        mincontour=500 # minimum size of a form to be detected
        CVCONTOUR_APPROX_LEVEL=5# parameter for call contour
        img_edge1=cv.CreateImage(cv.GetSize(Image1),8,1) #egde image

#        img1_8uc3=cv.CreateImage(cv.GetSize(Image1),8,3)

        img_edge2=cv.CreateImage(cv.GetSize(Image2),8,1)
 #       img2_8uc3=cv.CreateImage(cv.GetSize(Image2),8,3)

        cv.Threshold(Image1,img_edge1,123,255,cv.CV_THRESH_BINARY) # filter threshold
        cv.Threshold(Image2,img_edge2,123,255,cv.CV_THRESH_BINARY)



        storage1=cv.CreateMemStorage()
        storage2=cv.CreateMemStorage()

        first_contour1=cv.FindContours(img_edge1,storage1) # pointer to the first edge of the form 1
        first_contour2=cv.FindContours(img_edge2,storage2) # pointer to the first edge of the form 2


        newseq=first_contour1
        newseq2=first_contour2

        if not(first_contour1) or not(first_contour2):
                return 0

        current_contour=first_contour1
        while 1:
                current_contour=current_contour.h_next() # path in the sequence of edges of the first form
                if (not(current_contour)): # stop condition if the contour pointer = NULL
                        break

                if cv.ContourArea(current_contour)> mincontour :
                        newseq=cv.ApproxPoly(current_contour,storage1,cv.CV_POLY_APPROX_DP,CVCONTOUR_APPROX_LEVEL,0)
              #          cv.CvtColor(Image1,img1_8uc3,cv.CV_GRAY2BGR );
              #          cv.DrawContours(img1_8uc3,newseq,cv.CV_RGB(0,255,0),cv.CV_RGB(255,0,0),0,2,8);
              #          cv.NamedWindow("ContourImage2",cv.CV_WINDOW_AUTOSIZE)
              #          cv.ShowImage("ContourImage2",img1_8uc3)


        current_contour=first_contour2

       # path of the second form of contours
        while 1:
                current_contour=current_contour.h_next()
                if (not(current_contour)):
                        break

                if cv.ContourArea(current_contour)> mincontour :
                        newseq2=cv.ApproxPoly(current_contour,storage2,cv.CV_POLY_APPROX_DP,CVCONTOUR_APPROX_LEVEL,0)
              #          cv.CvtColor(Image2,img2_8uc3,cv.CV_GRAY2BGR);
              #          cv.DrawContours(img2_8uc3,newseq2,cv.CV_RGB(0,255,0),cv.CV_RGB(255,0,0),0,2,8);
              #          cv.NamedWindow("ContourImage",cv.CV_WINDOW_AUTOSIZE)
              #          cv.ShowImage("ContourImage",img2_8uc3)


        matchresult=1;
        matchresult=cv.MatchShapes(newseq,newseq2,1,2)
        return matchresult
        #print("Match result :"+str(matchresult))

#main
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX,5,5, 0, 3, 8) #initialize
SignsList=["a.jpg","b.jpg","c.jpg","d.jpg","e.jpg","f.jpg"]  # list which contain all images of signs
imagesList={"a.jpg":cv.LoadImage("signs/a.jpg",cv.CV_LOAD_IMAGE_GRAYSCALE)}

for e in SignsList:
        imagesList[e]=cv.LoadImage("signs/"+e,cv.CV_LOAD_IMAGE_GRAYSCALE)
        #imagesList.append(cv.LoadImage("signs/"+e,cv.CV_LOAD_IMAGE_GRAYSCALE))
cv.NamedWindow("Input",cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("Gesture Space",cv.CV_WINDOW_AUTOSIZE)
matchresult=1;
p_capWebcam=cv.CaptureFromCAM(0)
while 1 :
        p_imgOriginal =cv.QueryFrame(p_capWebcam)
        cv.Flip(p_imgOriginal,p_imgOriginal,1)

       # capture from webcam
        p_gray=cv.CreateImage(cv.GetSize(p_imgOriginal), 8, 1 )
        cv.CvtColor(p_imgOriginal,p_gray,cv.CV_BGR2GRAY)
        cv.SetImageROI(p_gray,(400,200,200,200))
       # Region setting of fixed interest
        cv.Threshold(p_gray,p_gray,100,255,cv.CV_THRESH_BINARY_INV)

        cv.Rectangle(p_imgOriginal,(400,200),(600,400),(255,0,0),4);
        j=0
        for imageI in imagesList :# path of the image list and test each image with the ROI (region of interest)
                #image_to_test=cv.LoadImage("signs/"+image_path,cv.CV_LOAD_IMAGE_GRAYSCALE)
                matchresult=compare_2_formes(p_gray,imagesList[imageI])      #comparison
                #print("le match est "+str(matchresult))
                if matchresult < 0.13 and matchresult!=0 :
                        sign_name=imageI.split('.')[0]
                        print("letter :"+sign_name+",with a matching of :"+str(matchresult))
                        cv.PutText(p_imgOriginal,sign_name,(5,120),font,255)

                cv.ShowImage("Input",p_imgOriginal)
                cv.ShowImage("Gesture Space",p_gray)
                j=j+1
        checkchar=cv.WaitKey(27)
        if checkchar==27 :
                        cv.DestroyAllWindows("Input")
                        cv.DestroyAllWindows("Gesture Space")
                        break
