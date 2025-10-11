from google.adk import BaseAgent, Tool, WorkflowAgent, SequentialAgent


# 1️⃣ Define a tool
def add_tool(a: float, b: float) -> float:
    return a + b


t_add = Tool(
    name="AddTool",
    func=add_tool,
    description="Adds two numbers",
)


# 2️⃣ Define a simple LLM agent (if you want dynamic decision-making)
class MyLLMAgent(BaseAgent):
    async def decide(self, input_text: str, **kwargs):
        # simple logic or call an LLM to decide which tool to use
        if "add" in input_text.lower():
            return {"tool": t_add, "args": {"a": 1, "b": 2}}
        # else fallback
        return {"tool": t_add, "args": {"a": 0, "b": 0}}


# 3️⃣ Define a workflow / orchestrator
class MyOrchestrator(WorkflowAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # you could use a SequentialAgent or others internally
        self.seq = SequentialAgent(agents=[MyLLMAgent(), MyLLMAgent()])

    async def run(self, input_text: str):
        return await self.seq.run(input_text)


# 4️⃣ Use it
import asyncio


async def main():
    orchestrator = MyOrchestrator()
    resp = await orchestrator.run("Add 5 and 7")
    print("Response:", resp)


if __name__ == "__main__":
    asyncio.run(main())
