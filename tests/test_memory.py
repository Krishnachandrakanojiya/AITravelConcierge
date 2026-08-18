from app.memory import ShortTermMemory


def test_memory_initializes_empty():
    memory = ShortTermMemory()
    assert memory.get_conversation_history() == []


def test_default_max_items_is_five():
    memory = ShortTermMemory()
    assert memory.max_items == 5


def test_custom_max_items():
    memory = ShortTermMemory(max_items=3)
    assert memory.max_items == 3


def test_add_single_conversation():
    memory = ShortTermMemory()
    memory.add_conversation("user", "hello")
    assert len(memory.get_conversation_history()) == 1


def test_single_conversation_role():
    memory = ShortTermMemory()
    memory.add_conversation("user", "hello")
    assert memory.get_conversation_history()[0]["role"] == "user"


def test_single_conversation_message():
    memory = ShortTermMemory()
    memory.add_conversation("user", "hello")
    assert memory.get_conversation_history()[0]["message"] == "hello"


def test_add_assistant_message():
    memory = ShortTermMemory()
    memory.add_conversation("assistant", "hi")
    assert memory.get_conversation_history()[0]["role"] == "assistant"


def test_history_preserves_order():
    memory = ShortTermMemory()
    memory.add_conversation("user", "one")
    memory.add_conversation("assistant", "two")
    history = memory.get_conversation_history()
    assert history[0]["message"] == "one"
    assert history[1]["message"] == "two"


def test_history_length_two():
    memory = ShortTermMemory()
    memory.add_conversation("user", "one")
    memory.add_conversation("assistant", "two")
    assert len(memory.get_conversation_history()) == 2


def test_memory_does_not_evict_under_limit():
    memory = ShortTermMemory(max_items=3)
    memory.add_conversation("user", "one")
    memory.add_conversation("assistant", "two")
    assert len(memory.get_conversation_history()) == 2


def test_memory_evicts_over_limit():
    memory = ShortTermMemory(max_items=2)
    memory.add_conversation("user", "one")
    memory.add_conversation("assistant", "two")
    memory.add_conversation("user", "three")
    assert len(memory.get_conversation_history()) == 2


def test_memory_evicts_oldest_item():
    memory = ShortTermMemory(max_items=2)
    memory.add_conversation("user", "one")
    memory.add_conversation("assistant", "two")
    memory.add_conversation("user", "three")
    history = memory.get_conversation_history()
    assert history[0]["message"] == "two"


def test_memory_keeps_latest_item():
    memory = ShortTermMemory(max_items=2)
    memory.add_conversation("user", "one")
    memory.add_conversation("assistant", "two")
    memory.add_conversation("user", "three")
    history = memory.get_conversation_history()
    assert history[-1]["message"] == "three"


def test_memory_with_max_items_one():
    memory = ShortTermMemory(max_items=1)
    memory.add_conversation("user", "one")
    memory.add_conversation("assistant", "two")
    assert len(memory.get_conversation_history()) == 1


def test_memory_with_max_items_one_keeps_latest():
    memory = ShortTermMemory(max_items=1)
    memory.add_conversation("user", "one")
    memory.add_conversation("assistant", "two")
    assert memory.get_conversation_history()[0]["message"] == "two"


def test_private_evict_method_can_be_called():
    memory = ShortTermMemory(max_items=1)
    memory.history = [
        {"role": "user", "message": "one"},
        {"role": "assistant", "message": "two"}
    ]
    memory._evict_if_needed()
    assert len(memory.get_conversation_history()) == 1


def test_private_evict_keeps_latest():
    memory = ShortTermMemory(max_items=1)
    memory.history = [
        {"role": "user", "message": "one"},
        {"role": "assistant", "message": "two"}
    ]
    memory._evict_if_needed()
    assert memory.get_conversation_history()[0]["message"] == "two"


def test_history_returns_list():
    memory = ShortTermMemory()
    assert isinstance(memory.get_conversation_history(), list)


def test_multiple_roles_supported():
    memory = ShortTermMemory()
    memory.add_conversation("system", "rules")
    assert memory.get_conversation_history()[0]["role"] == "system"


def test_memory_limit_after_many_messages():
    memory = ShortTermMemory(max_items=3)

    for index in range(10):
        memory.add_conversation("user", f"message {index}")

    history = memory.get_conversation_history()

    assert len(history) == 3
    assert history[0]["message"] == "message 7"
    assert history[-1]["message"] == "message 9"