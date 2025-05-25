import os
import time
import aiofiles
from config import CONSTS
from utils.constants import embed_files, EMB_FILE_FORMAT


def repo_path_for_user(user_id): 
    
    repo_path_for_user = os.path.join(CONSTS.local_repo, user_id)
    return repo_path_for_user   


async def file_upload_to_repo(user_id, input_files):
    
    abs_file_list = []
    skp_file_list = []
    start_time = time.time()
    dest_path = os.path.join(repo_path_for_user(user_id), embed_files)
    for uniq_file in input_files:
        
        fn = uniq_file.filename
        
        skip_file = validate_file_input_format(fn)
        
        if skip_file:
            skp_file_list.append(skip_file)
            continue
        
        dest_file = os.path.join(dest_path, fn)
        abs_file_list.append(dest_file)  
        file_path = uniq_file.file.name 
             
        async with aiofiles.open(dest_file, 'wb') as out_file:
            content = True
            while content:
                content = await uniq_file.read(10 * (2 ** 20))  # ~10MB
                await out_file.write(content)
        remove_file(file_path)
    total_time = time.time() - start_time 
    return abs_file_list, skp_file_list, total_time, EMB_FILE_FORMAT


def validate_file_input_format(input_file):
    
    ext_ = os.path.splitext(input_file)[1]
    
    if ext_ not in EMB_FILE_FORMAT:
        return input_file

    
def remove_file(file_path):
    
    if file_path is not None:
        os.remove(file_path)    
