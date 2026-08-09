from pathlib import Path

base = Path("knowledge")

print("Knowledge exists:", base.exists())
print()

for item in base.rglob("*"):
    print(item)