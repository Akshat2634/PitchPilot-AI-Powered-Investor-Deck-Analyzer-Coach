import logging
from app.config.logging_config import setup_logging
from app.ai.agents import pitch_analysis_agent, score_pitch_agent
from app.ai.config import State
from langgraph.graph import StateGraph, START, END
from app.schemas.pitch_schema import PitchData, EvaluationResponse

setup_logging()
logger = logging.getLogger(__name__)
    

class PitchGraph:
    def __init__(self):
        """Initialize the pitch workflow."""
        self.workflow = None
        self.compiled_app = None
        
    async def create_analysis_workflow(self) -> StateGraph:
        """
        Create the analysis workflow graph with nodes and edges.

        Returns:
            StateGraph: The configured analysis workflow graph
        """
        logger.info("Creating pitch analysis workflow")

        # Create the workflow
        workflow = StateGraph(State)
        
        # Add node
        workflow.add_node(pitch_analysis_agent)
        
        # Add edges 
        workflow.add_edge(START, pitch_analysis_agent)
        workflow.add_edge(pitch_analysis_agent, END)
        
        return workflow
        
    async def create_scoring_workflow(self) -> StateGraph:
        """
        Create the scoring workflow graph with nodes and edges.

        Returns:
            StateGraph: The configured scoring workflow graph
        """
        logger.info("Creating pitch scoring workflow")

        # Create the workflow
        workflow = StateGraph(State)
        
        # Add node
        workflow.add_node(score_pitch_agent)
        
        # Add edges 
        workflow.add_edge(START, score_pitch_agent)
        workflow.add_edge(score_pitch_agent, END)
        
        return workflow
        
    # async def create_workflow(self) -> StateGraph:
    #     """
    #     Create the complete workflow graph with nodes and edges.

    #     Returns:
    #         StateGraph: The configured workflow graph
    #     """
    #     logger.info("Creating pitch workflow")

    #     # Create the workflow
    #     workflow = StateGraph(State)
        
    #     # Add nodes
    #     workflow.add_node(pitch_analysis_agent)
    #     workflow.add_node(score_pitch_agent)
        
    #     # Add edges 
    #     workflow.add_edge(START, pitch_analysis_agent)
    #     workflow.add_edge(pitch_analysis_agent, score_pitch_agent)
    #     workflow.add_edge(score_pitch_agent, END)
        
    #     self.workflow = workflow
        
    #     return workflow
    
    # async def compile_workflow(self) -> None:
    #     """Compile the workflow for execution."""
    #     if not self.workflow:
    #         raise ValueError("Workflow not created. Call create_workflow first.")

    #     logger.info("Compiling pitch workflow")
    #     self.compiled_app = self.workflow.compile()
    
    
    async def compile_workflow_by_mode(self, mode: str) -> None:
        """
        Compile the appropriate workflow based on the pitch data mode.
        
        Args:
            mode: The mode of analysis ("analysis" or "score")
        """
        if mode == "analysis":
            self.workflow = await self.create_analysis_workflow()
        elif mode == "score":
            self.workflow = await self.create_scoring_workflow()
        else:
            raise ValueError(f"Invalid mode: {mode}. Must be 'analysis' or 'score'")
        
        logger.info(f"Compiling pitch workflow for mode: {mode}")
        self.compiled_app = self.workflow.compile()
        

    async def analyze_pitch(self, pitch_data: PitchData) -> EvaluationResponse: 
        """Analyze a pitch and return the analysis results."""
        if not self.compiled_app:
            raise ValueError("Workflow not compiled. Call compile_workflow first.")
        
        logger.info("Analyzing pitch")
        initial_state = State(pitch_data=pitch_data)
        
        try:
            # Run the workflow
            result = await self.compiled_app.ainvoke(initial_state, mode=pitch_data.mode)
            
            # Create evaluation response from the result
            evaluation_response = EvaluationResponse(
                pitch=result.get("pitch"),
                feedback=result.get("feedback"),
                questions=result.get("questions")
            )
            
            return evaluation_response
        except Exception as e:
            logger.error(f"Error processing pitch: {str(e)}")
            raise ValueError(f"Failed to process pitch: {str(e)}")
