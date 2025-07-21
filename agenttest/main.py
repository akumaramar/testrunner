from IPython.display import display, HTML
from helper import extract_html_content
import random
from helper import get_openai_api_key
from llama_index.utils.workflow import draw_all_possible_flows

# Set your OpenAI API key
api_key = get_openai_api_key()



from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context
)

class MyWorkflow(Workflow):
    # declare a function as a step
    @step
    async def my_step(self, ev: StartEvent) -> StopEvent:
        # do something here
        return StopEvent(result="Hello, world!")
    


async def main():
    basic_workflow = MyWorkflow(timeout=10, verbose=False)
    draw_all_possible_flows(basic_workflow, filename="./workflows/basic_workflow.html")
    html_content = extract_html_content("./workflows/basic_workflow.html")
    display(HTML(html_content))   
    result = await basic_workflow.run()
    
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



