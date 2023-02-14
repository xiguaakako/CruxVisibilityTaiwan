import numpy as np
import timeit
from math import atan, pi

# Reading raster file 
fn = 'C:/Users/邱巖盛/Desktop/不分幅_全台及澎湖/dem_20m.tif' # .tif file path
fi = QFileInfo(fn)
fname = fi.baseName()

# Adding layer
rlayer = iface.addRasterLayer(fn, fname)

# Value getter and setter, with numbers of 'row' and 'column' being parameters 
dataProvider = rlayer.dataProvider()
dataProvider.setEditable(enabled=True) 
block = dataProvider.block(1, rlayer.extent(), rlayer.width(), rlayer.height())
width = rlayer.width() # Total number of columns
height = rlayer.height() # Total number of rows
def getPixelVal(_row, _col):
    return block.value(_row, _col)
def setPixelVal(_row, _col, _val):
    block.setValue(_row, _col, float(_val))

# Function converting column values into a numpy array
def convertColValToNpArr(_col):
    colValArr = np.zeros(height)
    for row in range(height):
        colValArr[row] = getPixelVal(row, _col)
    return colValArr

# An 2D array containing all column value arrays, 0 if a column hasn't been converted into an array yet
colValArrArr = [0] * width

# Function converting deg, min, sec to rad
def DegMinSecToRad(_deg, _min, _sec):
    return (_deg + _min / 60 + _sec / 3600) * pi / 180


# Function converting numbers of 'row' and 'column' to TM2 coordinates

# Function converting TM2 coordinates to numbers of 'row' and 'column'



# Function giving the Acrux altitude at assigned TM2 coordinates
AcruxMaxAlt = DegMinSecToRad(2, 0, 0) # Temporary Constant Value

# Function giving the maximum altitude angle of south mountains (pixel)
def southMtShadingAltAngle(_row, _col):
    if _row == height-1: # If reaching the bottom of the map no need to proceed
        return 0.0 
    colValArr = colValArrArr[_col] # Reading the column Value
    currentLocAlt = colValArr[_row]  # Altitude of current location 
    scanningArrI = colValArr[(_row+1):height] # Slicing part that is souther than cur. loc. of the array
    maxMtAltIdx = np.argmax(scanningArrI) # Scanning the tallest mountain (pixel) and returning its index
    scanningArrII = scanningArrI[:maxMtAltIdx+1] # Slicing part that is norther than the highest mountain (pixel) of the array
    ### Note that lower mountains (pixels) souther than the highest mountain never create a higher shade. ### 
    southMtDistArr = 20 * np.arange(1, scanningArrII.size+1) # Distance array to south mountains (pixels), [20, 40, 60, ...] due to 20-meter-wides
    southDeltaAltArr = scanningArrII - currentLocAlt # Altitude difference between south mountains (pixels) and cur. loc.
    southMtPeakSlopeArr = southDeltaAltArr/southMtDistArr # The slope between cur.loc. and south mountains (pixels)
    maxSouthMtPeakSlope = np.amax(southMtPeakSlopeArr) # The maximum of the slope 
    return atan(maxSouthMtPeakSlope) # Converting slope into altitude angle
    
# Function giving the Acrux visibility at assigned location, 1 if visible and 0 else
def AcruxVisibility(_row, _col):
    visibility = 0
    southMtShadingAltAngleHere = southMtShadingAltAngle(_row, _col)
    # AcruxMaxAlt = ... the function
    if southMtShadingAltAngleHere < AcruxMaxAlt:
        visibility = 1
    return visibility

# Function printing the visibility map 
def printAreaAcruxVisibilityMap(_area):
    global colValArrArr
    # Setting the pixel value, 
    # -1 if the location's altitude is below -1 m,
    # 0 if Acrux is invisible there,
    # 1 if Acrux is visible there.
    for col in range(_area[0][0], _area[0][1]): 
        # Check if the column value array exists. If it exists, utilize it, else make it  
        colValArr = colValArrArr[col] 
        if type(colValArr) is not np.ndarray:
            colValArrArr[col] = convertColValToNpArr(col)
            colValArr = colValArrArr[col]
        # Start value setting
        if np.any(colValArr): # Checking if the coulmn is a zero array
            for row in range(_area[1][0], _area[1][1]):
                if colValArr[row] > -1:
                    if AcruxVisibility(row, col):
                        setPixelVal(row, col, 1)
                    else:
                        setPixelVal(row, col, 0)
                else:
                    setPixelVal(row, col, -1)
    # Writing new data
    dataProvider.writeBlock(block, 1)
    dataProvider.setEditable(enabled=False)
    
    # Dictionary of colors
    colorDict = {'white':'#ffffff', 'red':'#fd4431', 'black':'#000000'}

    # A list specifying the choropleth color shader rules
    lst = [ QgsColorRampShader.ColorRampItem(-1, QColor(colorDict['white'])),
            QgsColorRampShader.ColorRampItem(0, QColor(colorDict['white'])), 
            QgsColorRampShader.ColorRampItem(1, QColor(colorDict['red'])),
            QgsColorRampShader.ColorRampItem(3947, QColor(colorDict['black']))]

    # Shading, rendering
    myRasterShader = QgsRasterShader()
    myColorRamp = QgsColorRampShader()
    myColorRamp.setColorRampItemList(lst)
    myColorRamp.setColorRampType(QgsColorRampShader.Discrete)
    myRasterShader.setRasterShaderFunction(myColorRamp)
    myPseudoRenderer = QgsSingleBandPseudoColorRenderer(dataProvider, 1, myRasterShader)
    myPseudoRenderer.setOpacity(0.6) # Opacity (transparency can be set here)
    rlayer.setRenderer(myPseudoRenderer)
    rlayer.triggerRepaint

    '''
    # Checking current altitude maximum and minimum
    stats = dataProvider.bandStatistics(1, QgsRasterBandStats.All)
    min = stats.minimumValue
    max = stats.maximumValue
    print(min, max)
    '''

# Range of the area, ((left boundary, right boundary), (top boundary, bottom boundary))
area = ((0, width), (0, height))

# Map print timer
start = timeit.default_timer()
printAreaAcruxVisibilityMap(area)
stop = timeit.default_timer()

# Printing result in the console
print('====================================')
print('MAP PRINT RESULT!')
print()
print('Map in column {0:05d}~{1:05d} and row {2:05d}~{3:05d} is printed.'.format(area[0][0], area[0][1], area[1][0], area[1][1]))
print('Time used: {0:5.3f}s'.format(stop - start))    
print('*** Warning: If precession in the same columns is needed, only souther maps can be printed. ***')
