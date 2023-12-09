import h3

def calc_distance(coords_1, coords_2):
    return h3.point_dist(coords_1, coords_2, unit='m')
#
# coords_1 = (38.2732173, 67.8639645)
# coords_2 = (38.0224176, 67.7800878)
# print(calc_distance(coords_1,coords_2))