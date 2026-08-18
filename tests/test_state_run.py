from app.state import AgentState

state = AgentState()

print(f"Current State: {state.current_state.value}")

while state.current_state.value != "DONE":

    next_state = state.advance()

    print(
        f"State Changed -> {next_state.value}"
    )

print("Workflow Completed")