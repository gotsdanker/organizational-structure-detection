class CollectiveClassificationResult:
    def __init__(self, f1_score, pct, utility_score, threshold, jaccard, minority_classes):
        self.f1_score = f1_score
        self.pct = pct
        self.utility_score = utility_score
        self.threshold = threshold
        self.jaccard = jaccard
        self.minority_classes = minority_classes
