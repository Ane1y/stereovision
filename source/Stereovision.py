import sys
from depth_map import DepthMap
from argparse import ArgumentParser
from calibration import Calibrator
from photo_sequence import PhotoSequence

import params


def parse_args(args):
    parser = ArgumentParser(description='Application to calibrate stereopair and to build depth map')
    parser.add_argument("-c", "--calib", action='store_true',
                        help="choose calibration mode")
    parser.add_argument("-s", "--shoot", action='store_true', help='start taking calibration photos')
    parser.add_argument("-d", "--depthmap", action='store_true',
                        help="build depth map")
    parser.add_argument("-p", "--parameters", action='store_true',
                        help="correct parameters for depth map")
    return parser.parse_args(args), parser

if __name__ == "__main__":
    args, parser = parse_args(sys.argv[1:])
    if args.calib:
        calib = Calibrator()
        calib.take_photos()
        calib.calibrate_camera()
        calib.show_rectified_pair(params.TOTAL_PHOTOS)
    elif args.depthmap:
        depthMap = DepthMap()
        image = '../scenes/photo.png'
        rectified_pair, disparity = depthMap.build_depth_map(image)
        print(disparity.max())
        depthMap.draw_plot(rectified_pair, disparity)
        # depthMap.highlight_borders()
    elif args.shoot:
        seq = PhotoSequence()
    elif args.parameters:
        print("depth map with parameters")
    else:
        parser.print_help()