import os
import tgi

imgOut = 'test/testImage_green.tif'
imgIn = 'test/testImage.tif'


def test_readImage():
    img = tgi.readImage(imgIn)
    #assert img is not None
    assert img is not None
    img = None


def test_ApplyColorRamp():
    ct = tgi.ApplyColorRamp(imgOut, stdStretch=2)
    assert imgOut is not None


def test_tgi():
    img = tgi.readImage(imgIn)
    green = tgi.TriangularGreenness(img, rgb=[0, 1, 2])
    assert green is not None
    green=None


def test_main():
    if os.path.exists(imgOut):
        os.remove(imgOut)
    tgi.main(imgIn, imgOut, rgb=[0,1,2])
    assert os.path.exists(imgOut)


def test_parse_args():
    args=['-i', 'inputImage.tif', '-o', 'outputImage.tif', '-b', '1', '2', '3']
    arguments = tgi.parse_args(args)
    assert arguments.input == 'inputImage.tif'
