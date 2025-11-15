import asyncio, sys
from agent import query_design_standards

async def _run(topic: str):
    print(f"Topic: {topic}\n")
    ans = await query_design_standards(topic)
    print(ans)

def main():
    topic = " ".join(sys.argv[1:]) if len(sys.argv)>1 else input("Enter topic: ")
    asyncio.run(_run(topic))

if __name__ == "__main__":
    main()
