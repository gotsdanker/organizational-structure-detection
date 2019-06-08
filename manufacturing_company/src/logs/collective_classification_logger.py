import os
import datetime


class CollectiveClassificationLogger:
    def __init__(self, base_directory, levels):
        self.base_directory = base_directory
        self.levels = levels

        now = datetime.datetime.now()
        directory_name = now.strftime('%Y-%m-%d_%H:%M:%S_CollectiveClassification_' + str(levels) + '_levels')
        self.directory_path = base_directory + '/logs/collective_classification/' + directory_name

        os.mkdir(self.directory_path)

        self.write_header = True

    def save(self, result, month):
        log_file = self.directory_path + '/log_months_' + str(month) + '.csv'
        if not os.path.exists(log_file):
            self.write_header = True

        with open(log_file, 'a') as file:
            if self.write_header:
                file.write('f1_score;pct;utility_score;threshold;jaccard;minority_classes\n')
                self.write_header = False

            file.write('{0:.4f}'.format(result.f1_score))
            file.write(';')
            file.write(str(result.pct))
            file.write(';')
            file.write(result.utility_score)
            file.write(';')
            file.write(str(result.threshold))
            file.write(';')
            file.write(str(result.jaccard))
            file.write(';')
            file.write(str(result.minority_classes))
            file.write('\n')
