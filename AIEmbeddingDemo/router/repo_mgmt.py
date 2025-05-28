import os
import logging
from typing import List
from config import CONSTS
from datetime import datetime
from fastapi import APIRouter, Request, Form, UploadFile, File
from utils.repository import repo_path_for_user, file_upload_to_repo
from utils.support import write_system_message, extract_system_message
from utils.constants import embed_files, sys_msg_dir, image_repo, de_embed_files, ALL_FILES, EMBEDDED_FILES, ADMIN
from processor.embedding_workflow import create_data_embedding

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/makeRepo/", summary='create repository for storage', description='repository creation for storing datasets for analysis at later point')
def make_repo(request: Request):
    
    try:
        user_id = request.headers.get('x-user_id', 'admin')

        repo_path = repo_path_for_user(user_id)
        os.mkdir(repo_path)
        os.mkdir(os.path.join(repo_path, embed_files))
        os.mkdir(os.path.join(repo_path, sys_msg_dir))
        os.mkdir(os.path.join(repo_path, image_repo))
        os.mkdir(os.path.join(repo_path, de_embed_files))
        
        return 'Repository created successfully'
    
    except FileExistsError as e:
        logger.warning(e)
        return "Repository already exists"
    except Exception as e:
        logger.exception(e)   
        return str(e)   

    
@router.post("/listItems/", summary='show list of files in repository', description='displays the list of files present in repository for the given user')    
def list_items(request:Request, repository: str=Form(..., enum=[ALL_FILES, EMBEDDED_FILES])):
    
    user_id = request.headers.get('x-user_id', 'admin')
    details_dict = {}
    cnt = 0
    try: 
        list_of_scan_repo = []
        repo_path = repo_path_for_user(user_id)
        if repository == ALL_FILES:
            list_of_scan_repo.append(os.scandir(repo_path))
            
        embed_file_path = os.path.join(repo_path, embed_files)  # EMBEDDED REPO
        list_of_scan_repo.append(os.scandir(embed_file_path))
             
        for single_scan_repo in list_of_scan_repo:
            for entry in single_scan_repo:
                if entry.is_file():
                    cnt += 1
                    last_mod = datetime.fromtimestamp(entry.stat().st_mtime).strftime("%m/%d/%Y, %H:%M:%S")
                    details_dict.update({'file' + str(cnt):{"file_name":entry.name,
                                        "file_size(bytes)":os.path.getsize(entry),
                                        "last_modified":last_mod
                                        }})
        return details_dict
    except Exception as e:
        logger.exception(e)
        return str(e)     


@router.post("/setSystemMessage/", summary="Enter the system message to be set", description="""Enter the system message to be set for your usecase,
                                                                                    even though the validations are part of embeddings, system message is used to
                                                                                    pick the correct embeddings(it is a preface to your workflow""")
async def set_system_message(module:str, sys_msg:str): 
    
    try:
        output_ = write_system_message(ADMIN, module, sys_msg)
        return output_
    except Exception as e:
        logger.exception(e)
        return str(e)  


@router.post("/getSystemMessage/", summary="Get the system message which was set", description="""Get the system message for the usecase,
                                                                                   """)    
async def get_system_message(module:str): 
    
    try:
        output_ = extract_system_message(module)
        return output_
    except Exception as e:
        logger.exception(e)
        return str(e)     

    
@router.post("/createEmbeddings/", summary="Enter the system message to be set", description="""Enter the system message to be set for your usecase,
                                                                                    even though the validations are part of embeddings, system message is used to
                                                                                    pick the correct embeddings(it is a preface to your workflow""")    
async def create_embeddings(request:Request, module:str, input_files: List[UploadFile]=File(...)):
    
    skip_file_details = ""
    processing_error = ""
    emb_msg = ""
    try:
        user_id = ADMIN
        if CONSTS.repo_flag == 'None':
            
            abs_file_list, skp_file_list , _, sup_file_for = await file_upload_to_repo(user_id, input_files)
            
            if abs_file_list:
                skipped_files = create_data_embedding(module, abs_file_list)
                
                if skipped_files:
                    processing_error = "Unable to process the following files due to processing error, check logs for more details " + ", \n".join(skipped_files)
                
                emb_msg = "* Embeddings are created for module {}. \n * {}".format(module, processing_error)
            
            if skp_file_list:
                skip_file_details = "The following files are skipped due to unsupported extension: " + ", \n".join(skp_file_list) + \
                 ". Supported extensions are: " + ", ".join(sup_file_for)
                 
        return emb_msg + skip_file_details
    except Exception as e:
        logger.exception(e)
        return str(e)

    
@router.post("/deleteEmbeddings/", summary="Enter the system message to be set", description="""Enter the system message to be set for your usecase,
                                                                                    even though the validations are part of embeddings, system message is used to
                                                                                    pick the correct embeddings(it is a preface to your workflow""")        
async def delete_embeddings(request:Request, module:str, delete_doc:str):
    
    try:
        
        delete_embeddings(module, delete_doc)
    except Exception as e:
        logger.exception(e)
        return str(e)
