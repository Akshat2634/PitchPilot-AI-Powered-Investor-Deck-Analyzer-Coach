import os
from app.ai.pitch_analysis_tool import analyze_pitch_content, pretty_print_messages
from app.config.logging_config import setup_logging
import logging
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
import uuid


load_dotenv()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

model = os.getenv("OPENAI_MODEL")

# Create a checkpointer for persistence
checkpointer = InMemorySaver()

# Create agents with simplified prompts
pitch_analysis_agent = create_react_agent(
    model=init_chat_model(model),
    tools=[analyze_pitch_content],
    prompt=(
        "You are a world-class pitch analyst with expertise in venture capital evaluation frameworks.\n\n"
        "Analyze pitches based on clarity, differentiation, traction, scalability, market potential, and team strength.\n\n"
        "Provide structured feedback with overall assessment, strengths, weaknesses, opportunities, threats, and suggestions."
    ),
    name="pitch_analysis_agent",
    checkpointer=checkpointer
)

score_pitch_agent = create_react_agent(
    model=init_chat_model(model),
    tools=[analyze_pitch_content],
    prompt=(
        "You are a world-class pitch scoring expert with deep understanding of venture capital evaluation frameworks.\n\n"
        "Score pitches on criteria including clarity, differentiation, traction, scalability, and market potential.\n\n"
        "Provide a structured scoring analysis with numerical scores from 0-10 for each category."
    ),
    name="score_pitch_agent"
)

# Create supervisor with proper configuration
supervisor = create_supervisor(
    model=init_chat_model(model),
    agents=[pitch_analysis_agent, score_pitch_agent],
    prompt=(
        "You are a supervisor orchestrating a pitch evaluation workflow:\n"
        "- Use the pitch_analysis_agent to analyze and review startup pitches.\n"
        "- Use the score_pitch_agent to assign scores to pitches based on defined criteria.\n"
        "Assign work to only one agent at a time, never in parallel.\n"
        "Do not perform any analysis or scoring yourself—route tasks to the right agent.\n"
        "After each agent completes, review and decide the next step, until the process is done."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
    supervisor_name="supervisor"

).compile()

# Example usage
def analyze_pitch(pitch_text: str, thread_id: str = None):
    """
    Analyze a pitch using the supervisor and worker agents.
    
    Args:
        pitch_text: The pitch text to analyze
        thread_id: Optional thread ID for continuing conversations
    
    Returns:
        The final message history
    """
    # Create the input state
    input_state = {
        "messages": [
            {"role": "user", "content": f"Please analyze and score this pitch: {pitch_text}"}
        ]
    }
    
    # Create config with thread_id if provided
    config = {}
    if thread_id:
        config["configurable"] = {"thread_id": thread_id}
    
    # Stream the results
    last_chunk = None
    try:
        for chunk in supervisor.stream(input_state, config):
            pretty_print_messages(chunk, last_message=True)
            last_chunk = chunk
    except Exception as e:
        logger.error(f"Error during pitch analysis: {e}")
        raise
    
    # Return the final message history if available
    if last_chunk and "supervisor" in last_chunk and "messages" in last_chunk["supervisor"]:
        return last_chunk["supervisor"]["messages"]
    return []

# Example pitch text
example_pitch = "Our startup helps e-commerce brands improve conversion rates by using AI to generate personalized product videos at scale. We've onboarded 20 paying customers and achieved 30% MoM revenue growth since launch. The founding team has prior exits and deep e-commerce experience."

# Run an example analysis
if __name__ == "__main__":
    final_message_history = analyze_pitch(example_pitch, thread_id=str(uuid.uuid4()))