import os
from typing import Literal
from app.ai.config import get_openai_client
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config.logging_config import setup_logging
import logging
from app.ai.config import get_openai_client, parse_openai_response
from dotenv import load_dotenv
from app.schemas.pitch_schema import FeedbackModel, ScoreModel, WorkflowClassifier, State, PitchAction
from langchain_core.messages import AIMessage
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.graph import END


load_dotenv()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# OpenAI Supervisor - Uses OpenAI to determine which agent to call next
async def supervisor(state: State) -> Command[Literal["pitch_analysis_agent", "score_pitch_agent", "__end__"]]:
    """
    OpenAI-powered supervisor that determines which agent to call next based on user query and completed work.
    
    Args:
        state (State): Current application state
        
    Returns:
        Command: Routing command to next agent or end
    """
    logger.info("=== SUPERVISOR STARTED ===")
    logger.info("OpenAI supervisor determining next agent")
    
    try:
        # Get OpenAI client
        client = await get_openai_client()
        
        # Check what's already been completed
        has_feedback = state.get("feedback") is not None
        has_score = state.get("score") is not None
        user_query = state.get("user_query", "")

        
        logger.info(f"State analysis - Has feedback: {has_feedback}, Has score: {has_score}")
        logger.info(f"User query: {user_query}")
        
        # Create prompt for OpenAI to determine next agent
        system_prompt = """
        [IDENTITY]
        You are a workflow supervisor for a pitch analysis system.
        You are an expert in routing workflows with deep knowledge of evaluation criteria and scoring rubrics used by top venture capital firms.

        [TASK]
        Based on the founder's pitch and the user's query, determine which agent to call next.

        [CONTEXT]
        - Current state: has_feedback={has_feedback}, has_score={has_score}
        - User query: {user_query}
        - Available agents: "pitch_analysis_agent" (provides detailed feedback), "score_pitch_agent" (provides numerical scores)

        [ROUTING RULES]
        [CASE 1]
        1. If the user explicitly requests ONLY scoring (e.g., "provide just the score", "score only", "what's the score") AND no score exists, route to "score_pitch_agent"
        2. If the user requests ONLY scoring, and score ALREADY EXISTS, return "complete".
        
        [CASE 2]
        1. If the user explicitly requests ONLY analysis/feedback AND no feedback exists, route to "pitch_analysis_agent" 
        2. If the user requests ONLY analysis/feedback, and feedback ALREADY EXISTS, return "complete".
        
        [CASE 3]
        1. If the user query requests both analysis and scoring or is general/ambiguous:
            - If no feedback exists, route to "pitch_analysis_agent"
            - If feedback exists but no score exists, route to "score_pitch_agent"
        2. If both feedback and score exist (or the requested tasks are complete), return "__end__"
        
        
        [CASE 4]
        1. Default: if nothing exists, start with "pitch_analysis_agent"
        
        [OUTPUT FORMAT]
        Return exactly one of: "analysis", "scoring", or "complete"
        """
        
        # Call OpenAI to determine next agent
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_SUPERVISOR"),
            messages=[
                {"role": "system", "content": system_prompt.format(
                    has_feedback=has_feedback, 
                    has_score=has_score,
                    user_query=user_query
                )},
                {"role": "user", "content": f"Route this request: {user_query}"}
            ],
            response_model=WorkflowClassifier,
            temperature=0.1
        )
        
        next_agent = response.workflow_stage
        if next_agent == PitchAction.ANALYSIS:
            next_agent = "pitch_analysis_agent"
        elif next_agent == PitchAction.SCORING:
            next_agent = "score_pitch_agent"
        elif next_agent == PitchAction.COMPLETE:
            next_agent = END
            
        logger.critical(f"Supervisor routing to: {next_agent}")
        logger.info("=== SUPERVISOR COMPLETED ===")
        
        return Command(goto=next_agent)
        
    except Exception as e:
        logger.error(f"Error in supervisor: {str(e)}")
        # Fallback logic if OpenAI fails
        if not has_feedback:
            next_agent = "pitch_analysis_agent"
        elif not has_score:
            next_agent = "score_pitch_agent"
        else:
            next_agent = END
        
        logger.info(f"Fallback supervisor routing to: {next_agent}")
        return Command(goto=next_agent)


# Pitch Analysis Agent - Generates structured feedback  
async def pitch_analysis_agent(state: State) -> Command[Literal["supervisor"]]:
    """
    Analyze pitch content and generate structured feedback.
    
    Args:
        state (State): Current application state with pitch_data field populated
        
    Returns:
        Command: Updated state with feedback and route back to supervisor
    """
    logger.info("=== PITCH ANALYSIS AGENT STARTED ===")
    logger.info("Starting pitch analysis agent")
    
    try:
        pitch_data = state.get("pitch_data")
        if not pitch_data:
            logger.error("No pitch data found in state")
            raise ValueError("No pitch data found in state")
        
        logger.info(f"Pitch data received - text length: {len(pitch_data.pitch_text)} characters")
        logger.info("Creating analysis prompt template")
            
        prompt = ChatPromptTemplate.from_template(
            """
            [IDENTITY]
            You are a world‑class pitch analyst, steeped in the frameworks and best practices of leading venture capital firms—Y Combinator, Sequoia Capital, Andreessen Horowitz (a16z), Benchmark, Accel, and Greylock Ventures.

            [TASK]
            Assess the following pitch content with the rigor of a YC partner and an a16z investor. Apply the evaluation standards, scoring rubrics, and qualitative insights these firms use when vetting founders.

            [EVALUATION CRITERIA]
            1. Clarity: How clearly does the pitch articulate the problem, solution, and unique value proposition? 
            2. Differentiation: How distinct and defensible is the offering compared to direct and indirect competitors? 
            3. Traction: How convincingly does the pitch demonstrate early user/customer validation, revenue, or growth metrics? 
            4. Scalability: How well does the pitch show the potential to expand market reach, grow margins, and leverage network effects? 
            5. Market Potential: How well-defined and sizable is the Total Addressable Market (TAM)? 
            6. Team Strength: How effectively does the pitch convey the founding team's domain expertise and execution capability? 
            
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
        
        logger.info("Getting OpenAI client")
        client = await get_openai_client()
        
        logger.info("Sending request to OpenAI for pitch analysis")
        logger.info(f"Using model: {os.getenv('OPENAI_MODEL')}")
        
        result = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            response_model=FeedbackModel,
            temperature=0.2,
            messages=[
                {"role": "developer", "content": prompt.format(pitch_text=pitch_data.pitch_text)}
            ]
        )
        
        logger.info("Successfully received feedback from OpenAI")
        logger.info(f"Feedback generated - Overall feedback length: {len(result.overall_feedback)} characters")
        logger.info("=== PITCH ANALYSIS AGENT COMPLETED SUCCESSFULLY ===")
        
        return Command(
            goto="supervisor",
            update={
                "feedback": result,
                "messages": state.get("messages", []) + [AIMessage(content=str(result))]
            }
        )
        
    except Exception as e:
        logger.error(f"Error in pitch analysis agent: {str(e)}")
        logger.error("=== PITCH ANALYSIS AGENT FAILED ===")
        raise ValueError(f"Error in pitch analysis agent: {str(e)}")
    
    
# Score Pitch Agent - Generates structured scoring
async def score_pitch_agent(state: State) -> Command[Literal["supervisor"]]:
    """
    Analyze pitch content and generate structured scoring.
    
    Args:
        state (State): Current application state with pitch_data field populated
        
    Returns:
        Command: Updated state with scores and route back to supervisor
    """
    logger.info("=== SCORE PITCH AGENT STARTED ===")
    logger.info("Starting score pitch agent")
    
    try:
        pitch_data = state.get("pitch_data")
        if not pitch_data:
            logger.error("No pitch data found in state")
            raise ValueError("No pitch data found in state")
        
        logger.info(f"Pitch data received - text length: {len(pitch_data.pitch_text)} characters")
        logger.info("Creating scoring prompt template")
            
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
        
        logger.info("Getting OpenAI client")
        client = await get_openai_client()
        
        logger.info("Sending request to OpenAI for pitch scoring")
        logger.info(f"Using model: {os.getenv('OPENAI_MODEL')}")
        
        result = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            response_model=ScoreModel,
            temperature=0.2,
            messages=[
                {"role": "developer", "content": prompt.format(pitch_text=pitch_data.pitch_text)}
            ]
        )
        
        logger.info("Successfully received scores from OpenAI")
        logger.info(f"Scores generated - Overall: {result.overall}, Clarity: {result.clarity}, Differentiation: {result.differentiation}, Traction: {result.traction}, Scalability: {result.scalability}")
        logger.info("=== SCORE PITCH AGENT COMPLETED SUCCESSFULLY ===")
        
        return Command(
            goto="supervisor",
            update={
                "score": result,
                "messages": state.get("messages", []) + [AIMessage(content=str(result))]
            }
        )
        
    except Exception as e:
        logger.error(f"Error in score pitch agent: {str(e)}")
        logger.error("=== SCORE PITCH AGENT FAILED ===")
        raise ValueError(f"Error in score pitch agent: {str(e)}")