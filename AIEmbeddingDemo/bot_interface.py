import json
import logging
import requests
import gradio as gr
import random, string
from config import CONSTS
from utils.support import record_closure

logging.setLogRecordFactory(record_closure(None))

def ai_emb_userinterface(user_message, chat_history, session_id):
    
    global session_
    
    if not chat_history:        
        session_ = session_id+''.join(random.choices(string.ascii_letters + string.digits, k=16))        
        
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded","X-Session-Id":session_}
    params_={"user_input":user_message, "chat_history":chat_history}
    
    try:
        response = requests.post(f"http://localhost:{int(CONSTS.app_port)}/triggerWorkflow", json=params_, headers=headers) 
        output_ = json.loads(response.text)
        
        if output_.get("download_flag",False):
            file_name = output_.get("file_name")
            chat_response = output_.get("chat_response")
            
            file_path = f"{CONSTS.local_repo}/{file_name}"
            final_output = f"{chat_response}, [{file_name}]({file_path})"
              
            
        else:
            final_output = output_.get('chat_response')
        
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        final_output = 'Server down, please try later!!!'
              
    return final_output


id_component = gr.State(value = 'ai_emb_ui')
sk_demo = gr.ChatInterface(ai_emb_userinterface,
                        additional_inputs = [id_component],
                        chatbot=gr.Chatbot(label='IVR queries!!!',
                                           avatar_images=('./images/user.png','./images/bot.png'),
                                           scale=1,
                                           height=400,
                                           type="messages",
                                           ),
                        title='AI Embeddings Demo',
                        textbox=gr.Textbox(placeholder="Type your queries here", container=False, scale=7,submit_btn=True),
                        type="messages"
                                             
                        )
if __name__ == "__main__":
    sk_demo.launch(share=True,server_port=int(CONSTS.gradio_port))