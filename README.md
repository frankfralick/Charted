#Charted


Charted is a Python framework for visualizing data in Rhinoceros 3d.  The goal is to provide an 
extension to Rhino's API that allows for the creation of both simple and complex
visualizations, as well as offering the possibility of using Rhino's powerful modelling/drawing capabilities in creating novel visualizations that would
otherwise be difficult with other popular JavaScript/SVG based tools and frameworks.

Charted aims to supply objects that are very featureful and at the same time 
unobtrusive and easy to implement.  This is accomplished through a delegation pattern that makes 
class objects behave and feel like JavaScript's prototype pattern.

##Installation and dependencies:

  * For now, for ease of getting going, I am including all dependencies not part of the standard library.
  * Clone Charted into your standard CPython site-packages directory.

### Getting started:

  * Open a new session of Rhino and maximize the top view.
  * Enter the command "EditPythonScript".
  * In Rhino's Python editor, go to "Tools", "Options", then under the "Script Engine" tab, check the box for "Enable Frames".  None of this will work if
you skip this step.

![Enable Frames](https://raw.github.com/frankfralick/Charted/master/images/FramesEnabled.PNG)

  * Import the following needed modules:

```python
import rhinoscriptsyntax as rs
import scriptcontext as rsc
import sys

#Add your site-packages directory to the path if you need to.
sys.path.append("C:\\Python27\\Lib\\site-packages\\")
from charted import charted
import operator

```

### Making a Scene and a taste of the prototype pattern:

* Next we need to create an instance of the Scene class.  The scene object encapsulates the idea of the visible area that will be drawn, where it is, what the resolution will be, and how many units wide at that resolution the drawing area will be.      
* The scene, like the other classes in Charted, defines defaults.   Currently the attributes that the Scene class defines are: 
  * sceneBottomLeft
  * sceneWidth 
  * sceneResolution
  * sceneBorderVisible
  * sceneLayerName

* The instance of the Scene class the we create will be passed to any chart we might want to create within the scene, so it will always be a first step.  Create a scene object, create a new chart object, and pass in the scene. 

```python
scene = charted.Scene(rs)
```
* The Scene class has several configurable attributes that have reasonable defaults that you can choose to overide. 
* If you run what we have so far, it won't look like much has happened, but we have created a boundary that is 100 units wide (using the default unit of the file), that has an aspect ratio of 1920 x 1080, and you have two new layers.  One called "Scene Boundary" that will be off by default, and a current layer called "Charted".  The bottom left corner of the scene boundary is placed at (0,0,0). 
* Notice that we have only need to pass in rhinoscriptsyntax.  All of the basic aspects of the Scene object can be overridden.  Here is an example with all of Scene's options shown:
```python
scene = chart.Scene(rs, sceneBottomLeft =(10,10,10), sceneResolution = (640,480), 
                        sceneWidth = 300, sceneBorderVisible = True, sceneLayerName = "Test Scene")
```

### A simple scatter chart
* Create a fresh file or undo what has already been done.  
* An important aspect of Charted is that all attributes of class objects come with defaults, even data sets.  You create objects that override some aspects of the defaults and the rest shines through.  When we begin to 


## More about delegation and some background:

A while back I had the need to create a lot of scatter plots that were varying over time, with the 
intent to eventually composite them together into an animation.  If you imagine writing a class to describe 
scatter plot, you would be immediately confronted with a problem.  There are many possible ways to draw
such a chart, and an object meant to encapsulate that concept will have to be constructed with just as many 
arguments.

When I started researching this problem I came across this on stackoverflow:  http://stackoverflow.com/questions/11702437/where-to-keep-options-values-paths-to-important-files-etc/11703813#11703813

The author calls this problem "configuration sprawl", and that's a good description.

```python
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

```


=== Features: ===

*Support for basic chart types that aren't terrible (I'm looking at you pie chart) like scatter, bar, histogram, and more to come.
*Support for animating time-series data.
*Support for geospatial data visualizations.
*Utility functions for obtaining and parsing Twitter and Instagram data.





