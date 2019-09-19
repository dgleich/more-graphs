import os

import numpy as np
import cv2 as cv

from sklearn.neighbors import KDTree

def alter_file_name(file, insert,delim='.', ignore_post_fix = False):
    prefix, postfix = file.split(delim)
    if ignore_post_fix:
        return prefix + insert
    else:
        return prefix + insert + postfix

def get_key_points(image_file,sift_config = None, mask=None):
    """-------------------------------------------------------------------------
      Helper function made from the open cv tutorial, used to get the keypoints
      from the OpenCV SIFT implementation. Configuration dictionary can be
      passed in, but defaults will be used otherwise. Mask can be passed in to
      only compute the keypoints in a specified region.
    -------------------------------------------------------------------------"""
    img = cv.imread(image_file)
    #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if sift_config:
        sift = cv.xfeatures2d.SIFT_create(**sift_config)
    else:
        sift = cv.xfeatures2d.SIFT_create()
    return sift.detect(img, None)

def make_wheres_waldo_graphs(map_files_location):
    """-------------------------------------------------------------------------
        Creates a connected epsilon graph for the SIFT features found in the
      Wheres Waldo maps and the characters. an initial search radius of 25
      pixels is used, if a keypoint doesn't have any nearest neighbors within
      that distance, the radius is increased. The resulting graph's edge weights
      are weighted by the distance between the features in the document.

      Graphs are saved in a sift_object folder,
    -------------------------------------------------------------------------"""
    search_radius = 25

    sift_object_location = map_files_locations + "/sift_objects"

    if not os.path.exists(sift_object_location):
        os.mkdir(sift_object_location)

    for file in [file for file in os.listdir(map_files_location) if ".jpg" in file]:

        matrix_non_zeros = []

        key_points = get_key_points(map_files_location + '/' + file)
        n = len(key_points)

        #floor pixel locations, swap i and j
        index_map = [(int(kp.pt[1]),int(kp.pt[0])) for kp in key_points]

        pixel_locations = np.empty((len(key_points), 2))
        for i, kp in enumerate(key_points):
            pixel_locations[i, 0] = kp.pt[0]
            pixel_locations[i, 1] = kp.pt[1]

        tree = KDTree(pixel_locations, leaf_size=10)
        for i in range(n):
            while True:
                # look for nearby neighbors in the picture.
                ind, dist = \
                    tree.query_radius(pixel_locations[i, :].reshape(1, -1),
                                      r=search_radius, return_distance=True)
                if len(ind) == 0:
                    #increase radius and try again if none found.
                    search_radius += 5
                else:
                    break

            for j in range(ind.shape[0]):
                if i != ind[0][j]:
                    matrix_non_zeros.append(([i, ind[0][j]], 1))

        print(f"final search radius is {search_radius}")

        m = len(matrix_non_zeros)*2
        matrix_output_file = alter_file_name(file, '.smat',
                                  ignore_post_fix=True)

        with open(sift_object_location +'/' + matrix_output_file,'w') as wptr:
            wptr.write("{0:d}\t{1:d}\t{2:d}\n".format(n, n, m))
            for ([i,j],w) in matrix_non_zeros:
                wptr.write("{0:d}\t{1:d}\t{2:d}\n".format(i, j, w))
                wptr.write("{0:d}\t{1:d}\t{2:d}\n".format(j, i, w))

        mapping_file = alter_file_name(file,".xy",
                                       ignore_post_fix=True)
        with open(sift_object_location + '/' + mapping_file,'w') as f:
            for i,j in index_map:
                f.write("{0:d}\t{1:d}\n".format(i, j))

        print("finished making SIFT graph for {}\n".format(file))


if __name__ == "__main__":
    map_files_location = None
    make_wheres_waldo_graphs(map_files_location)
