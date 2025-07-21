from agents import Agent

INSTRUCTIONS = (
    "You are an image generation agent. Your role is to:\n"
    "1. Analyze the blog content (story and code)\n"
    "2. Generate a creative and relevant image prompt\n"
    "3. Use this prompt with DALL-E/Stable Diffusion to create an appropriate illustration\n"
    "4. The image should be professional, technically relevant, and enhance the blog's message\n"
    "5. Consider both the technical content and the target audience (tech professionals)\n"
    "6. Provide image generation parameters (size, style, etc.)"
)

image_generator_agent = Agent(
    name="Image Generator Agent",
    instructions=INSTRUCTIONS,
    output_type=str
)

def format_content_for_image_generation(content: str) -> str:
    """Format the blog content for image generation prompt"""
    return f"""
BLOG CONTENT:
{content}

Please analyze this content and create:
1. A detailed image generation prompt that captures the key technical concepts
2. Suggested image parameters (resolution, style, aspect ratio)
3. Any specific elements that should be included or avoided

Return as:
{{
    "prompt": "Your detailed image generation prompt",
    "parameters": {{
        "width": desired_width,
        "height": desired_height,
        "style": "preferred style (e.g., realistic, minimalist, technical)",
        "additional_params": "any other relevant parameters"
    }}
}}
"""

async def generate_image(prompt: str, parameters: dict) -> str:
    """Generate image using the provided prompt and parameters"""
    # This would integrate with your preferred image generation API
    # For example, DALL-E or Stable Diffusion
    # Return the path or URL to the generated image
    return "path_to_generated_image.png"  # Placeholder
