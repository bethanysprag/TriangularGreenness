import os
import tgi


def test_main():
    output = 'test/testImage_green.tif'
    if os.path.exists(output):
        os.remove(output)
    tgi.main('test/testImage.tif', output, rgb=[0,1,2])
    assert os.path.exists(output)


