import rhinoscriptsyntax as rs
import scriptcontext as rsc
import sys
#Add your site-packages directory to the path if you need to.
sys.path.append("C:\\Python27\\Lib\\site-packages\\")
from charted import charted
import operator
import clr


scene = charted.Scene(rs, sceneWidth = 300)
