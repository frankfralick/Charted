import rhinoscriptsyntax as rs
import scriptcontext as rsc
import sys
#Add your site-packages directory to the path if you need to.
sys.path.append("C:\\Python27\\Lib\\site-packages\\")

from charted import charted
import operator


scene = charted.Scene(rs)

data = [(10,11),(75,75),(10,10),(70000,600)]
#charted.Scatter.options.set(chartDataSeriesXY = data)

scatterChart = charted.Scatter(rs,rsc,scene, chartHeight = .5, chartVerticalOffset = 0)
data2 = [(800,700), (300,400), (500,1000),(500,500)]

newScatterChart = charted.Scatter(rs,rsc,scene, chartDataSeriesXY = data2)



















#charted.Scatter.options.set(chartDataSeries = data)
