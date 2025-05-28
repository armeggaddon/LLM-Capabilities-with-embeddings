import os
import logging
from pathlib import Path
from datetime import datetime
from functools import lru_cache
from utils.repository import repo_path_for_user
from utils.constants import sys_msg_dir, SYS_MSG_LOG, SYSTEM_MSG_CMN, ADMIN

logger = logging.getLogger(__name__)
old_factory = logging.getLogRecordFactory()


def record_closure(session_id):
    
    """This is used to embed the trace id in logs"""
    
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.session_id = session_id
        return record

    return record_factory

    
def write_system_message(user_id, module, sys_msg):
    
    try:
        module_file_name = module + '.txt'
        
        user_repo_path = repo_path_for_user(user_id)
        dir_path = os.path.join(user_repo_path, sys_msg_dir)
        
        sys_file = os.path.join(dir_path, module_file_name)
        if Path(sys_file).is_file():
            
            time_ = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
            new_sys_file = os.path.join(dir_path, module + "_" + time_)
            os.rename(sys_file, new_sys_file)
            
        with open(sys_file, "w") as file_:
            file_.write(sys_msg)
            
    
        return SYS_MSG_LOG.format(module)
    except Exception as e:
        logger.error(e)
        raise

    
@lru_cache(typed=True)
def extract_system_message(module):
    
    try:
        sys_msg = SYSTEM_MSG_CMN
        
        module_file_name = module + '.txt'
        user_repo_path = repo_path_for_user(ADMIN)
        sys_file = os.path.join(user_repo_path, sys_msg_dir, module_file_name)
        
        if Path(sys_file).is_file():
            with open(sys_file, 'r') as sys_file: 
                sys_msg = sys_file.read()
        
        return sys_msg     
    except TypeError:
        logger.error("Set the system message before proceeding")
        raise
