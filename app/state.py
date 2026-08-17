from enum import Enum


class TravelState(Enum):

    INIT = "INIT"
    CLARIFY_REQUIREMENTS = "CLARIFY_REQUIREMENTS"
    PLAN_TOOLS = "PLAN_TOOLS"
    EXECUTE_TOOLS = "EXECUTE_TOOLS"
    ANALYZE_RESULTS = "ANALYZE_RESULTS"
    RESOLVE_ISSUES = "RESOLVE_ISSUES"
    PRODUCE_OUTPUT = "PRODUCE_OUTPUT"
    DONE = "DONE"

class AgentState:

    def __init__(self):

        self.current_state = TravelState.INIT

    def advance(self):

        transitions = {
            TravelState.INIT: TravelState.CLARIFY_REQUIREMENTS,
            TravelState.CLARIFY_REQUIREMENTS: TravelState.PLAN_TOOLS,
            TravelState.PLAN_TOOLS: TravelState.EXECUTE_TOOLS,
            TravelState.EXECUTE_TOOLS: TravelState.ANALYZE_RESULTS,
            TravelState.ANALYZE_RESULTS: TravelState.RESOLVE_ISSUES,
            TravelState.RESOLVE_ISSUES: TravelState.PRODUCE_OUTPUT,
            TravelState.PRODUCE_OUTPUT: TravelState.DONE
        }

        self.current_state = transitions.get(
            self.current_state,
            TravelState.DONE
        )

        return self.current_state

    def reset(self):

        self.current_state = TravelState.INIT