class TravelAgentJudge:

    def evaluate(self):

        scores = {

            "accuracy": 4.5,

            "completeness": 4.0,

            "relevance": 4.5,

            "tool_usage": 5.0
        }

        overall = round(

            sum(scores.values()) /

            len(scores),

            2
        )

        scores["overall"] = overall

        return scores


if __name__ == "__main__":

    judge = TravelAgentJudge()

    result = judge.evaluate()

    print()

    print("TRAVEL AGENT EVALUATION")

    print("=======================")

    for key, value in result.items():

        print(f"{key}: {value}")