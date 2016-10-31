from query_translator.util import readFile

def main():
    #original_file = "results/final_f917_evaluation_output.txt"
    #original_file = "testresult/F917_Ranker_TestResult.log"
    #test_file = "testresult/F917_Ranker_kl2_testresult.log"
    #original_file = "results/final_wq_evaluation_output.txt"
    original_file = "testresult/WQ_Ranker_TestResult.log"
    test_file = "testresult/WQ_Ranker_kl_longscore.log"

    original_list = readFile(original_file).split("\n")
    test_list = readFile(test_file).split("\n")

    win = 0
    loss = 0
    for i in xrange(len(original_list)):
        if (original_list[i] == ""):
            continue
        triple_o = original_list[i].split("\t")
        triple_t = test_list[i].split("\t")

        answer_o = triple_o[2][1:-1]
        answer_t = triple_t[2][1:-1]
        answer = triple_o[1][1:-1]

        answers_o = answer_o.split(", ")
        answers_t = answer_t.split(", ")

        print answers_o, answers_t

        if (answer_o == answer_t):
            continue

        if (answer_o == answer):
            loss += 1

        if (answer_t == answer):
            win += 1

    print win
    print loss


if __name__ == "__main__":
    main()