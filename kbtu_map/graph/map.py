import logging

from kbtu_map.settings import GRAPH_PATH
from kbtu_map.graph import Graph

LOG = logging.getLogger('map')


class Map:
    __instance = None

    @staticmethod
    def get_instance():
        if Map.__instance is None:
            Map.__instance = Graph.get_instance(GRAPH_PATH)
            LOG.info(f'Connected map ({id(Map.__instance)})')

        return Map.__instance
