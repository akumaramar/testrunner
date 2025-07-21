from agents import Agent, Runner, trace
# Use environment variable to set the API key

import os
from dotenv import load_dotenv
import asyncio
from storybuilder_agent import storybuilder_agent
from code_agent import code_agent
from search_agent import search_agent
from outline_agent import outline_agent
from review_agent import (
    review_agent, 
    feedback_compiler_agent, 
    format_content_for_review, 
    format_feedback_for_compilation,
    check_approval
)
from image_generator_agent import (
    image_generator_agent,
    format_content_for_image_generation,
    generate_image
)

async def main():
    load_dotenv()

    # Generate the outline based on input topic
    input_prompt = input("What kind of topic you want to generate your blog for:   ")

    with trace("Generating Story"):
        
        #1 Search the topic on the web
        search_results = await Runner.run(search_agent, input_prompt)
        print(search_results.final_output)
        print("Search results generated")
        
        #2 Generte outline on the topic
        outline = await Runner.run(outline_agent, search_results.final_output)
        print(outline.final_output)
        print("Outline generated")

        #3 Generate the story based on the outline
        story = await Runner.run(storybuilder_agent, outline.final_output)
        print(story.final_output)
        print("Story generated")

        #4 Generate the code snippets based on the story
        code = await Runner.run(code_agent, story.final_output)
        print(code.final_output)
        print("Code generated")

        #5 Start review process
        current_content = f"""
Story:
{story.final_output}

Code Snippets:
{code.final_output}
"""
        is_approved = False
        review_iteration = 1
        
        while not is_approved:
            print(f"\n=== Review Iteration {review_iteration} ===")
            
            # Format content for review with guidelines
            formatted_content = format_content_for_review(current_content)
            print("\nCurrent content for review:")
            print(formatted_content)
            print("\nTo approve the content, include the word 'APPROVED' in your feedback.")
            print("If changes are needed, provide specific feedback for improvements.")
            
            #6 Get LLM review
            print("\nGetting LLM review...")
            llm_review = await Runner.run(review_agent, formatted_content)
            print("LLM Review completed:")
            print(llm_review.final_output)
            
            #7 Get human review
            print("\nWaiting for human review...")
            human_feedback = input("Please provide your review following the guidelines above:\n")
            
            #8 Check for approval
            if check_approval(human_feedback):
                print("\nContent has been approved!")
                is_approved = True
                final_content = current_content
            else:
                #9 Use LLM to compile and incorporate feedback
                print("\nCompiling and incorporating feedback...")
                feedback_compilation_prompt = format_feedback_for_compilation(
                    current_content,
                    llm_review.final_output,
                    human_feedback
                )
                
                improved_content = await Runner.run(feedback_compiler_agent, feedback_compilation_prompt)
                current_content = improved_content.final_output
                review_iteration += 1
        
        # Generate blog image
        print("\nGenerating blog image...")
        image_prompt = await Runner.run(
            image_generator_agent,
            format_content_for_image_generation(final_content)
        )
        
        # Generate the actual image
        image_path = await generate_image(
            image_prompt.final_output["prompt"],
            image_prompt.final_output["parameters"]
        )
        
        print("\nFinal approved content with image:")
        print(final_content)
        print(f"\nBlog image generated: {image_path}")
        print("\nImage Generation Prompt:", image_prompt.final_output["prompt"])
        print("Image Parameters:", image_prompt.final_output["parameters"])

if __name__ == "__main__":
    asyncio.run(main())
