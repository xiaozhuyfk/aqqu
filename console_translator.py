"""
Provides a console based translation interface.

Copyright 2015, University of Freiburg.

Elmar Haussmann <haussmann@cs.uni-freiburg.de>

"""
import logging

import globals
import scorer_globals
from query_translator.features import FeatureExtractor
from query_translator.translator import QueryTranslator
from query_translator.util import writeFile, test_file, rank_error, rank_pos
from query_translator.ranker import feature_diff

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
    if args.ranker_name not in scorer_globals.scorers_dict:
        logger.error("%s is not a valid ranker" % args.ranker_name)
        logger.error("Valid rankers are: %s " % (" ".join(scorer_globals.scorers_dict.keys())))
    logger.info("Using ranker %s" % args.ranker_name)
    ranker = scorer_globals.scorers_dict[args.ranker_name]
    translator = QueryTranslator.init_from_config()
    translator.set_scorer(ranker)

    writeFile(test_file, "", "w")

    for i in xrange(len(rank_error)):
        query = rank_error[i]
        results = translator.translate_and_execute_query(query)
        if (len(results) > 0):
            correct = results[rank_pos[i]].query_candidate

            candidate = results[0].query_candidate
            sparql_query = candidate.to_sparql_query()
            correct_query = correct.to_sparql_query()

            result_rows = results[0].query_result_rows
            result = []
            for r in result_rows:
                if len(r) > 1:
                    result.append("%s (%s)" % (r[1], r[0]))
                else:
                    result.append("%s" % r[0])
            correct_result_rows = results[rank_pos[i]].query_result_rows
            correct_result = []
            for r in correct_result_rows:
                if len(r) > 1:
                    correct_result.append("%s (%s)" % (r[1], r[0]))
                else:
                    correct_result.append("%s" % r[0])

            extractor = FeatureExtractor(True, False, None)
            features = extractor.extract_features(candidate)
            y_features = extractor.extract_features(correct)
            diff = feature_diff(features, y_features)

            X = ranker.dict_vec.transform(diff)
            if ranker.scaler:
                X = ranker.scaler.transform(X)
            ranker.model.n_jobs = 1
            p = ranker.model.predict(X)
            c = ranker.label_encoder.inverse_transform(p)
            res = c[0]

            root_name = "Root Node: %s\n" % (candidate.root_node.entity.name.encode('utf-8'))
            query_str = "SPARQL query: %s\n" % (sparql_query.encode('utf-8'))
            graph_str = "Candidate Graph: %s\n" % (candidate.graph_as_string().encode('utf-8'))
            graph_str_simple = "Simple Candidate Graph: %s" % (candidate.graph_as_simple_string().encode('utf-8'))
            y_graph_str_simple = "Answer Candidate Graph: %s" % (correct.graph_as_simple_string().encode('utf-8'))
            result_str = "Result: %s\n" % ((" ".join(result)).encode('utf-8'))
            correct_result_str = "Correct Result: %s\n" % ((" ".join(correct_result)).encode('utf-8'))

            feature_str = "Result Features: %s\n" % (str(features).encode('utf-8'))
            y_feature_str = "Answer Features: %s\n" %(str(y_features).encode('utf-8'))
            diff_str = "Feature Diff: %s\n" %(str(diff).encode('utf-8'))

            x_str = "X vector: %s\n" % (str(X).encode('utf-8'))
            p_str = "Predict vector: %s\n" % (str(p).encode('utf-8'))
            c_str = "C vector: %s\n" % (str(c).encode('utf-8'))
            cmp_res = "Compare result: %d\n" % (res)

            writeFile(test_file, root_name, "a")
            writeFile(test_file, result_str, "a")
            writeFile(test_file, correct_result_str, "a")

            writeFile(test_file, graph_str_simple, "a")
            writeFile(test_file, y_graph_str_simple, "a")

            writeFile(test_file, feature_str, "a")
            writeFile(test_file, y_feature_str, "a")
            writeFile(test_file, diff_str, "a")

            writeFile(test_file, x_str, "a")
            writeFile(test_file, p_str, "a")
            writeFile(test_file, c_str, "a")
            writeFile(test_file, cmp_res, "a")
        writeFile(test_file, "\n", "a")

    """
    for query in test_set + unidentified:
        results = translator.translate_and_execute_query(query)
        if (len(results) > 0):
            for i in xrange(len(results)):
                if (i > 10):
                    break
                candidate = results[i].query_candidate
                sparql_query = candidate.to_sparql_query()
                result_rows = results[i].query_result_rows
                result = []
                for r in result_rows:
                    if len(r) > 1:
                        result.append("%s (%s)" % (r[1], r[0]))
                    else:
                        result.append("%s" % r[0])

                extractor = FeatureExtractor(True, False, None)
                features = extractor.extract_features(candidate)

                root_name = "%d Root Node: %s\n" % (i+1, candidate.root_node.entity.name.encode('utf-8'))
                query_str = "%d SPARQL query: %s\n" % (i+1, sparql_query.encode('utf-8'))
                graph_str = "%d Candidate Graph: %s\n" % (i+1, candidate.graph_as_string().encode('utf-8'))
                graph_str_simple = "%d Simple Candidate Graph: %s" % (i+1, candidate.graph_as_simple_string().encode('utf-8'))
                result_str = "%d Result: %s\n" % (i+1, (" ".join(result)).encode('utf-8'))
                feature_str = "%d Features: %s\n" % (i+1, str(features).encode('utf-8'))
                writeFile(test_file, root_name, "a")
                #writeFile(test_file, graph_str, "a")
                writeFile(test_file, graph_str_simple, "a")
                writeFile(test_file, feature_str, "a")
                #writeFile(test_file, query_str, "a")
                writeFile(test_file, result_str, "a")
        writeFile(test_file, "\n", "a")
    """

    """
    while True:
        sys.stdout.write("enter question> ")
        sys.stdout.flush()
        query = sys.stdin.readline().strip()
        logger.info("Translating query: %s" % query)
        results = translator.translate_and_execute_query(query)
        logger.info("Done translating query: %s" % query)
        logger.info("#candidates: %s" % len(results))
        if len(results) > 0:
            best_candidate = results[0].query_candidate
            sparql_query = best_candidate.to_sparql_query()
            result_rows = results[0].query_result_rows
            result = []
            # Usually we get a name + mid.
            for r in result_rows:
                if len(r) > 1:
                    result.append("%s (%s)" % (r[1], r[0]))
                else:
                    result.append("%s" % r[0])
            logger.info("SPARQL query: %s" % sparql_query)
            logger.info("Result: %s " % " ".join(result))
    """


if __name__ == "__main__":
    main()
