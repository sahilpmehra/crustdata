import asyncio
from initialize_vectors import initialize_vector_store

async def startup():
    print("Initializing vector store...")
    try:
        await initialize_vector_store()
        print("Vector store initialization complete!")
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(startup()) 