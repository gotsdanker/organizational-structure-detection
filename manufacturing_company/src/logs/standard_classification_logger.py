import os
import datetime


class StandardClassificationLogger:
    def __init__(self, base_directory, levels, algorithm):
        self.base_directory = base_directory
        self.levels = levels
        self.algorithm = algorithm

        now = datetime.datetime.now()
        directory_name = now.strftime('%Y-%m-%d_%H:%M:%S_' + algorithm.__name__ + '_' + str(levels) + '_levels')
        self.directory_path = base_directory + '/logs/standard_classification/' + directory_name

        os.mkdir(self.directory_path)

        self.write_header = True

    def save(self, modelInfo, month):
        log_file = self.directory_path + '/log_months_' + str(month) + '.csv'
        if not os.path.exists(log_file):
            self.write_header = True

        with open(log_file, 'a') as file:
            if self.write_header:
                file.write('f1_score;pct;params;features;cv_scorer\n')
                self.write_header = False

            file.write('{0:.4f}'.format(modelInfo.model.best_score_))
            file.write(';')
            file.write(str(modelInfo.pct))
            file.write(';')
            file.write(str(dict(modelInfo.model.best_params_)))
            file.write(';')
            file.write(str(modelInfo.features))
            file.write(';')
            file.write(modelInfo.cv_scorer)
            file.write('\n')
