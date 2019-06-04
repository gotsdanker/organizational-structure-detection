import os
import datetime


def save(modelInfoMap, algorithm, levels):
    now = datetime.datetime.now()
    # filename = now.strftime('%Y-%m-%d_%H:%M:%S_' + algorithm.__name__ + '_' + levels + 'levels.txt')
    directoryName = now.strftime('%Y-%m-%d_%H:%M:%S_' + algorithm.__name__ + '_' + str(levels) + 'levels')
    directoryPath = now.strftime('manufacturing_company/logs/' + directoryName)
    os.mkdir(directoryPath)

    for month, modelInfoList in modelInfoMap.items():
        with open(directoryPath + '/' + str(month) + '_months', 'a') as file:
            for modelInfo in modelInfoList:
                file.write(algorithm.__name__ + '\n\n')
                file.write(modelInfo.cv_scorer + ': {0:.4f}'.format(modelInfo.model.best_score_) + '\n\n')

                file.write('features: [\n')
                for feature in modelInfo.features:
                    file.write('\t' + feature + '\n')
                file.write(']\n\n')

                file.write('params: ' + str(dict(modelInfo.model.best_params_)) + '\n\n')

                for i in modelInfo.model.cv_results_.keys():
                    try:
                        file.write('{0:30s} {1:.4f} \n'.format(i, modelInfo.model.cv_results_[i][modelInfo.model.best_index_]))
                    except:
                        pass

                file.write('##################################################################\n\n')