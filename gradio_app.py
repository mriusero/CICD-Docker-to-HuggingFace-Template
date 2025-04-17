import gradio as gr
from smolagents import GradioUI, CodeAgent, HfApiModel

model = HfApiModel()

alfred = CodeAgent(
    tools=[],
    model=model,
    add_base_tools=True,  # Add any additional base tools
    planning_interval=3   # Enable planning every 3 steps
)

if __name__ == "__main__":
    GradioUI(alfred).launch()