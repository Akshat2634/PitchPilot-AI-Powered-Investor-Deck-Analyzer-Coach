import logging
from app.ai.config import setup_logging
from app.ai.agents import supervisor, pitch_analysis_agent, score_pitch_agent
from langgraph.graph import StateGraph, START
from app.schemas.pitch_schema import PitchData, EvaluationResponse, State
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState




setup_logging()
logger = logging.getLogger(__name__)
    
# Initialize the memory saver
memory = MemorySaver()

class PitchGraph:
    def __init__(self):
        """Initialize the pitch workflow."""
        self.workflow = None
        self.compiled_app = None
        
        
    async def create_workflow(self) -> StateGraph:
        """Create the workflow graph using the new Command pattern."""
        workflow = StateGraph(State)

        # Add nodes - supervisor and agents
        workflow.add_node("supervisor", supervisor)
        workflow.add_node("pitch_analysis_agent", pitch_analysis_agent)
        workflow.add_node("score_pitch_agent", score_pitch_agent)

        # Start with supervisor
        workflow.add_edge(START, "supervisor")

        self.workflow = workflow
        return workflow
    
    async def compile_workflow(self) -> None:
        """Compile the workflow for execution."""
        if not self.workflow:
            raise ValueError("Workflow not created. Call create_workflow first.")

        logger.info("Compiling pitch workflow")
        # Use memory saver to prevent memory leaks in long-running workflows
        self.compiled_app = self.workflow.compile(checkpointer=memory)
        

    async def analyze_pitch(self, pitch_data: PitchData) -> EvaluationResponse: 
        """Analyze a pitch and return the analysis results."""
        if not self.workflow:
            await self.create_workflow()

        if not self.compiled_app:
            await self.compile_workflow()
        
        logger.info("Analyzing pitch")
        initial_state = {
            "pitch_data": pitch_data,
            "user_query": pitch_data.user_query,
            "messages": [],
            "workflow_stage": None,
            "next_step": None,
            "feedback": None,
            "score": None
        }
        
        try:
            # Run the workflow with a unique thread ID to prevent memory leaks
            # Each invocation gets its own thread to avoid state accumulation
            import uuid
            thread_id = str(uuid.uuid4())
            config = {"configurable": {"thread_id": thread_id}}
            
            result = await self.compiled_app.ainvoke(initial_state, config=config)
            
            # Create evaluation response from the result
            evaluation_response = EvaluationResponse(
                pitch=result.get("pitch_data"),
                feedback=result.get("feedback"),
                score=result.get("score")
            )
            
            # Clear references to prevent memory retention
            initial_state.clear()
            result = None
            
            return evaluation_response
        except Exception as e:
            logger.error(f"Error processing pitch: {str(e)}")
            # Clean up state on error to prevent memory leaks
            initial_state.clear()
            raise ValueError(f"Failed to process pitch: {str(e)}")
        finally:
            # Ensure cleanup happens even if an exception occurs
            if 'initial_state' in locals():
                initial_state.clear()

if __name__ == "__main__":
    import asyncio
    pitch_graph = PitchGraph()
    pitch_data = PitchData(
        pitch_text="Hi how are you? I am a startup that is building a new product that will help people to learn new things.", 
        user_query="Please provide just the feedback for this pitch"
    )
    evaluation_response = asyncio.run(pitch_graph.analyze_pitch(pitch_data))
    print(evaluation_response)