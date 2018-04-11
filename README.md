# TriangularGreeness
Implements a simple triangular greenness index on true color imagery.  The index was the result of a study to create an index  that is sensitive to differences in leaf chlorophyll content at leaf and canopy scales, when limited to true color.

## Usage

While TriangularGreenness can be used as a Python library, the more common use is to use the Command Line Interface (CLI).

```
$ python tgi.py 
usage: bfalg-ndwi -i INPUT [-b BANDS BANDS] [--outfile OUTFILE]
                  [--basename BASENAME] [--l8bqa L8BQA] [--coastmask]
                  [--minsize MINSIZE] [--close CLOSE] [--simple SIMPLE]
                  [--verbose VERBOSE] [--version]

Beachfront Algorithm: NDWI (v1.0.3)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input image (Required, Must contain red, green, and 
                        blue bands) (default: None)
  -b BANDS BANDS, --bands BANDS BANDS
                        Band numbers for Red, Green, and Blue bands 
                        (default: [0, 1, 2])
  -o, OUTFILE, --outfile OUTDIR       
                        Required, Output image name.  Will contain 8-bit 
                        stretched values indicating liklihood of containing 
                        green vegetation, with a standard color ramp applied
                        (default: None )
