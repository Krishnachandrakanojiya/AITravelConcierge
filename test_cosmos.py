from app.long_term_memory.core import CosmosMemory

memory = CosmosMemory()

memory.add_memory(
    "user1",
    "Krishna prefers vegetarian meals"
)

result = memory.get_memory(
    "user1"
)

print(result)