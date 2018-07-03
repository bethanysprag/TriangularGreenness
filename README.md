# TriangularGreeness
Implements a simple triangular greenness index on true color imagery.  The index was the result of a study to create an index  that is sensitive to differences in leaf chlorophyll content at leaf and canopy scales, when limited to true color.

Based on research cited in:
*Hunt, E.R., Daughtry, C.S.T., Eitel, J.U.H., Long, D.S., 2011. Remote sensing leaf chlorophyll
content using a visible band index. Agronomy Journal 103, 1090–1099.*

## Usage

While TriangularGreenness can be used as a Python library, the more common use is to use the Command Line Interface (CLI).

```
$ python tgi.py 
usage: bfalg-ndwi -i INPUT -o OUTFILE [-b BANDS BANDS]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input image (Required, Must contain red, green, and 
                        blue bands) (default: None)
  -b BANDS BANDS BANDS, --bands BANDS BANDS BANDS
                        Band numbers for Red, Green, and Blue bands 
                        (default: [0, 1, 2])
  -o, OUTFILE, --outfile OUTDIR
                        Required, Output image name.  Will contain 8-bit 
                        stretched values indicating liklihood of containing 
                        green vegetation, with a standard color ramp applied
                        (default: None )
```

### Docker
A Dockerfile and a docker-compose.yml are included for ease of development. The built docker image provides all the system dependencies needed to run the library. The library can also be tested locally, but all system dependencies must be installed first, and the use of a virtualenv is recommended.

To build the docker image use the included docker-compose tasks:

    $ docker-compose build

Which will build an image called that can be run

    # this will run the image in interactive mode (open bash script)
    $ docker-compose run bash

    # this willl run the tests using the locally available image
    $ docker-compose run test
