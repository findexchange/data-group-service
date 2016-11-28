from scipy.spatial import distance
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import Counter


def get_tags(data):
	tags = data.tags.drop_duplicates().reset_index(drop = True)
	return tags