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


load_dotenv()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Workflow Classifier - Uses OpenAI to determine workflow stage based on user query
async def workflow_classifier(state: State) -> dict:
    """
    Use OpenAI to classify the current workflow stage based on user query and completed work.
    
    Args:
        state (State): Current application state
        
    Returns:
        dict: Updated state with workflow_stage
    """
    logger.info("=== WORKFLOW CLASSIFIER STARTED ===")
    logger.info("OpenAI workflow classifier determining current stage")
    
    try:
        # Get OpenAI client
        client = await get_openai_client()
        
        # Check what's already been completed
        has_feedback = state.get("feedback") is not None
        has_score = state.get("score") is not None
        pitch_data = state.get("pitch_data")
        pitch_text = pitch_data.pitch_text if pitch_data else ""
        input_action = pitch_data.action if pitch_data else ""
        logger.info(f"Pitch text: {pitch_text}")
        logger.info(f"State analysis - Has feedback: {has_feedback}, Has score: {has_score}")
        
        # Create prompt for OpenAI to classify workflow stage
        system_prompt = """
        [IDENTITY]
        You are a workflow classifier supervisor for a pitch analysis system. 
        You are an expert in the art of classifying workflow stages and have a deep understanding of the evaluation criteria and scoring rubrics of leading venture capital firms.

        [TASK]
        Based on the founder's pitch and input action, determine the next workflow stage.
        
        [RULES]
        - Based on the founder's pitch and input action, determine the next workflow stage.
        - Check if the requested action is already completed by determining if the feedback or score is not None.
        - If the requested action is not completed, classify as the requested action.
        - If the requested action is completed, classify as "complete". 
        
        [INPUT]
        - Founder's pitch: {pitch_text}
        - Input action: {input_action}
        - Has feedback: {has_feedback}
        - Has score: {has_score}
        
        [OUTPUT FORMAT]
        Return only one of: "analysis", "scoring", or "complete"
        """
        
        # Call OpenAI to classify workflow stage
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": system_prompt.format(pitch_text=pitch_text, input_action=input_action, has_feedback=has_feedback, has_score=has_score)}
            ],
            response_model=WorkflowClassifier,
            temperature=0.1
        )
        
        workflow_stage = response.workflow_stage
        logger.info(f"OpenAI classified workflow stage as: {workflow_stage}")
        
        logger.info("=== WORKFLOW CLASSIFIER COMPLETED ===")
        return {"workflow_stage": workflow_stage}
        
    except Exception as e:
        logger.error(f"Error in workflow classifier: {str(e)}")
        # Fallback to simple logic if OpenAI fails
        if not has_feedback:
            workflow_stage = PitchAction.ANALYSIS.value
        elif not has_score:
            workflow_stage = PitchAction.SCORING.value
        else:
            workflow_stage = "complete"
        
        logger.info(f"Fallback workflow stage: {workflow_stage}")
        return {"workflow_stage": workflow_stage}


# Router - Determines the next step based on workflow stage
def router(state: State) -> dict:
    """
    Route to the next step based on the current workflow stage.
    
    Args:
        state (State): Current application state
        
    Returns:
        dict: Updated state with next_step
    """
    logger.info("=== ROUTER STARTED ===")
    logger.info("Router determining next step")
    
    workflow_stage = state.get("workflow_stage", "analysis")
    logger.info(f"Current workflow stage: {workflow_stage}")
    
    if workflow_stage == "analysis":
        next_step = PitchAction.ANALYSIS.value
        logger.info("Routing to pitch analysis agent")
    elif workflow_stage == "scoring":
        next_step = PitchAction.SCORING.value
        logger.info("Routing to score pitch agent")
    else:  # complete
        next_step = "complete"
        logger.info("Workflow complete - routing to end")
    
    logger.info(f"Router directing to: {next_step}")
    logger.info("=== ROUTER COMPLETED ===")
    return {"next_step": next_step}


# Pitch Analysis Agent - Generates structured feedback  
async def pitch_analysis_agent(state: State) -> dict:
    """
    Analyze pitch content and generate structured feedback.
    
    Args:
        state (State): Current application state with pitch_data field populated
        
    Returns:
        dict: Updated state with feedback field populated
        
    Raises:
        ValueError: If pitch_data is missing in the state
        RuntimeError: If analysis process fails
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
        
        # Update the state with the feedback
        response = {
            "feedback": result,
            "messages": [AIMessage(content=str(result))]
        }
        
        logger.info("=== PITCH ANALYSIS AGENT COMPLETED SUCCESSFULLY ===")
        return response
        
    except Exception as e:
        logger.error(f"Error in pitch analysis agent: {str(e)}")
        logger.error("=== PITCH ANALYSIS AGENT FAILED ===")
        raise ValueError(f"Error in pitch analysis agent: {str(e)}")
    
    
# Score Pitch Agent - Generates structured scoring
async def score_pitch_agent(state: State) -> dict:
    """
    Analyze pitch content and generate structured scoring.
    
    Args:
        state (State): Current application state with pitch_data field populated
        
    Returns:
        dict: Updated state with score fields populated    

    Raises:
        ValueError: If pitch_data is missing in the state
        RuntimeError: If analysis process fails
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
        
        response = {
            "score": result,
            "messages": [AIMessage(content=str(result))]
        }
        
        logger.info("=== SCORE PITCH AGENT COMPLETED SUCCESSFULLY ===")
        return response
        
    except Exception as e:
        logger.error(f"Error in score pitch agent: {str(e)}")
        logger.error("=== SCORE PITCH AGENT FAILED ===")
        raise ValueError(f"Error in score pitch agent: {str(e)}")