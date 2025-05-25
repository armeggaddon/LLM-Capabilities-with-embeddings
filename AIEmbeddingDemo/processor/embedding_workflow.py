import os
import shutil
import logging
import chromadb
from pathlib import Path
from processor.file_mgmt import file_processor
from utils.model_config import azure_openai_llm 
from utils.model_config import azure_openai_embed_model
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.storage.storage_context import StorageContext
from config import CONSTS
from utils.repository import repo_path_for_user
from utils.constants import ADMIN, embed_files, de_embed_files

logger = logging.getLogger(__name__)

from llama_index.core import Settings

Settings.llm = azure_openai_llm
Settings.embed_model = azure_openai_embed_model


def _enable_vector_store(collection_name, action_):
    
    vs_client = chromadb.HttpClient(host=CONSTS.chroma_host,
                                    port=CONSTS.chroma_port)
    chroma_collection = getattr(vs_client, action_)(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)  
    return vector_store 


def _enable_index(collection_name):
    
    vector_store = _enable_vector_store(collection_name, 'get_collection')
    
    index_ = VectorStoreIndex.from_vector_store(
        vector_store
    )
    return index_    


def create_data_embedding(collection_name, input_files_):
    
    new_input_files, skipped_files = file_processor(input_files_)
    
    if new_input_files:
        documents = SimpleDirectoryReader(input_files=new_input_files).load_data(show_progress=True)
        
        for document_ in documents:
            document_.doc_id = os.path.splitext(document_.metadata['file_name'])[0]
        
        vector_store = _enable_vector_store(collection_name, 'get_or_create_collection')
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        _ = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    
    return skipped_files
  

def delete_embeddings(collection_name, file_name_to_delete):
    
    try:
        filename_, _ = os.path.splitext(file_name_to_delete)
        index_ = _enable_index(collection_name)
        index_.delete_ref_doc(ref_doc_id=filename_)
        
        repo_path = repo_path_for_user(ADMIN)
        
        src_path = os.path.join(repo_path, embed_files, file_name_to_delete)
        dest_path = os.path.join(repo_path, de_embed_files, file_name_to_delete)
        shutil.move(src_path, dest_path)
        
        file_name_to_delete = f'{file_name_to_delete}.txt'
        # for original files, if present
        src_path_orig = os.path.join(repo_path, embed_files, file_name_to_delete)
        if Path(src_path_orig).is_file():  # check the file is present
            
            dest_path_orig = os.path.join(repo_path, de_embed_files, file_name_to_delete)
            shutil.move(src_path_orig, dest_path_orig)
        
        return f"Document {file_name_to_delete} removed from embeddings"
    except Exception as e:
        logger.error("Unable to delete the document {} from index".format(file_name_to_delete) , str(e))
        raise
