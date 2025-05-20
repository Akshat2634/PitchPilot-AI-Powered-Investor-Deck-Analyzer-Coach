from typing import Any, Dict
from langchain_core.messages import convert_to_messages
from langchain_core.tools import tool


# Pretty print messages
def pretty_print_message(message, indent=False):
    """Print a single message in a pretty format."""
    if hasattr(message, "pretty_repr"):
        pretty_message = message.pretty_repr(html=True)
    else:
        pretty_message = f"{message.get('role', 'unknown')}: {message.get('content', '')}"
    
    if not indent:
        print(pretty_message)
        return

    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    print(indented)

# Pretty print messages from chunks of messages
def pretty_print_messages(update, last_message=False):
    """Print messages from chunks in a readable format."""
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        print(update_label)
        print("\n")

        if "messages" in node_update:
            messages = convert_to_messages(node_update["messages"])
            if last_message:
                messages = messages[-1:]

            for m in messages:
                pretty_print_message(m, indent=is_subgraph)
            print("\n")
            
# Create a tool to process the pitch using LangChain's tool decorator
@tool
def analyze_pitch_content(pitch_text: str) -> str:
    """
    Analyze the pitch content provided.
    
    Args:
        pitch_text: The pitch text to analyze
        
    Returns:
        Analysis of the pitch
    """
    return f"Received pitch text: {pitch_text}"