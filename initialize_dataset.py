import numpy as np
import os
similarity = np.zeros(1, dtype=int)
npload = np.save(os.getcwd()+'\\..\\Recommend.npy', similarity)
print()