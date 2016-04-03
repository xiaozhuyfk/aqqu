"""
Provides a console based translation interface.

Copyright 2015, University of Freiburg.

Elmar Haussmann <haussmann@cs.uni-freiburg.de>

"""
import logging
import globals

logging.basicConfig(format = "%(asctime)s : %(levelname)s "
                             ": %(module)s : %(message)s",
                    level = logging.INFO)

logger = logging.getLogger(__name__)

result_file = "testresult/dump/pairs"
edges = [
    "http://rdf.freebase.com/ns/astronomy.astronomical_discovery.discovery_technique"
]

PAIR_QUERY_FORMAT = '''
        SELECT ?e1 ?e2 where {
        ?e1 <%s> ?e2.
        }
    '''


def main():

    import argparse
    parser = argparse.ArgumentParser(description = "Console based translation.")
    parser.add_argument("ranker_name",
                        default = "WQ_Ranker",
                        help = "The ranker to use.")
    parser.add_argument("--config",
                        default = "config.cfg",
                        help = "The configuration file to use.")
    args = parser.parse_args()
    globals.read_configuration(args.config)
    config_params = globals.config
    backend = globals.get_sparql_backend(config_params)

    for edge in edges:
        print backend.query_json(PAIR_QUERY_FORMAT % edge)


if __name__ == "__main__":
    main()
