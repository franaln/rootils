from .utils import guess_binning
from .utils import array_to_hist
from .utils import array_to_graph

from .plots import lines
from .plots import hists
from .plots import hists_ratio
from .plots import corr
from .plots import confusion_matrix


try:
    del plots
except:
    pass

try:
    del utils
except:
    pass
