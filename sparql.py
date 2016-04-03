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


    query = """
PREFIX fb: <http://rdf.freebase.com/key/>
 SELECT DISTINCT ?0 where {
 fb:m.025s6bf fb:wikipedia.en_id ?0 .
 FILTER (?0 != fb:m.025s6bf)
} LIMIT 300
    """

    query = '''
        SELECT ?name where {
        ?x <http://rdf.freebase.com/ns/type.object.name> ?name.
        } LIMIT 2000000
    '''

    query = '''
        SELECT ?e1 ?e2 where {
        ?e1 <http://rdf.freebase.com/ns/astronomy.astronomical_discovery.discovery_technique> ?e2.
        } LIMIT 2000000
    '''

    print backend.query_json(query)


if __name__ == "__main__":
    main()
