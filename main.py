import data
import search

import numpy as np



results = search.depthSearch(np.array([0,2,3,1,4,5,6,7,8]))

data.writeData(0, "depth", results[1], results[2], results[3])