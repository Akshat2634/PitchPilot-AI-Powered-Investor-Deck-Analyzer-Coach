import logging
from app.ai.config import setup_logging
from app.ai.agents import pitch_analysis_agent, score_pitch_agent, workflow_classifier, router
from langgraph.graph import StateGraph, START, END
from app.schemas.pitch_schema import PitchData, EvaluationResponse, State, PitchAction

setup_logging()
logger = logging.getLogger(__name__)
    

class PitchGraph:
    def __init__(self):
        """Initialize the pitch workflow."""
        self.workflow = None
        self.compiled_app = None
        
        
    async def create_workflow(self) -> StateGraph:
        workflow = StateGraph(State)

        # nodes
        workflow.add_node("classifier", workflow_classifier)
        workflow.add_node("router",    router)
        workflow.add_node("pitch_analysis_agent", pitch_analysis_agent)
        workflow.add_node("score_pitch_agent",    score_pitch_agent)

        # start → classifier → router
        workflow.add_edge(START,      "classifier")
        workflow.add_edge("classifier","router")

        # router → (analysis | scoring | end)
        workflow.add_conditional_edges(
            "router",
            lambda state: state.get("next_step"),
            {
                PitchAction.ANALYSIS.value: "pitch_analysis_agent",
                PitchAction.SCORING.value:  "score_pitch_agent",
                "complete":      END
            }
        )

        # after each agent, go back through classifier → router
        workflow.add_edge("pitch_analysis_agent", "classifier")
        workflow.add_edge("score_pitch_agent",    "classifier")

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
        initial_state = {
            "pitch_data": pitch_data,
            "messages": [],
            "workflow_stage": None,
            "next_step": None,
            "feedback": None,
            "score": None
        }
        try:
            # Run the workflow
            result = await self.compiled_app.ainvoke(initial_state)
            
            # Create evaluation response from the result
            evaluation_response = EvaluationResponse(
                pitch=result.get("pitch_data"),
                feedback=result.get("feedback"),
                score=result.get("score")
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
    pitch_data = PitchData(pitch_text="Hi how are you? I am a startup that is building a new product that will help people to learn new things.", action=PitchAction.ANALYSIS.value)
    evaluation_response = asyncio.run(pitch_graph.analyze_pitch(pitch_data))
    print(evaluation_response)