import os
from typing import Literal
from app.ai.config import get_openai_client, State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config.logging_config import setup_logging
import logging
from app.ai.config import get_openai_client, parse_openai_response
from dotenv import load_dotenv
from app.schemas.pitch_schema import FeedbackModel, ScoreModel, NextAgentResponse
from langgraph.types import Command
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage


load_dotenv()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Supervisor Agent - Orchestrates the pitch evaluation workflow
async def supervisor_agent(state: MessagesState) -> Command[Literal["pitch_analysis_agent", "score_pitch_agent", "END"]]:
    """
    Supervisor agent that orchestrates the pitch evaluation workflow.
    
    This agent determines which specialized agent to call next based on the current state
    of the evaluation process. It ensures that agents are called in the correct sequence
    
    Args:
        state (State): Current application state
        
    Returns:
        Command: Instruction on which agent to call next or to end the process  
        
    Raises:
        ValueError: If there's an error determining the next step
    """
    logger.info("Supervisor agent determining next step")
    
    client = await get_openai_client()
    
    prompt = ChatPromptTemplate.from_template(
        """
        [IDENTITY]
        You are a workflow supervisor agent responsible for orchestrating the pitch evaluation process by calling the appropriate agents.

        [TASK]
        Determine which specialized agent to call next in the pitch evaluation workflow based on the user's request.
        
        [WORKFLOW LOGIC]
        - If user wants to analyze the pitch, call "pitch_analysis_agent"
        - If user wants to score the pitch, call "score_pitch_agent"
        
        [OUTPUT FORMAT]
        Return a JSON with these fields:
        - agent_name: The next agent to call ("pitch_analysis_agent", "score_pitch_agent", or "END")
        """
    )
    
    response = await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages= [{"role": "developer", "content": prompt}],
        response_format=NextAgentResponse
    )
    
    parsed_response = await parse_openai_response(response)
    response_data = NextAgentResponse.model_validate_json(parsed_response)
    
    return Command(
        goto=response_data.agent_name,
        update={"messages": [AIMessage(content=response)]}
    )
        

# Pitch Analysis Agent - Generates structured feedback  
async def pitch_analysis_agent(state: MessagesState) -> Command[Literal["supervisor"]]:
    """
    Analyze pitch content and generate structured feedback and scoring.
    
    This agent processes the pitch data from the state and leverages OpenAI's language models
    to evaluate the pitch quality. It populates the state's feedback and score fields with
    detailed assessment information.
    
    The function works with the State TypedDict defined in config.py, which contains:
    - pitch_data: Extracted text from the uploaded pitch
    - feedback: Structured feedback (strengths, weaknesses, suggestions)
    
    Args:
        state (State): Current application state with pitch_data field populated
        
    Returns:
        State: Updated state with feedback and score fields populated
        
    Raises:
        ValueError: If pitch_data is missing in the state
        RuntimeError: If analysis process fails
    """
    logger.info("Starting pitch analysis agent")
    try:
        prompt = ChatPromptTemplate.from_template(
            """
            [IDENTITY]
            You are a world‑class pitch analyst, steeped in the frameworks and best practices of leading venture capital firms—Y Combinator, Sequoia Capital, Andreessen Horowitz (a16z), Benchmark, Accel, and Greylock Ventures.

            [TASK]
            Assess the following pitch content with the rigor of a YC partner and an a16z investor. Apply the evaluation standards, scoring rubrics, and qualitative insights these firms use when vetting founders.

            [EVALUATION CRITERIA]
            1. Clarity: How clearly does the pitch articulate the problem, solution, and unique value proposition? (Score 0–10)
            2. Differentiation: How distinct and defensible is the offering compared to direct and indirect competitors? (Score 0–10)
            3. Traction: How convincingly does the pitch demonstrate early user/customer validation, revenue, or growth metrics? (Score 0–10)
            4. Scalability: How well does the pitch show the potential to expand market reach, grow margins, and leverage network effects? (Score 0–10)
            5. Market Potential: How well-defined and sizable is the Total Addressable Market (TAM)? (Score 0–10)
            6. Team Strength: How effectively does the pitch convey the founding team's domain expertise and execution capability? (Score 0–10)
            
            [INPUT]
            - ELEVATOR PITCH CONTENT: {pitch_text}

            [OUTPUT FORMAT]
            Provide a structured output with these sections:

            1. **Overall Feedback:** A concise summary and rationale of the pitch.
            2. **Strengths:** Highlight the pitch's strongest elements, citing examples.
            3. **Weaknesses:** Pinpoint key gaps or shortcomings, with context.
            4. **Opportunities:** Identify untapped angles or areas ripe for expansion.
            5. **Threats:** Surface potential risks or competitive headwinds not adequately addressed.
            6. **Suggestions for improvement:** Specific, prioritized steps to elevate the pitch, referencing YC/a16z playbooks where relevant.
            
            """
    
    )
        client = await get_openai_client()
        result = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            response_format=FeedbackModel,
            temperature=0.2,
            messages=[
                {"role": "developer", "content": prompt.format(pitch_text=state.pitch_data.pitch_text)}
            ]
        )
        response = await parse_openai_response(result)
        feedback = FeedbackModel.model_validate_json(response)
        
        # Update the state with the feedback and return a Command to go to supervisor
        return Command(
            goto="supervisor",
            update={"feedback": feedback,
                    "messages": [AIMessage(content=response)] }
        )
    except Exception as e:
        logger.error(f"Error in pitch analysis agent: {str(e)}")
        raise ValueError(f"Error in pitch analysis agent: {str(e)}")
    
    
# Score Pitch Agent - Generates structured scoring
async def score_pitch_agent(state: MessagesState) -> Command[Literal["supervisor"]]:
    """
    Analyze pitch content and generate structured scoring.
    
    This agent processes the pitch data from the state and leverages OpenAI's language models
    to evaluate the pitch quality. It populates the state's score fields with
    detailed assessment information.    
    
    Args:
        state (State): Current application state with pitch_data field populated
        
    Returns:
        State: Updated state with score fields populated    

    Raises:
        ValueError: If pitch_data is missing in the state
        RuntimeError: If analysis process fails
    """
    logger.info("Starting score pitch agent")
    try:
        prompt = ChatPromptTemplate.from_template(
            """
            [IDENTITY]
            You are a world-class pitch analyst, leveraging the rigorous vetting frameworks of top venture firms—including Y Combinator, Sequoia Capital, Andreessen Horowitz (a16z), Benchmark, Accel, and Greylock Ventures.
            You are an expert in the art of scoring pitches and have a deep understanding of the evaluation criteria and scoring rubrics of leading venture capital firms.

            [TASK]
            Given the founder's pitch, produce a structured scoring rubric that quantifies and justifies the pitch's strengths across key dimensions.

            [EVALUATION CRITERIA]
            1. Clarity: How clearly the pitch conveys the problem, solution, and unique value proposition.
            2. Differentiation: How defensibly the offering stands out against competitors.
            3. Traction: The strength of demonstrated user/customer validation, revenue, or engagement metrics.
            4. Scalability: Evidence of potential to expand market reach, improve margins, and leverage network effects.
            5. Market Potential: The size and potential of the Total Addressable Market.
            6. Team Strength: The quality and experience of the founding team.

            [INPUT]
            - PITCH_TEXT: {pitch_text}

            [OUTPUT FORMAT]
            Provide a structured scoring analysis with these sections:

            1. Clarity: Score from 0 to 10 
            2. Differentiation: Score from 0 to 10 
            3. Traction: Score from 0 to 10 
            4. Scalability: Score from 0 to 10 
            5. Overall: Score from 0 to 10 
            """
        )
        
        client = await get_openai_client()
        result = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            response_format=ScoreModel,
            temperature=0.2,
            messages=[
                {"role": "developer", "content": prompt.format(pitch_text=state.pitch_data.pitch_text)}
            ]
        )
        response = await parse_openai_response(result)
        score = ScoreModel.model_validate_json(response)
        
        return Command(
            goto="supervisor",
            update={"score": score,
                    "messages": [AIMessage(content=response)]}
        )
    except Exception as e:
        logger.error(f"Error in score pitch agent: {str(e)}")
        raise ValueError(f"Error in score pitch agent: {str(e)}")