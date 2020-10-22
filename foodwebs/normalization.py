import numpy as np
import networkx as nx


def flows_normalization(graph_view, norm_type):
    if norm_type == 'biomass':
        return biomass_normalization(graph_view)
    elif norm_type == 'log':
        return log_normalization(graph_view)
    elif norm_type == 'diet':
        return diet_normalization(graph_view)
    elif norm_type == 'tst':
        return tst_normalization(graph_view)
    return graph_view


def diet_normalization(graph_view):
    '''
    In this normalization method, each weight is divided by node's diet,
    which is sum of it's input weights, inlcuding Import
    '''
    def get_node_diet(node):
        return sum([x[2] for x in graph_view.in_edges(node, data='weight')])

    nx.set_edge_attributes(graph_view, {(e[0], e[1]): {'weight': e[2] / get_node_diet(e[1])}
                                        for e in graph_view.edges(data='weight')})
    return graph_view


def log_normalization(graph_view):
    nx.set_edge_attributes(graph_view, {(e[0], e[1]): {'weight': np.log(e[2])}
                                        for e in graph_view.edges(data='weight')})
    return graph_view


def biomass_normalization(graph_view):
    biomass = nx.get_node_attributes(graph_view, "Biomass")
    nx.set_edge_attributes(graph_view, {(e[0], e[1]): {'weight': e[2] / biomass[e[0]]}
                                        for e in graph_view.edges(data='weight')})
    return graph_view


def tst_normalization(graph_view):
    '''Function returning a list of internal flows normalized to TST'''

    TST = sum([x[2] for x in graph_view.edges(data='weight')])
    nx.set_edge_attributes(graph_view, {(e[0], e[1]): {'weight': e[2] / TST}
                                        for e in graph_view.edges(data='weight')})
    return graph_view
