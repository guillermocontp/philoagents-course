@lru_cache(maxsize=1)
def create_workflow_graph_raw_context():
    graph_builder = StateGraph(PhilosopherState)

    # NODES
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("retrieve_philosopher_context", retriever_node)
    # DELETED: graph_builder.add_node("summarize_context_node", summarize_context_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    graph_builder.add_node("connector_node", connector_node)
    
    # FLOW
    graph_builder.add_edge(START, "conversation_node")
    
    graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition,
        {
            "tools": "retrieve_philosopher_context",
            END: "connector_node"
        }
    )

    # MODIFIED EDGE: Go straight from Retriever back to Conversation
    # (The "Brain" now reads the raw book pages directly)
    graph_builder.add_edge("retrieve_philosopher_context", "conversation_node")
    
    # Tail logic remains the same
    graph_builder.add_conditional_edges("connector_node", should_summarize_conversation)
    graph_builder.add_edge("summarize_conversation_node", END)
    
    return graph_builder





@lru_cache(maxsize=1)
def create_workflow_graph_stateless():
    graph_builder = StateGraph(PhilosopherState)

    # NODES
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("retrieve_philosopher_context", retriever_node)
    graph_builder.add_node("summarize_context_node", summarize_context_node)
    
    # DELETED: Connector and Summarize Conversation nodes
    
    # FLOW
    graph_builder.add_edge(START, "conversation_node")
    
    # MODIFIED CONDITIONAL EDGE:
    # If we are done talking, go straight to END. Do not pass Go. Do not Collect Summary.
    graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition,
        {
            "tools": "retrieve_philosopher_context",
            END: END  # Direct exit!
        }
    )
    
    graph_builder.add_edge("retrieve_philosopher_context", "summarize_context_node")
    graph_builder.add_edge("summarize_context_node", "conversation_node")
    
    return graph_builder
