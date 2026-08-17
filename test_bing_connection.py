from dotenv import load_dotenv
import os

load_dotenv()

print("PROJECT_ENDPOINT:")
print(os.getenv("PROJECT_ENDPOINT"))

print()

print("BING_CONNECTION_ID:")
print(os.getenv("BING_CONNECTION_ID"))