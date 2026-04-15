import numpy as np

# Better mapping for cityscapes
VEGETATION_CLASSES = [8]     # vegetation
BUILDING_CLASSES = [2]       # building
ROAD_CLASSES = [0]           # road
WATER_CLASSES = []           # not present

def calculate_stats(mask):
    total = mask.size

    vegetation = np.isin(mask, VEGETATION_CLASSES).sum() / total
    building = np.isin(mask, BUILDING_CLASSES).sum() / total
    road = np.isin(mask, ROAD_CLASSES).sum() / total
    water = 0

    return {
        "vegetation": vegetation,
        "building": building,
        "road": road,
        "water": water
    }