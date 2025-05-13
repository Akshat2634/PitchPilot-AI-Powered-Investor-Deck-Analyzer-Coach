import logging
from app.ai.config import setup_logging
from app.ai.agents import pitch_analysis_agent, score_pitch_agent, supervisor_agent
from app.ai.config import State
from langgraph.graph import StateGraph, START, END , MessagesState
from app.schemas.pitch_schema import PitchData, EvaluationResponse

setup_logging()
logger = logging.getLogger(__name__)
    

class PitchGraph:
    def __init__(self):
        """Initialize the pitch workflow."""
        self.workflow = None
        self.compiled_app = None
        
        
    async def create_workflow(self) -> StateGraph:
        """
        Create the complete workflow graph with nodes and edges.

        Returns:
            StateGraph: The configured workflow graph
        """
        logger.info("Creating pitch workflow")

        # Create the workflow
        workflow = StateGraph(State)
        
        # Add nodes 
        workflow.add_node(supervisor_agent)
        workflow.add_node(pitch_analysis_agent)
        workflow.add_node(score_pitch_agent)
        
        # Add edges 
        workflow.add_edge(START, "supervisor_agent")

        self.workflow = workflow
        
        return workflow
    
    async def compile_workflow(self) -> None:
        """Compile the workflow for execution."""
        if not self.workflow:
            raise ValueError("Workflow not created. Call create_workflow first.")

        logger.info("Compiling pitch workflow")
        self.compiled_app = self.workflow.compile()
        

    async def analyze_pitch(self, pitch_data: PitchData) -> EvaluationResponse: 
        """Analyze a pitch and return the analysis results."""
        if not self.compiled_app:
            raise ValueError("Workflow not compiled. Call compile_workflow first.")
        
        logger.info("Analyzing pitch")
        initial_state = State(pitch_data=pitch_data)
        
        try:
            # Run the workflow
            result = await self.compiled_app.ainvoke(initial_state)
            
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

if __name__ == "__main__":
    import asyncio
    pitch_graph = PitchGraph()
    asyncio.run(pitch_graph.create_workflow())
    asyncio.run(pitch_graph.compile_workflow())
    pitch_data = PitchData(pitch_text="Hi how are you?")
    evaluation_response = asyncio.run(pitch_graph.analyze_pitch(pitch_data))
    print(evaluation_response)