from services.knowledge.loader import KnowledgeLoader

loader = KnowledgeLoader()

print("Base Path:")
print(loader.base_path)

print()

careers = loader.careers()

print("Total Careers:", len(careers))

print()

for career in careers:

    print(career.get("title", "No Title"))