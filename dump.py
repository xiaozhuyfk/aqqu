
import logging
import globals
from query_translator.util import writeFile
from query_translator.FreebaseDumpParser import FreebaseDumpParserC
from query_translator.FreebaseDumpReader import FreebaseDumpReaderC



aws_raw_dir = "/research/backup/aqqu/testresult/raw/"
aws_dump_dir = "/research/backup/aqqu/testresult/dump/"
aws_query_dir = "/research/backup/aqqu/testresult/query/"
aws_bow_dir = "/research/backup/aqqu/testresult/bow/"
boston_dump_dir = "/home/hongyul/aqqu/testresult/dump/"
boston_query_dir = "/home/hongyul/aqqu/testresult/query/"
boston_bow_dir = "/home/hongyul/aqqu/testresult/bow"


PAIR_QUERY_FORMAT = '''
        SELECT ?e1 ?e2 where {
            ?e1 <%s> ?e2.
        }
    '''

ENTITY_NAME_FORMAT = '''
PREFIX fb: <http://rdf.freebase.com/ns/>
SELECT DISTINCT ?0 where {
    fb:%s fb:type.object.name ?0 .
}
'''

RELATION_QUERY_FORMAT = '''
SELECT ?r where {
    ?e1 ?r ?e2.
} LIMIT 20000
'''

QUERY_FORMAT = "#uw20(#1(%s) #1(%s))"


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

    relations = set()

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

                e1_name = backend.query_json(ENTITY_NAME_FORMAT % e1)
                print e1, e1_name
                e1_name = e1_name[0][0].encode("utf-8")
                e1_paren = e1_name.find("(")
                if (e1_paren != -1):
                        e1_name = e1_name[:e1_paren]

                if (e2.startswith("m.")):
                    e2_name = backend.query_json(ENTITY_NAME_FORMAT % e2)[0][0].encode('utf-8')
                    e2_paren = e2_name.find("(")
                    if (e2_paren != -1):
                        e2_name = e2_name[:e2_paren]
                else:
                    e2_name = e2


                relation_name = Parser.DiscardPrefix(edge)
                rel = relation_name.replace(".", "_")

                aws_dump_file = aws_dump_dir + rel + ".log"
                print e1_name, e2_name

                '''
                if (edge not in relations):
                    writeFile(aws_dump_file, "", "w")
                    relations.add(edge)
                query = QUERY_FORMAT % (e1, e2)
                '''





if __name__ == "__main__":
    main()