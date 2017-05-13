# Contour-ASL-Gesture-Recognition

This is my prototype of a real time contour comparison system that receives users’ gestural 
input via web camera and compares it to my own set of previously compiled images to determine 
peak similarities. These simularities determine the actual gesture with a negligible margin
of error when used in the correct environment. I relied heavily on the OpenCV library in 
Python, which deals mainly with computer vision, to define a method of comparison to implement,
and to finally optimize this build in its entirety. Relies on python 2.7 and CC2 imports,
along with numpy. 
