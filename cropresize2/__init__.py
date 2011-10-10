#!/usr/bin/env python

import sys
try:
    import Image
except ImportError:
    from PIL import Image

# Crop modes
CM_AUTO, CM_FORCECROP, CM_NOCROP = range(3)

def crop_resize(image, size, exact_size=False, crop_mode=CM_AUTO):
    """
    Crop out the proportional middle of the image and set to the desired size.
    * image: a PIL image object
    * size: a 2-tuple of (width,height);  at least one must be specified
    * exact_size: whether to scale up for smaller images
    If the image is bigger than the sizes passed, this works as expected.
    If the image is smaller than the sizes passed, then behavior is dictated
    by the ``exact_size`` flag.  If the ``exact_size`` flag is false,
    the image will be returned unmodified.  If the ``exact_size`` flag is true,
    the image will be scaled up to the required size.
    """
    assert size[0] or size[1], "Must provide a width or a height"

    size = list(size)

    image_ar = image.size[0]/float(image.size[1])
    new_image_ar = size[0]/float(size[1])
    _crop = (crop_mode == CM_FORCECROP) or \
            (crop_mode == CM_AUTO and ((new_image_ar / 2 > image_ar) or (new_image_ar * 2 < image_ar)))

    if _crop:
        if image_ar > new_image_ar:
            # trim the width
            xoffset = int(0.5*(image.size[0] - new_image_ar*image.size[1]))
            image = image.crop((xoffset, 0, image.size[0]-xoffset, image.size[1]))
        elif image_ar < new_image_ar:
            # trim the height
            yoffset = int(0.5*(image.size[1] - image.size[0]/new_image_ar))
            image = image.crop((0, yoffset, image.size[0], image.size[1] - yoffset))
    else:
        if image_ar > new_image_ar:
            size[1] = int(image.size[1]*size[0]/float(image.size[0]))
        else:
            size[0] = int(image.size[0]*size[1]/float(image.size[1]))

    return image.resize(size, Image.ANTIALIAS)

def main():
    from optparse import OptionParser
    parser = OptionParser('%prog [options] image1.png [image2.jpg] [...]')
    parser.add_option('-W', '--width',
                      help="desired width of image in pixels")
    parser.add_option('-H', '--height',
                      help="desired height of image in pixels")
    parser.add_option('-e', '--exact-size', dest='exact',
                      action='store_true', default=False,
                      help="scale up images smaller than specified")
    parser.add_option('-d', '--display', dest='display',
                      action='store_true', default=False,
                      help="display the resized images (don't write to file)")
    parser.add_option('-c', '--force-crop', dest='force_crop',
                      action='store_true', default=False,
                      help="force crop image even normal ratio")
    parser.add_option('-O', '--file', dest='output',
                      help="output to a file, stdout otherwise [1 image only]")
    (options, args) = parser.parse_args()

    # print arguments if files not given
    if not args:
        parser.print_help()
        sys.exit()

    # get the desired size
    try:
        width = int(options.width)
    except TypeError:
        width = None
    try:
        height = int(options.height)
    except TypeError:
        height = None

    # asser that we have something to do with the image
    if not options.display:
        if len(args) > 1:
            raise NotImplementedError # XXX

    # resize the images
    for arg in args:
        image = Image.open(arg)
        new_image = crop_resize(image, (width, height), options.exact, options.force_crop and CM_FORCECROP or CM_AUTO)
        if options.display:
            new_image.show()
        else:
            if len(args) == 1:
                # output
                if options.output:
                    new_image.save(options.output)
                else:
                    sys.stdout.write(new_image.tostring(image.format))

if __name__ == '__main__':
    main()
