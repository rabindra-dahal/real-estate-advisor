import inspect
import app.interfaces.vector_repo as vr
import app.interfaces.llm_service as ls

print("--- Methods in IVectorRepository ---")
for name, member in inspect.getmembers(vr.IVectorRepository, predicate=inspect.isfunction):
    print(f" - {name}{inspect.signature(member)}")

print("\n--- Methods in ILLMService ---")
for name, member in inspect.getmembers(ls.ILLMService, predicate=inspect.isfunction):
    print(f" - {name}{inspect.signature(member)}")
