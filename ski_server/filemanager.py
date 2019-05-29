from flask import Blueprint, render_template, request,redirect, session,url_for, g
from . import db
from . import auth
import os
import enum
from os import listdir

FILE_TYPE_IDX = 1

class FILE_TYPE_ENUM(enum.IntEnum):
    DIRACTORY = 0
    IMAGE_FILE = 1
    NOT_IMAGE_FILE = 1


filemanager_blueprint= Blueprint('filemanager_blueprint', __name__,
                        template_folder='templates',url_prefix='/filemanager')


@filemanager_blueprint.route("/file_explorer")
@auth.login_required
def file_explorer_page_router():

    def get_file_list_from_path(dir_path):

        def set_file_type(file_path) :
            if os.path.isfile(file_path) :
                return FILE_TYPE_ENUM.NOT_IMAGE_FILE
            else :
                return FILE_TYPE_ENUM.DIRACTORY

        def sort_directory_first_in_list(file_list_from_dir):
            file_list_from_dir.sort(key=lambda file_with_type: file_with_type[FILE_TYPE_IDX])
            return file_list_from_dir



        file_list_from_dir= [(f, set_file_type(os.path.join(dir_path, f))) for f in listdir(dir_path)]
        return sort_directory_first_in_list(file_list_from_dir)


    root_dir_path = os.getenv("ROOT_DIRECTORY_PATH","C:\\Users\\누리꿈소프트\\Desktop")
    return render_template("filemanager/file_explorer.html",path=root_dir_path,fileListFromServer=get_file_list_from_path(root_dir_path))
