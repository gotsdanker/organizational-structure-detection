# FILES
MC_FILE_01_AFTER_DATA_CLEANING_COMMUNICATION = 'manufacturing_company/data/intermediate/01_after_data_cleaning/communication.csv'
MC_FILE_01_AFTER_DATA_CLEANING_REPORTSTO = 'manufacturing_company/data/intermediate/01_after_data_cleaning/reportsto.csv'

MC_FILE_02_DROP_DUPLICATES = 'manufacturing_company/data/intermediate/02_drop_duplicates/communication.csv'

MC_FILE_MINIMUM_ACTIVITY = 'manufacturing_company/data/processed/minimum_activity/months_{0}.csv'

MC_FILE_NETWORK_MEASURES = 'manufacturing_company/data/processed/network_measures/months_{0}.csv'

MC_FILE_FEATURES = 'manufacturing_company/data/processed/features/months_{0}.csv'

MC_FILE_POSITIONS = 'manufacturing_company/data/raw/positions.csv'

# NUMBER OF MONTHS
MONTHS = [1,2,3,4,5]

# LABELS
SENDER = 'Sender'
RECIPIENT = 'Recipient'
EVENT_DATE = 'EventDate'
ID = 'ID'
REPORTS_TO_ID = 'ReportsToID'
POSITION = 'ManagementLevel'
YEAR = 'year'
MONTH = 'month'

WEIGHT = 'weight'

# NETWORK MEASURES
IN_DEGREE = 'in_degree'
OUT_DEGREE = 'out_degree'
BETWEENNESS = 'betweenness'
CLOSENESS = 'closeness'
EIGENVECTOR = 'eigenvector'
CLUSTERING = 'clustering_coeff'
PAGERANK = 'pagerank'
HUBS = 'hubs'
AUTHORITIES = 'authorities'
CLIQUES_COUNT = 'cliques_count'
MAX_CLIQUE = 'max_clique'

# OTHER FEATURES
OVERTIME = 'overtime'
WORK_AT_WEEKEND = 'work_at_weekend'
NEIGHBORHOOD_VARIABILITY_SENDER = 'neighborhood_variability_sender'
NEIGHBORHOOD_VARIABILITY_RECIPIENT = 'neighborhood_variability_recipient'
NEIGHBORHOOD_VARIABILITY_ALL = 'neighborhood_variability_all'
