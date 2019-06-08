from manufacturing_company.src.common.const import *
from manufacturing_company.src.classification_algorithms.NodeInfo import NodeInfo
from manufacturing_company.src.classification_algorithms.standard_classification import *
import pandas as pd
import operator
import networkx as nx
from manufacturing_company.src.classification_algorithms.CollectiveClassificationResult import CollectiveClassificationResult
from manufacturing_company.src.logs.collective_classification_logger import CollectiveClassificationLogger
from sklearn.metrics import jaccard_score, f1_score


def select_nodes_based_on_utility_score(utility_score_name, utility_score, pct, levels):
    utility_score = utility_score.sort_values(utility_score_name, ascending=False)

    known_nodes_map = dict()

    for position in range(1, levels + 1):
        employees_on_given_position = utility_score[utility_score[POSITION] == position]
        all_nodes = len(employees_on_given_position)
        known_nodes = round(all_nodes * pct)

        known_nodes_id = employees_on_given_position.iloc[:known_nodes].index
        known_nodes_map.update({id: position for id in known_nodes_id})

    return known_nodes_map


def message_passing(G, known_nodes, threshold, minority_labels, levels, jaccard_min):
    max_iter = 1000

    df_nodes = pd.DataFrame(G.nodes(data='utility_score'), columns=[ID, 'utility_score'])
    df_nodes = df_nodes.set_index(ID)

    order_desc = df_nodes.sort_values('utility_score', ascending=True).index

    nodes = pd.DataFrame(G.nodes(data='label'), columns=[ID, 'label'])
    nodes = nodes.set_index(ID)
    nodes = nodes.loc[order_desc, 'label'].to_dict()

    label_counter = {node_id: NodeInfo() for node_id in nodes.keys()}

    for i in range(max_iter):
        old_labels = [value for (key, value) in nodes.items() if key not in known_nodes]
        for node, label in nodes.items():
            if label != -1:
                neighbors = G.neighbors(node)
                for neighbor in neighbors:
                    if neighbor not in known_nodes:
                        label_counter[neighbor].labels.append(label)

        # UPDATE LABELS
        for node, label in nodes.items():
            unique_labels = len(set(label_counter[node].labels)) == 1

            # TODO method calculate label frequency
            label_freq = None
            if levels == 2:
                label_freq = {1: 0, 2: 0}
            elif levels == 3:
                label_freq = {1: 0, 2: 0, 3: 0}
            else:
                print(set(nodes.values()))
                raise Exception

            for l in label_freq.keys():
                size = label_counter[node].labels.count(l)
                if l not in minority_labels:
                    size = round(size / float(threshold))
                label_freq[l] = size

            same_freq = len(set(label_freq.values())) == 1

            # TODO function select update strategy
            if unique_labels:
                nodes[node] = label_counter[node].labels[0]
                label_counter[node].unchanged_iter = 0
            elif same_freq:
                # TODO update unchanged state
                label_counter[node].unchanged_iter += 1

                if label_counter[node].unchanged_iter > 10:
                    neighbors = G.neighbors(node)

                    max_utility_score = -1
                    node_label = -1

                    for neighbor_id in neighbors:
                        neighbor = G.nodes[neighbor_id]
                        if (neighbor['utility_score'] > max_utility_score) & (neighbor['label'] != -1):
                            max_utility_score = neighbor['utility_score']
                            node_label = neighbor['label']

                    nodes[node] = node_label
                    label_counter[node].unchanged_iter = 0
            else:
                nodes[node] = max(label_freq.items(), key=operator.itemgetter(1))[0]
                label_counter[node].unchanged_iter = 0

            label_counter[node].labels = []

        new_labels = [value for (key, value) in nodes.items() if key not in known_nodes]
        if (jaccard_score(old_labels, new_labels, average='micro') >= jaccard_min) & (-1 not in nodes.values()):
            break

    return nodes


def collective_classification(logger, month, G, df_features, pct, levels, df_positions, threshold, minority_labels, jaccard_min):
    feature_names = df_features.loc[:, df_features.columns != POSITION]

    for utility_score_name in feature_names:
        utility_score = df_features[[utility_score_name, POSITION]]
        known_nodes = select_nodes_based_on_utility_score(utility_score_name, utility_score, pct, levels)

        nx.set_node_attributes(G, -1, 'label')
        nx.set_node_attributes(G, known_nodes, 'label')
        nx.set_node_attributes(G, utility_score[utility_score_name], 'utility_score')

        nodes = message_passing(G, known_nodes, threshold, minority_labels, levels, jaccard_min)

        nodes = pd.DataFrame.from_dict(nodes, orient='index', columns=[POSITION])
        nodes.index.name = ID

        nodes = nodes.loc[~nodes.index.isin(known_nodes)]

        df_merged = pd.merge(nodes, df_features[POSITION], on=ID)

        f1 = f1_score(df_merged.iloc[:, 0], df_merged.iloc[:, 1], average='macro')

        logger.save(
            CollectiveClassificationResult(f1, pct, utility_score_name, threshold, jaccard_min, minority_labels), month)

