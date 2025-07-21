from agents import Agent

REVIEW_INSTRUCTIONS = (
    "You are a review agent responsible for analyzing content and providing structured feedback. "
    "Analyze the content for technical accuracy, clarity, code correctness, and potential improvements."
)

FEEDBACK_COMPILER_INSTRUCTIONS = (
    "You are a feedback compilation agent. Your role is to:\n"
    "1. Analyze both LLM and human review feedback\n"
    "2. Combine and synthesize the feedback intelligently\n"
    "3. Apply the suggested improvements to the content\n"
    "4. Return the improved content while preserving the original structure"
)

# Agent for initial content review
review_agent = Agent(
    name="Review Agent",
    instructions=REVIEW_INSTRUCTIONS,
    output_type=str
)

# Agent for compiling and applying feedback
feedback_compiler_agent = Agent(
    name="Feedback Compiler Agent",
    instructions=FEEDBACK_COMPILER_INSTRUCTIONS,
    output_type=str
)

def format_content_for_review(content: str) -> str:
    """Format the content in a way that's easy to review"""
    return (
        "=== CONTENT FOR REVIEW ===\n\n"
        f"{content}\n\n"
        "=== REVIEW GUIDELINES ===\n"
        "Please provide feedback on:\n"
        "1. Technical accuracy\n"
        "2. Clarity and structure\n"
        "3. Code snippet correctness\n"
        "4. Suggested improvements\n\n"
        "Format your feedback as:\n"
        "- Technical: [your comments]\n"
        "- Clarity: [your comments]\n"
        "- Code: [your comments]\n"
        "- Improvements: [your comments]"
    )

def format_feedback_for_compilation(content: str, llm_feedback: str, human_feedback: str) -> str:
    """Format the content and feedback for the compiler agent"""
    return f"""
ORIGINAL CONTENT:
{content}

LLM REVIEW FEEDBACK:
{llm_feedback}

HUMAN REVIEW FEEDBACK:
{human_feedback}

Please analyze both reviews and generate improved content that:
1. Addresses technical feedback
2. Improves clarity and structure
3. Enhances code quality
4. Implements suggested improvements
5. Maintains the original content structure (Story/Code Snippets sections)
"""

def check_approval(feedback: str) -> bool:
    """Check if the review feedback contains explicit approval"""
    return "APPROVED" in feedback.upper()
