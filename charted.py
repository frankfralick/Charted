"""PyBuilding is a Python module made to facilitate the moving building
   data between building scale modelling tools as well as downstream to
   object scale modelling tools in ways that are useful.

   This module aims to organize API proceedures of commonly used software
   packages into a framework on which ad-hoc, building specific solutions
   can be generated."""
import sys
sys.path.append("C:\\Python27\\Lib\\site-packages\\")
sys.path.append("C:\\Python27\\Lib\\")
import utils.stuf
from utils.options import Options, attrs
import math
import operator
import ast

def testInv(number):
    this = number*2
    return this

class PbException(Exception):
    pass

class ValExcept(PbException):
    def __init__(self,message):
        self.message = message

    def __str__(self):
        return repr("woops")

def RGaxisXDiv(value, data):
    this = RGaxisDiv(value, data, 0)
    return this

def RGaxisYDiv(value, data):
    this = RGaxisDiv(value, data, 1)
    return this

def RGaxisDiv(value, data, axis):
    if data == None:
        return value
    xValsMax = max(data, key = lambda data:data[axis])
    xRangeMax = xValsMax[axis]
    xValsMin = min(data, key = lambda data:data[axis])
    xRangeMin = xValsMin[axis]
    if value == "Coarse":
        mod = 1
    elif value == "Medium":
        mod = .5
    elif value == "Fine":
        mod = .25
    thisRange = xRangeMax - xRangeMin

    intLen = len(list(str(abs(int(thisRange)))))
    if intLen >=3:
        if thisRange%math.pow(10,intLen-1) == 0:
            divs = (thisRange-(thisRange%math.pow(10,intLen-1))+math.pow(10,intLen-1))/math.pow(10,intLen-1)
            divs = (int(divs),math.pow(10,intLen-1))
        elif thisRange%math.pow(10,intLen-1) != 0:
            divs = (thisRange+math.pow(10,intLen-1))/math.pow(10,intLen-1)
            divs = (int(divs),math.pow(10,intLen-1))
        #divs = divs*mod
    else:
        divs = int(thisRange/10)
        if divs == 0:
            divs = thisRange/len(data)
            divs = (int(divs),1)
    #print "HERE HERE HERE:    "+str(divs)
    return divs

def RGmaxWidth(value,currently):
        if value < 500:
            pass

class RhinoGraphSceneUpperBounds(PbException):

    def __init__(self, height, blOffsetZero):
        self.height = height
        self.blOffsetZero = blOffsetZero
    def __str__(self):
        return repr("Provided height percentage, "+str(self.height)+", added to the x coordinate of the bottom left offset, "+str(self.blOffsetZero)+", cannot be greater than 1.")

class RhinoGraphSceneRightBounds(PbException):

    def __init__(self, width, blOffsetFirst):
        #print "Upper bound of chart is outside the current scene."
        self.width = width
        self.blOffsetFirst = blOffsetFirst
    def __str__(self):
        return repr("Provided width percentage, "+str(self.width)+", added to the x coordinate of the bottom left offset, "+str(self.blOffsetFirst)+", cannot be greater than 1.")

class RhinoLayerSelection(PbException):

    def __init__(self, layer):
        self.layer = layer
    def __str__(self):
        return repr("Make sure there are object on the layer named "+str(self.layer))

class Base:
    pass

class Scene(Base):
    options = Options(
                      sceneBottomLeft = (0,0,0),
                      sceneWidth = 100,
                      sceneResolution = (1920,1080),
                      sceneBorderVisible = False,
                      sceneLayerName = "Charted"
                      )

    options.magic(
                  chartXAxisDiv = lambda v, cur: RGaxisXDiv(v, cur.chartDataSeriesXY,cur.chartXAxisStyle),# if isinstance(cur.chartXAxisStyle, None) else v,
                  chartYAxisDiv = lambda v, cur: RGaxisYDiv(v, cur.chartDataSeriesXY,cur.chartYAxisStyle)# if isinstance(cur.chartYAxisStyle, None) else v,
                  )
    def __init__(self, rs, **kwargs):
        if rs.IsLayer(self.options.sceneLayerName)==False:
            rs.AddLayer(self.options.sceneLayerName)
            rs.CurrentLayer(self.options.sceneLayerName)
        self.options = Scene.options.push(kwargs)
        self.sceneBottomLeft = self.options.sceneBottomLeft
        self.sceneWidth = self.options.sceneWidth
        #print "SCENEWIDTH:   "+str(self.sceneWidth)
        self.sceneResolution = self.options.sceneResolution
        self.sceneDimRatio = float(self.sceneResolution[0])/float(self.sceneResolution[1])
        self.sceneHeight = self.sceneWidth/self.sceneDimRatio
        self.sceneBottomRight = (self.sceneBottomLeft[0]+self.sceneWidth,self.sceneBottomLeft[1],self.sceneBottomLeft[2])
        self.sceneTopRight = (self.sceneBottomLeft[0]+self.sceneWidth,self.sceneBottomLeft[1]+self.sceneHeight,self.sceneBottomLeft[2])
        self.sceneTopLeft = (self.sceneBottomLeft[0],self.sceneBottomLeft[1]+self.sceneHeight,self.sceneBottomLeft[2])
        self.sceneBoundary = rs.AddPolyline((self.sceneBottomLeft,self.sceneBottomRight,self.sceneTopRight,self.sceneTopLeft,
                                       self.sceneBottomLeft))
        sceneBoundaryLayer = "Scene Boundary"
        if rs.IsLayer(sceneBoundaryLayer) == True:
            rs.ObjectLayer(self.sceneBoundary,sceneBoundaryLayer)
        else:
            rs.AddLayer("Scene Boundary")
            rs.ObjectLayer(self.sceneBoundary,sceneBoundaryLayer)
        if self.options.sceneBorderVisible == False:
            rs.LayerVisible("Scene Boundary",False)
        elif self.options.sceneBorderVisible == True:
            rs.LayerVisible("Scene Boundary",True)
        self.sceneCentroid = (self.sceneBottomLeft[0]+float(self.sceneWidth)/2,self.sceneBottomLeft[1]+float(self.sceneHeight)/2,self.sceneBottomLeft[2])
        #rs.AddPoint(self.sceneCentroid)
        #rs.ViewCameraTarget(target = self.sceneCentroid)
        self.sceneBoundingBox = rs.BoundingBox(self.sceneBoundary)
        #rs.ZoomBoundingBox(self.sceneBoundingBox)
        #rs.ViewCameraLens(length = 300)
        #viewDiagonal = math.sqrt(float(self.sceneWidth)/2*float(self.sceneWidth)/2+float(self.sceneHeight)/2*float(self.sceneHeight)/2)
        #self.sceneLens = rs.ViewCameraLens(length = 35)
        #print "this is the scene Lens  "+str(self.sceneLens)
        #self.viewAngle = math.radians(61)
        #self.sceneCameraHeight = viewDiagonal*(math.tan(self.viewAngle))
        #print "this is the camera height  "+str(self.sceneCameraHeight)
        #rs.ViewCameraTarget(camera = (self.sceneCentroid[0], self.sceneCentroid[1], self.sceneCentroid[2]+self.sceneCameraHeight),target = self.sceneCentroid)
        rs.ZoomBoundingBox(self.sceneBoundingBox)

class Chart:
    options = Scene.options.add(
                                        chartVerticalOffset = .65,
                                        chartHorizontalOffset = 0,
                                        chartHeight = .35,
                                        chartWidth = .35,
                                        chartXAxisOffset = .1,
                                        chartYAxisOffset = .1,
                                        chartXAxisLabel = "Default X Axis Label",
                                        chartYAxisLabel = "Default Y Axis Label",
                                        chartBorderVisible = True,
                                        chartAxesVisible = True,
                                        chartDataSeriesXY = [(200,200),(650,4),(50,6),(70,80)],
                                        chartStyle = "Scatter",
                                        chartXAxisDiv = None,
                                        chartYAxisDiv = None,
                                        chartXAxisStyle = "Coarse", #Medium, Fine
                                        chartYAxisStyle = "Coarse", #Medium, Fine
                                        chartXAxisMod = 1,
                                        chartYAxisMod = 1,
                                        chartShowAxes = True,
                                        chartShowArrows = False,
                                        axisTick = .015,
                                        axisXLayerName = "X Axis",
                                        axisYLayerName = "Y Axis",
                                        axisXVisible = True,
                                        axisYVisible = True,
                                        axisXTickVisible = True,
                                        axisYTickVisible = True,
                                        pointStyle = "Circles",
                                        pointSizeToScale = False,
                                        colorPoints = True,
                                        fillPoints = True,
                                        hatchName = "Solid",
                                        pointColor = (150,175,100),
                                        pointHatchColor = (150,175,100),
                                        hatchTransparency = True,
                                        hatchTransparencyValue = 50,
                                        uniformTextAngle = False
                                        )

    def __init__(self, rs, rsc, math, scene,**kwargs):
        self.scene = scene
        self.options = RhinoGraphChart.options.push(kwargs)
        self.allObjects = []
        try:
            if self.options.chartVerticalOffset+self.options.chartHeight > 1:
                raise RhinoGraphSceneUpperBounds(self.options.chartHeight, self.options.chartVerticalOffset)
            elif self.options.chartHorizontalOffset+self.options.chartWidth > 1:
                raise RhinoGraphSceneRightBounds(self.options.chartWidth, self.options.chartHorizontalOffset)
        except PbException as X:
            print X
            raise X

        self.rs = rs
        self.chartVerticalOffset = self.options.chartVerticalOffset
        self.chartHorizontalOffset = self.options.chartHorizontalOffset
        self.chartHeight = self.options.chartHeight
        self.chartWidth = self.options.chartWidth
        self.chartXAxisOffset = self.options.chartXAxisOffset
        self.chartYAxisOffset = self.options.chartYAxisOffset
        self.chartXAxisLabel = self.options.chartXAxisLabel
        self.chartYAxisLabel = self.options.chartYAxisLabel
        self.chartWidthAbs = self.scene.sceneWidth*self.chartWidth
        self.chartHeightAbs = self.scene.sceneHeight*self.chartHeight
        self.chartBottomOffset = self.scene.sceneHeight*self.chartVerticalOffset
        self.chartLeftOffset = self.scene.sceneWidth*self.chartHorizontalOffset
        self.chartBlx = self.scene.sceneBottomLeft[0]+self.chartLeftOffset
        self.chartBly = self.scene.sceneBottomLeft[1]+self.chartBottomOffset
        self.chartBlz = self.scene.sceneBottomLeft[2]
        self.chartBL = (self.chartBlx,self.chartBly,self.chartBlz)
        self.chartBR = (self.chartBlx+self.chartWidthAbs,self.chartBly, self.chartBlz)
        self.chartTR = (self.chartBlx+self.chartWidthAbs,self.chartBly+self.chartHeightAbs,self.chartBlz)
        self.chartTL = (self.chartBlx,self.chartBly+self.chartHeightAbs,self.chartBlz)
        self.chartCorners = []
        self.chartCorners.append(self.chartBL)
        self.chartCorners.append(self.chartBR)
        self.chartCorners.append(self.chartTR)
        self.chartCorners.append(self.chartTL)
        if self.options.chartBorderVisible == True:
            self.chartBorder = rs.AddPolyline((self.chartBL,self.chartBR,self.chartTR,self.chartTL,self.chartBL))
            self.allObjects.append(self.chartBorder)
        self.axisXOffsetAbs = ((self.chartCorners[1][0]-self.chartCorners[0][0])*self.chartXAxisOffset)
        self.axisYOffsetAbs = ((self.chartCorners[3][1]-self.chartCorners[0][1])*self.chartYAxisOffset)
        self.axisOriginX = self.chartCorners[0][0]+self.axisXOffsetAbs
        self.axisOriginY = self.chartCorners[0][1]+self.axisYOffsetAbs
        self.axisOriginZ = self.chartCorners[0][2]
        self.axisXExtentX = self.chartCorners[1][0]-self.axisXOffsetAbs
        self.axisXExtentY = self.chartCorners[1][1]+self.axisYOffsetAbs
        self.axisXExtentZ = self.chartCorners[1][2]
        self.axisYExtentX = self.chartCorners[3][0]+self.axisXOffsetAbs
        self.axisYExtentY = self.chartCorners[3][1]-self.axisYOffsetAbs
        self.axisYExtentZ = self.chartCorners[3][2]
        self.axisXLayerName = self.options.axisXLayerName
        self.axisYLayerName = self.options.axisYLayerName

    def setBlCoord(self,bottomOffset,leftOffset):
        """
        @type bottomOffset: Float
        @param bottomOffset: The percentage (as a decimal) of the height of
        """
        blX = self.chartBL[0]+(self.chartWidthAbs*leftOffset)
        blY = self.chartBL[1]+(self.chartHeightAbs*bottomOffset)
        blZ = self.chartBL[2]
        return (blX,blY,blZ)

    def toLayer(self,object,layer):
        if self.rs.IsLayer(layer)==True:
            self.rs.ObjectLayer(object, layer)
        else:
            self.rs.AddLayer(layer,parent = self.options.sceneLayerName)
            self.rs.ObjectLayer(object, layer)
    def deleteObjects(self):
        for thisObject in self.allObjects:
            self.rs.DeleteObject(thisObject)

class Scatter(Chart):
    def __init__(self, rs, rsc, math, scene, **kwargs):
        #super(RhinoGraphScatter, self).__init__(rs, rsc, math, scene, **kwargs)
        Chart.__init__(self,rs,rsc,math,scene,**kwargs)
        if self.options.chartShowAxes == True:
            self.axisX = rs.AddLine((self.axisOriginX, self.axisOriginY, self.axisOriginZ),
                                        (self.axisXExtentX, self.axisXExtentY, self.axisXExtentZ))
            if rs.IsLayer(self.axisXLayerName) != True:
                rs.AddLayer(self.axisXLayerName)
                rs.ObjectLayer(self.axisX, self.axisXLayerName)
            else:
                rs.ObjectLayer(self.axisX, self.axisXLayerName)
            if self.options.axisXVisible == True:
                rs.ShowObject(self.axisX)
            else:
                rs.HideObject(self.axisX)
            self.axisXLength = rs.Distance((self.axisOriginX, self.axisOriginY, self.axisOriginZ),
                                        (self.axisXExtentX, self.axisXExtentY, self.axisXExtentZ))
            self.axisY = rs.AddLine((self.axisOriginX, self.axisOriginY, self.axisOriginZ),
                                        (self.axisYExtentX, self.axisYExtentY, self.axisYExtentZ))
            if rs.IsLayer(self.axisYLayerName) != True:
                rs.AddLayer(self.axisYLayerName)
                rs.ObjectLayer(self.axisY, self.axisYLayerName)
            else:
                rs.ObjectLayer(self.axisY, self.axisYLayerName)
            if self.options.axisYVisible == True:
                rs.ShowObject(self.axisY)
            else:
                rs.HideObject(self.axisY)
            self.axisYLength = rs.Distance((self.axisOriginX, self.axisOriginY, self.axisOriginZ),
                                        (self.axisYExtentX, self.axisYExtentY, self.axisYExtentZ))
            if self.options.chartShowArrows == True:
                rs.CurveArrows(self.axisYLine,2)
                rs.CurveArrows(self.axisXLine,2)

        self.chartDataSeriesXY = self.options.chartDataSeriesXY

        dataSeries = self.chartDataSeriesXY
        xValsMax = max(self.chartDataSeriesXY, key = lambda dataSeries:dataSeries[0])
        xRangeMax = xValsMax[0]
        xValsMin = min(self.chartDataSeriesXY, key = lambda dataSeries:dataSeries[0])
        xRangeMin = xValsMin[0]
        self.axisXRange = (xRangeMin,xRangeMax)
        yValsMax = max(self.chartDataSeriesXY, key = lambda dataSeries:dataSeries[1])
        yRangeMax = yValsMax[1]
        yValsMin = min(self.chartDataSeriesXY, key = lambda dataSeries:dataSeries[1])
        yRangeMin = yValsMin[1]
        self.axisYRange = (yRangeMin,yRangeMax)
        if self.options.axisXTickVisible == True:
            if self.options.chartXAxisDiv == None:
                self.chartXAxisDiv = RGaxisXDiv(1,self.chartDataSeriesXY)
        self.axisXTickCount = self.chartXAxisDiv[0]
        print "This is chartXAxisDiv:    "+str(self.chartXAxisDiv)
        print self.axisXTickCount
        self.axisXTickOrigins = rs.DivideCurve(self.axisX,self.axisXTickCount)
        self.tickMod = self.options.axisTick*self.axisXLength
        if self.options.axisTick*self.axisYLength < self.tickMod:
            self.tickMod = self.options.axisTick*self.axisYLength
        self.axisXTicks = []
        for i in range(len(self.axisXTickOrigins)):
            thisTick = rs.AddLine(self.axisXTickOrigins[i],
                                    (self.axisXTickOrigins[i][0],
                                    self.axisXTickOrigins[i][1]-self.tickMod,
                                    self.axisXTickOrigins[i][2]))
            self.axisXTicks.append(thisTick)
        if self.options.axisYTickVisible == True:
            if self.options.chartYAxisDiv == None:
                self.chartYAxisDiv = RGaxisYDiv(1,self.chartDataSeriesXY)
        self.axisYTickCount = self.chartYAxisDiv[0]
        self.axisYTickOrigins = rs.DivideCurve(self.axisY,self.axisYTickCount)
        self.axisYTicks = []
        for i in range(len(self.axisYTickOrigins)):
            thisTick = rs.AddLine(self.axisYTickOrigins[i],
                                    (self.axisYTickOrigins[i][0]-self.tickMod,
                                    self.axisYTickOrigins[i][1],
                                    self.axisYTickOrigins[i][2]))
            self.axisYTicks.append(thisTick)
        self.axisXScale = self.chartXAxisDiv[1]/(rs.Distance(self.axisXTickOrigins[1],
                                       (self.axisOriginX,
                                        self.axisOriginY,
                                        self.axisOriginZ)))
        self.axisYScale = self.chartYAxisDiv[1]/(rs.Distance(self.axisYTickOrigins[1],
                                       (self.axisOriginX,
                                        self.axisOriginY,
                                        self.axisOriginZ)))
        self.dataPoints = []
        if self.axisYRange[0] < 0:
            negVal = abs(self.axisYRange[0])
            negValScaled = negVal/self.axisYScale
            rs.MoveObject(self.axisX,(0,negValScaled,0))
        axisPoint = rs.CurveStartPoint(self.axisX)
        self.axisOriginX = axisPoint[0]
        self.axisOriginY = axisPoint[1]
        self.axisOriginZ = axisPoint[2]
        for i in range(len(self.chartDataSeriesXY)):
            self.dataXScaled = self.chartDataSeriesXY[i][0]/self.axisXScale
            self.dataYScaled = self.chartDataSeriesXY[i][1]/self.axisYScale
            pointX = self.axisOriginX+self.dataXScaled
            pointY = self.axisOriginY+self.dataYScaled
            pointZ = self.axisOriginZ
            if self.options.pointStyle == "Circles":
                dataPoint = rs.AddCircle((pointX,pointY,pointZ),self.tickMod)

                if self.options.fillPoints == True:
                    dataPointHatch = rs.AddHatch(dataPoint,self.options.hatchName)
                    self.dataPoints.append((dataPoint,dataPointHatch))
                else:
                    self.dataPoints.append((dataPoint,None))
            else:
                dataPoint = rs.AddPoint(pointX,pointY,pointZ)
                self.dataPoints.append((dataPoint,None))
        for i in range(len(self.dataPoints)):
            if self.options.colorPoints == True:
                rs.ObjectColor(self.dataPoints[i][0],self.options.pointColor)
            if self.options.fillPoints == True:
                if self.dataPoints[i][1] != None:
                    rs.ObjectColor(self.dataPoints[i][1],self.options.pointHatchColor)
                    if self.options.hatchTransparency == True:
                        matIndex = rs.ObjectMaterialIndex(self.dataPoints[i][1])
                        rs.MaterialTransparency(matIndex,self.options.hatchTransparencyValue)

class RhinoGraphTwitter(Chart):
    options = Chart.options.add(
                                          timeLabel = "Sunday, 10/28/12, 00:00 EST",
                                          timeLabelLeftOffset = 0,
                                          timeLabelBottomOffset = 0,
                                          timeLabelSize = .15,
                                          timeLabelFont = "Arial",
                                          timeLabelFontStyle = 0,
                                          timeLabelJustification = None,
                                          timeLabelLayer = "Time Label",
                                          timeLabelColor = (80,80,80)
                                          )
    def __init__(self, rs, rsc, math, scene, **kwargs):
        Chart.__init__(self,rs,rsc,math,scene,**kwargs)
        self.options = RhinoGraphTwitter.options.push(kwargs)
        self.timeLabel = self.options.timeLabel
        self.bottomLeft = self.setBlCoord(self.options.timeLabelBottomOffset,self.options.timeLabelLeftOffset)
        self.timeLabelsObject = rs.AddText(self.options.timeLabel,
                                           self.bottomLeft,
                                           self.options.timeLabelSize,
                                           self.options.timeLabelFont,
                                           self.options.timeLabelFontStyle,
                                           self.options.timeLabelJustification)
        self.allObjects.append(self.timeLabelsObject)
        self.toLayer(self.timeLabelsObject,self.options.timeLabelLayer)
        rs.ObjectColor(self.timeLabelsObject,self.options.timeLabelColor)

class RhinoLayers:
    def __init__(self,rsc):
        self.layers = rsc.doc.Layers
    def filterLayersByPrefix(self,prefix):
        prefixLength = len(list(prefix))
        prefixList = list(prefix)
        self.stringLayers = []
        self.filteredLayers = []
        count = len(list(self.layers))-1
        for layer in self.layers:
            self.stringLayers.append(str(layer))
        for layer in self.stringLayers:
            if len(list(layer)) < prefixLength:
                pass
            elif len(list(layer)) > prefixLength:
                if prefixList != layer[:prefixLength]:
                      self.filteredLayers.append(layer)
                      count = len(self.filteredLayers)
        return self.filteredLayers

class Tweet3:
    def __init__(self,tweetLiteral):
        self.tweetLiteral = str(tweetLiteral)
        self.tweetDict = ast.literal_eval(self.tweetLiteral)
        self.date = self.tweetDict["created_at"]
        self.geo = self.tweetDict["geo"]
        self.source = self.tweetDict["source"]
        self.text = self.tweetDict["text"]
        self.image = None
        dateList = self.date.split(" ")
        day = int(dateList[1])
        timeList = dateList[4].split(":")
        hour = int(timeList[0])
        minute = int(timeList[1])
        day = day*24*60*60
        hour = hour*60*60
        minute = minute*60
        self.tweetTime = day+hour+minute
        if self.geo != None:
            self.coordinates = self.tweetDict["geo"]["coordinates"]

        else:
            self.coordinates = None

class Tweet2:
    def __init__(self,tweetLiteral,imageDir,xpath,url):
        self.tweetLiteral = str(tweetLiteral)
        self.tweetDict = ast.literal_eval(self.tweetLiteral)
        self.date = self.tweetDict["created_at"]
        self.geo = self.tweetDict["geo"]
        self.source = self.tweetDict["source"]
        self.text = self.tweetDict["text"]
        self.image = None
        dateList = self.date.split(" ")
        day = int(dateList[1])
        timeList = dateList[4].split(":")
        hour = int(timeList[0])
        minute = int(timeList[1])
        day = day*24*60*60
        hour = hour*60*60
        minute = minute*60
        self.tweetTime = day+hour+minute
        if self.geo != None:
            self.coordinates = self.tweetDict["geo"]["coordinates"]
            if self.source != None:
                        sourceList = list(self.source)
                        if sourceList[24] == "i":
                            if sourceList[25] == "n":
                                if sourceList[26] == "s":
                                    thisText = self.text
                                    thisTextList = thisText.split("http://")
                                    instagramUrl = "http://"+thisTextList[1]
                                    try:
                                        thisLink = url.urlopen(instagramUrl).read()

                                        thisPath = xpath.search(thisLink, "/html/body/div/div/div/div/section/div/div[2]/span[2]")


                                        thisList = [x for x in thisPath[0].split('"')]

                                        self.imagePath = imageDir + str(self.tweetTime) + " " + str(self.coordinates[0]) + " " + str(self.coordinates[1]) + " .jpg"

                                        testImage = open(self.imagePath, "wb")
                                        testImage.write(url.urlopen(thisList[3]).read())
                                        testImage.close()
                                    except:
                                        pass
        else:
            self.coordinates = None
 


class Tweet:
    def __init__(self, latitude, longitude, time):
        self.lat = latitude
        self.lon = longitude
        self.time = time
        
class Instagram:
    def __init__(self, latitude, longitude, time, fileName):
        self.lat = latitude
        self.lon = longitude
        self.time = time
        self.fileName = fileName

class WeatherStation:
    def __init__(self, usafID, ncdcID, latitude, longitude, measurements):
        self.usafID = usafID
        self.ncdcID = ncdcID
        self.lat = latitude
        self.lon = longitude
        self.measurements = measurements
        self.maxTime = 0
        for i in range(len(measurements)-1):
            if self.measurements[i].time < self.measurements[i+1].time:
                self.maxTime = self.measurements[i+1].time
        self.minTime = self.maxTime
        for i in range(len(measurements)-1):
            if self.measurements[i].time < self.minTime:
                self.minTime = self.measurements[i].time
    
class WeatherStationData:
    def __init__(self, usafID, ncdcID, time, direction, speed):
        self.usafID = usafID
        self.ncdcID = ncdcID
        self.time = time
        self.direction = direction
        self.speed = speed

def UtilsTextToList(path, delimitedHow = False, itemType = False, header = 0):
    textFile = open(path, "r")
    fileLines = textFile.readlines()
    fileLines = fileLines[header:]
    if delimitedHow != False:
        if itemType != False:
            textFileRead = [[itemType(x) for x in line.split(delimitedHow)] for line in fileLines]
            return textFileRead
        elif itemType == False:
            textFileRead = [[x for x in line.split(delimitedHow)] for line in fileLines]
            return textFileRead
    elif delimitedHow == False:
        return fileLines      
    textFile.close()

def UtilsDateToSeconds(yearMonthDay,hourMinutes):
    #yearMonthDay = int(yearMonthDay)
    yearMonthDay = list(yearMonthDay)
    year = yearMonthDay[0:4]
    year = int("".join(year))
    month = yearMonthDay[4:6]
    month = int("".join(month))
    day = yearMonthDay[6:8]
    day = int("".join(day))
    daySeconds = day*24*60*60
    hour = int(hourMinutes[:2])
    minute = int(hourMinutes[2:])
    hourSeconds = hour*60*60
    minuteSeconds = minute*60
    totalSeconds = daySeconds+hourSeconds+minuteSeconds
    #print totalSeconds
    return totalSeconds
        
def InstallTest():
    return "It worked!  You can now start working with charted."

def Version():
    return "Version 1.0"


