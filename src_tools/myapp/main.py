from langchain_core.messages import HumanMessage
from myapp.graph import build_app
from myapp.state import RagState
import asyncio

async def run_example(msg):
    app = build_app()
    
    initial_state = RagState()
    initial_state["messages"] = msg
    final_state = await app.ainvoke(initial_state)

    print("\n=== Final Answer ===\n")
    print(final_state.get("final_answer", ""))

    png_bytes = app.get_graph().draw_mermaid_png()
    with open("workflow.png", "wb") as f:
        f.write(png_bytes)

if __name__ == "__main__":
    asyncio.run(run_example(msg=[HumanMessage(content="We need information about Professional services and delivery: engagement scopes and implementation guides.")]))