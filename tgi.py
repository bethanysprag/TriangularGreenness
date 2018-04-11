import sys
import os
import argparse
import logging
import numpy as np

try:
    from osgeo import gdal, osr
except:
    import gdal, osr

logger = logging.getLogger(__name__)


def parse_args(args):
    """ Parse arguments for the NDWI algorithm """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--input', help='Input image', required=True)
    parser.add_argument('-b', '--bands', help='Band numbers for Red,Green,and Blue bands', default=[0, 1, 2], nargs=3, type=int)

    parser.add_argument('-o', '--outfile', required=True, help='Output Filename', default='')
    return parser.parse_args(args)

def readImage(imgPath):
    """Reads geotiff into memory """
    logger.info('Reading img: %s' % imgPath)
    i1_src = gdal.Open(imgPath)
    i1 = i1_src.ReadAsArray()
    if i1.ndim > 2:
        i1 = np.rollaxis(i1, 0, 3)
    i1_src = None
    return i1


def saveArrayAsRaster(rasterfn, newRasterfn, array):
    """Saves numpy array as geotif"""
    logger.info('Saving image as %s' % newRasterfn)
    raster = gdal.Open(rasterfn)
    # nBands = raster.count
    checksum = array.ndim
    if checksum == 3:
        temp = array.shape
        nBands = temp[2]
    else:
        nBands = 1
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    driver = gdal.GetDriverByName('GTiff')
    if array.dtype == 'uint8':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Byte)
    elif array.dtype == 'int16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Int16)
    elif array.dtype == 'float16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Float32)
    elif array.dtype == 'float32':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Float32)
    elif array.dtype == 'int32':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Int32)
    elif array.dtype == 'uint16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_UInt16)
    else:
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_CFloat64)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0,
                               pixelHeight))
    if nBands > 1:
        for i in range(1, (nBands + 1)):
            outband = outRaster.GetRasterBand(i)
            x = i-1
            outband.WriteArray(array[:, :, x])
    else:
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


def Atebit(img):
    """Stretches and converts image array to 8-bit"""
    logger.info('Converting image to 8-bit')
    imgMin = img.min()
    offset = (0-imgMin)
    img = img + offset
    img = ((img * 1.0)/img.max()) * 255
    img = img.astype('uint8')
    return img


def xO_TGI(inImg, rgb=None):
    """Estimates leaf chlorophyll content based on true color imagery."""
    logger.info('Calculating Triangular Greenness Index')
    try:
        if rgb is None:
            print 'Setting default rgb bands'
            rgb = [0,1,2]
        r,g,b = rgb
        x,y,z = inImg.shape
        inImg = Atebit(inImg)
        dtype= inImg.dtype
        R = inImg[:,:,r].astype('float64')
        G = inImg[:,:,g].astype('float64')
        B = inImg[:,:,b].astype('float64')
        _TGI = (-1) * 0.5 * ((200*(R-G))-(100 * (R-B)))
        return Atebit(_TGI)
    except:
        logger.error('Error: unable to calculate triangular greenness index')
        sys.exit(1)


def ApplyColorRamp(imgPath, ct=None, colorScheme=None, _min=None, _max=None, stdStretch=None):
    """Applys color ramp to geotif"""
    logger.info('Applying color ramp to output image')
    rs = gdal.Open(imgPath, gdal.GA_Update)
    rb = rs.GetRasterBand(1)
    if ct is None:
        condition = 0
        if _min is not None:
            if _max is not None:
                condition = 1
        if condition != 1:
            img = rb.ReadAsArray()
            imgMin = img.min()
            imgMax = img.max()
            if stdStretch is not None:
                stdStretch = float(stdStretch)
                _STD = img.std()
                _mean = img.mean()
                _min = _mean - (stdStretch * _STD)
                _max = _mean + (stdStretch * _STD)
                if _min < img.min():
                    _min = img.min()
                if _max > img.max():
                    _max = img.max()
            else:
                _min = imgMin
                _max = imgMax
        _min = int(_min)
        _max = int(_max)
        if colorScheme is None:
           colorScheme = 'GreenYellowRed'
        colorRamps = {'GreenYellowRed': [(0,128,0),(0,255,0),(255,255,0),(255,0,0),(128,0,0)],
                      'PR': [(0,0,143),(0,0,255),(0,255,255),(255,255,0),(255,0,0),(128,0,0)],
                      'BlueRed':[(0,0,143),(0,0,255),(255,0,0),(128,0,0)],
                      'RedBlue':[(128,0,0),(255,0,0),(0,0,255),(0,0,128)],
                      'YellowOrangeRed':[(128,128,0),(255,255,0),(255,128,0),(255,0,0),(128,0,0)],
                      'OrangeRedMagentaBlue': [(200,100,0),(255,0,0),(255,0,255),(0,0,200)],
                      'RedYellowCyanBlue' : [(255,0,0),(255,255,0),(0,255,255),(0,0,255)],
                      'GreenCyanBlue' : [(0,255,0),(0,255,255),(0,0,255),],
                      'GreenCyanBlue2' : [(0,50,0),(0,128,128),(0,0,255),],
                      'Greens' : [(0,50,0),(0,100,0),(0,150,0),(0,200,0),(0,255,0)],
                      'Blues' : [(0,0,50),(0,0,100),(0,0,150),(0,0,200),(0,0,255)],
                      'Reds' : [(50,0,0),(100,0,0),(150,0,0),(200,0,0),(255,0,0)],
                      'Rainbow' : [(255,0,255),(0,0,255),(0,255,255),(0,255,0),(255,255,0),(255,128,0),(255,0,0)],
                      'Grey' : [(0,0,0),(255,255,255)],
                      'Earth' : [(80,45,10),(134,71,25),(150,125,25),(100,128,0),(0,100,25)],
                      'Cool' : [(0,255,255),(0,150,255),(75,0,75),(255,0,255)],
                      'Terrain' : [(0,0,75),(0,0,255),(0,255,128),(255,255,175),(150,80,20),(80,45,10)],
                      'PH_Green': [(215,25,28),(253,174,97),(255,255,191),(166,217,106),(26,150,65)]
                      }
        try:
            Scheme = colorRamps[colorScheme]
        except:
            Scheme = colorRamps['GreenYellowRed']
        print colorScheme, Scheme
        colorScheme = Scheme
        colortable = gdal.ColorTable()
        _range = _max - _min
        binSize = _range/(len(colorScheme)-1)
        binValues = []
        for i in range(len(colorScheme)):
            temp = _min + (i*binSize)
            binValues.append(int(temp))
        for i in range(int(_min),_max):
            colortable.SetColorEntry(i,colorScheme[0])
        for i in range(len(binValues)-1):
            colortable.CreateColorRamp(binValues[i],colorScheme[i],binValues[i+1],colorScheme[i+1])
        for i in range(binValues[-1],int(_max)):
           colortable.SetColorEntry(i,colorScheme[-1])
        
    rb.SetColorTable(colortable)
    rb.FlushCache()
    rs.FlushCache()
    rs = None
    return #colortable


def main(image_path, out_path, rgb=None):
    img = readImage(image_path)
    #Calculate Triangular Greenness
    green = xO_TGI(img, rgb=rgb)
    #Save output array to file
    saveArrayAsRaster(image_path, out_path, green)
    #Apply ColorRamp
    ApplyColorRamp(out_path, colorScheme='PH_Green', _min=0, _max=255, stdStretch=None)


def usage():
    print("""
          Usage:
          tgi -i in_raster -o out_raster -b R,G,B default 0,1,2
          """
          )
    sys.exit(1)


if __name__ == '__main__':

    img_path = None
    out_path = None
    rgb = [0,1,2]

    args = parse_args(sys.argv[1:])
    """
    for i in range(len(sys.argv)-1):
        arg = sys.argv[i]
        if arg == '-i':
            img_path = sys.argv[i+1]
        elif arg == '-o':
            out_path = sys.argv[i+1]
        elif arg == '-r':
            rgb = sys.argv[i+1]
            rgb = int(rgb.split(','))
    """
    img_path = args.input
    out_path = args.outfile
    rgb = args.bands
    if img_path is None:
        usage()
    if out_path is None:
        usage()

    main(img_path, out_path, rgb=rgb)
    sys.exit(0)
