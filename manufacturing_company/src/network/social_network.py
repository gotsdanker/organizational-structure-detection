from manufacturing_company.src.common.const import *
import networkx as nx
from networkx.algorithms.clique import cliques_containing_node, node_clique_number
import pandas as pd


def calculate_weights(df):
    messages_send_to_specific_employee = df.groupby([SENDER, RECIPIENT]).size().reset_index()
    all_sent_messages = df.groupby(SENDER).size().reset_index()

    weights_df = messages_send_to_specific_employee.merge(all_sent_messages, on=SENDER)
    weights_df[WEIGHT] = weights_df['0_x'] / weights_df['0_y']

    df = df.merge(weights_df, on=[SENDER, RECIPIENT])
    df = df.drop_duplicates([SENDER, RECIPIENT])

    return df[[SENDER, RECIPIENT, WEIGHT]]


def create_network(df):
    return nx.from_pandas_edgelist(df, source=SENDER, target=RECIPIENT, edge_attr=WEIGHT, create_using=nx.DiGraph)


def calculate_network_measures(G):
    in_degree = nx.in_degree_centrality(G)
    out_degree = nx.out_degree_centrality(G)
    betweenness = nx.betweenness_centrality(G, weight=WEIGHT)
    closeness = nx.closeness_centrality(G, distance=WEIGHT)
    eigenvector = nx.eigenvector_centrality(G.reverse(), weight=WEIGHT)
    clustering = nx.clustering(G.to_undirected(), weight=WEIGHT)
    pagerank = nx.pagerank(G, weight=WEIGHT)
    hubs, authorities = nx.hits_numpy(G)
    max_clique = node_clique_number(G.to_undirected())

    node_cliques = cliques_containing_node(G.to_undirected())
    node_cliques_count = {}
    for node, cliques in node_cliques.items():
        node_cliques_count[node] = len(cliques)

    network_df = pd.DataFrame(list(G.nodes), columns=[ID]);

    network_df[IN_DEGREE] = network_df[ID].map(in_degree)
    network_df[OUT_DEGREE] = network_df[ID].map(out_degree)
    network_df[BETWEENNESS] = network_df[ID].map(betweenness)
    network_df[CLOSENESS] = network_df[ID].map(closeness)
    network_df[EIGENVECTOR] = network_df[ID].map(eigenvector)
    network_df[CLUSTERING] = network_df[ID].map(clustering)
    network_df[PAGERANK] = network_df[ID].map(pagerank)
    network_df[HUBS] = network_df[ID].map(hubs)
    network_df[AUTHORITIES] = network_df[ID].map(authorities)
    network_df[MAX_CLIQUE] = network_df[ID].map(max_clique)
    network_df[CLIQUES_COUNT] = network_df[ID].map(node_cliques_count)

    return network_df