# FILES
MC_FILE_01_REMOVE_FORMER_EMPLOYEE_AND_TECHNICAL_ACCOUNTS_COMMUNICATION = 'manufacturing_company/data/intermediate/01_remove_former_employee_and_technical_accounts/communication.csv'
MC_FILE_01_REMOVE_FORMER_EMPLOYEE_AND_TECHNICAL_ACCOUNTS_REPORTSTO = 'manufacturing_company/data/intermediate/01_remove_former_employee_and_technical_accounts/reportsto.csv'

MC_FILE_02_REMOVE_MESSAGES_SENT_TO_YOURSELF_COMMUNICATION = 'manufacturing_company/data/intermediate/02_remove_messages_sent_to_yourself/communication.csv'
MC_FILE_02_REMOVE_MESSAGES_SENT_TO_YOURSELF_REPORTSTO = 'manufacturing_company/data/intermediate/02_remove_messages_sent_to_yourself/reportsto.csv'

MC_FILE_03_DROP_DUPLICATES = 'manufacturing_company/data/intermediate/03_drop_duplicates/communication.csv'

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
