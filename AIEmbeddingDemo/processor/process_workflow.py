from processor.embedding_workflow import emb_query_workflow

def user_workflow(user_input, chat_history, workflow, session_id):
    
    output_ = emb_query_workflow(workflow, user_input, chat_history, workflow, session_id)
    
    final_output = {"chat_response":output_}
    return final_output
    
    
    
    
    
    
    