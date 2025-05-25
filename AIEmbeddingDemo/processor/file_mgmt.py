import os
import logging
import pypandoc
from processor.constants import DOCX, TXT
from utils.constants import ADMIN, embed_files, image_repo
from utils.repository import repo_path_for_user

logger = logging.getLogger(__name__)
repo_path = repo_path_for_user(ADMIN)

def file_processor(input_files):

    new_input_files = []
    skipped_files = []
    for input_file in input_files:
        ext_ = os.path.splitext(input_file)[1]

        if ext_ in [DOCX, TXT]:
            try:
                new_file_name = convert_files_to_emb_format(input_file)
                new_input_files.append(new_file_name)

            except Exception as e:
                skip_file = os.path.split(input_file)[1]
                skipped_files.append(skip_file)
                logger.error("Error in converting the file for accommodating image, skipping the file(s) " + skip_file)

    return new_input_files, skipped_files 


def convert_files_to_emb_format(input_file):
    
    try:
        _, file_ = os.path.split(input_file)
        file_name, _ = os.path.splitext(file_)
        new_file_name = f'{repo_path}/{embed_files}/{file_name}.txt'
        _ = pypandoc.convert_file(input_file,
                                     'html5',
                                     extra_args=[f'--extract-media={repo_path}/{image_repo}/{file_name}'],
                                     outputfile=new_file_name)
        return new_file_name
    except Exception as e:
        logger.error(e)
        raise