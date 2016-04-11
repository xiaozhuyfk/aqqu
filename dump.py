
import logging
import globals
from query_translator.util import writeFile
from query_translator.FreebaseDumpParser import FreebaseDumpParserC
from query_translator.FreebaseDumpReader import FreebaseDumpReaderC



aws_dump_dir = "/research/backup/aqqu/testresult/dump/"
aws_query_dir = "/research/backup/aqqu/testresult/query/"
aws_bow_dir = "/research/backup/aqqu/testresult/bow/"
boston_dump_dir = "/home/hongyul/aqqu/testresult/dump/"
boston_query_dir = "/home/hongyul/aqqu/testresult/query/"
boston_bow_dir = "/home/hongyul/aqqu/testresult/bow"


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

    file = "/data/freebase-rdf-latest.gz"
    reader = FreebaseDumpReaderC()
    reader.open(file)
    Parser = FreebaseDumpParserC()

    for cnt,lvCol in enumerate(reader):

        if 0 == (cnt % 1000):
            print 'read [%d] obj' %(cnt)

        for vCol in lvCol:
            e1 = vCol[0]
            e1 = Parser.DiscardPrefix(e1).decode('utf-8')
            edge = vCol[1].decode('utf-8')
            e2 = Parser.DiscardPrefix(vCol[2]).decode('utf-8')
            if e1.startswith("m.") and edge.startswith("<http://rdf.freebase.com"):
                at_index = e2.find("@")
                url_index = e2.find("^")

                if (at_index != -1 and url_index != -1):
                    e2 = e2[:min(at_index, url_index)]
                elif (at_index != -1):
                    e2 = e2[:at_index]
                elif (url_index != -1):
                    e2 = e2[:url_index]

                relation_name = Parser.DiscardPrefix(edge)

                print edge, relation_name


if __name__ == "__main__":
    main()