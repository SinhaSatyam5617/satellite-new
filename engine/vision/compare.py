import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from engine.vision.yolo_seg import run_yolo
from engine.vision.object_stats import get_counts
from engine.vision.classifier import map_to_categories, YOLO_TO_CATEGORY
from engine.vision.yolo_seg import model


def compare_images(before_path, after_path):

    before_res = run_yolo(before_path)
    after_res  = run_yolo(after_path)

    before_counts = get_counts(before_res)
    after_counts  = get_counts(after_res)

    before_cat = map_to_categories(before_counts, model)
    after_cat  = map_to_categories(after_counts, model)

    return before_cat, after_cat