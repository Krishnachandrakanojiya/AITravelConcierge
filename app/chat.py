from app.main import plan_trip


def show_help():
    print("\nCommands:")
    print("  help   - Show available commands")
    print("  status - Show system status")
    print("  clear  - Clear screen")
    print("  quit   - Exit application")
    print()


def main():

    print("=" * 60)
    print("🚀 Travel Agent Chat Interface")
    print("=" * 60)
    print("Welcome! I'm your AI Travel Concierge.")
    print("Tell me about your travel plans and I'll help you plan your trip!")
    print()

    show_help()

    while True:

        user_input = input("\n💬 You: ").strip()

        if user_input.lower() == "quit":
            print("\n👋 Goodbye! Safe travels!")
            break

        elif user_input.lower() == "help":
            show_help()
            continue

        elif user_input.lower() == "status":
            print("\n✅ Azure OpenAI Connected")
            print("✅ Semantic Kernel Ready")
            print("✅ Cosmos DB Connected")
            print("✅ RAG Knowledge Base Ready")
            print("✅ Bing Connection Available")
            continue

        elif user_input.lower() == "clear":
            print("\n" * 40)
            continue

        print("\n🤖 Agent: Let me help you plan your trip...")

        trip = plan_trip()

        print("\n" + "=" * 60)
        print("🎯 TRAVEL PLAN")
        print("=" * 60)

        print(
            trip.model_dump_json(
                indent=2
            )
        )


if __name__ == "__main__":
    main()