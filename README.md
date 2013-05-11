#Charted

The goal is to provide an extension to Rhino's API that allows for the creation of both simple and complex
visualizations, as well as offering the possibility of creating novel visualizations that would
otherwise be difficult with other popular javascript/svg based tools and frameworks.

The design goal of this code is to supply objects that are very featureful and at the same time 
unobtrusive and easy to implement.  This is accomplished through a delegation pattern that makes 
class objects behave and feel like javascript's prototype pattern.

##Installation and dependencies:

  * For now, for ease of getting going, I am including all dependencies not part of the standard library.
  * Clone into your standard CPython site-packages directory.

## Getting started:

  * Open a new session of Rhino and maximize the top view.
  * Enter the command "EditPythonScript".
  * In Rhino's Python editor, go to "Tools", "Options", then under the "Script Engine" tab, check the box for "Enable Frames".  None of this will work if
you skip this step.

  * Import the following needed modules:

```python
    import 

```


## More about delegation and some background:

A while back I had the need to create a lot of scatter plots that were varying over time, with the 
intent to eventually composite them together into an animation.  If you imagine writing a class to describe 
scatter plot, you would be immediately confronted with a problem.  There are many possible ways to draw
such a chart, and an object meant to encapsulate that concept will have to be constructed with just as many 
arguments.

When I started researching this problem I came across this on stackoverflow:  http://stackoverflow.com/questions/11702437/where-to-keep-options-values-paths-to-important-files-etc/11703813#11703813

The author calls this problem "configuration sprawl", and that's a good description.

```python
class RhinoGraphChart:
    options = RhinoGraphScene.options.add(
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





