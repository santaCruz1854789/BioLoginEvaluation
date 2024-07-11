# Rounding number
ROUNDING_NUMBER = 7

# Number of TOTAL IDENTITIES
TOTAL_IDENTITIES = 840

# Number of ENROLLED IDENTITIES
ENROLLED_IDENTITIES = 700

# Number of IMPOSTORS
IMPOSTORS_IDENTITES = TOTAL_IDENTITIES - ENROLLED_IDENTITIES

# Number of templates for each enrolled entity
ENROLLED_TEMPLATES = 3

# Number of probes for each probe
PROBES_ATTEMPTS = 3

# The path to the Gallery directory
GALLERY_PATH = "./Eval_Dataset/gallery"

# The path to the Probe directory
PROBES_PATH = "./Eval_Dataset/probes"

# Name of the distance matrix
DISTANCE_MATRIX_NAME = "distance_matrix.csv"

# Threshold constants
MIN_THRESHOLD = 0.0
MAX_THRESHOLD = 1.0
THRESHOLD_STEP = 0.01

# Focused threshold
#MIN_THRESHOLD = 0.5
#MAX_THRESHOLD = 0.6
#THRESHOLD_STEP = 0.001

# Name of the evaluation metric
EVALUATION_METRICS_NAME = "evaluation_metrics.json"

