from flask import Blueprint, render_template, request,redirect, session,url_for, g
from . import db
from . import auth
import os
import enum
from os import listdir

filemanager_blueprint= Blueprint('filemanager_blueprint', __name__,
                        template_folder='templates',url_prefix='/filemanager')

@filemanager_blueprint.route("/file_explorer")
@auth.login_required
def file_explorer_page_router():

    root_dir_path = os.getenv("ROOT_DIRECTORY_PATH","C:\\Users\\누리꿈소프트\\Desktop")
    return render_template("filemanager/file_explorer.html",path=root_dir_path,filesWithJson=get_file_list_in_json(root_dir_path))

def get_file_list_in_json(dir_path):

    return [{"filename":f,"filetype":str(int(set_file_type(os.path.join(dir_path, f)))),"filepath":os.path.join(dir_path, f)} for f in listdir(dir_path)]

def set_file_type(file_path) :
    if os.path.isfile(file_path) :
        return FILE_TYPE_ENUM.NOT_IMAGE_FILE
    else :
        return FILE_TYPE_ENUM.DIRACTORY

class FILE_TYPE_ENUM(enum.IntEnum):
    DIRACTORY = 0
    IMAGE_FILE = 1
    NOT_IMAGE_FILE = 2



