import os 
import csv
import xml.etree.ElementTree as ET
import sys

working_directory = os.getcwd()


def create_init(dir_path,import_file):
    with open(f"{dir_path}/__init__.py",'w') as file:
        file.write(f"from . import {import_file}")
        file.close()

def create_py_files(py_path,dir):
    with open(f'{py_path}/{dir}.py','w') as file:
        if dir == 'controllers':
            imports="""from odoo import SUPERUSER_ID, fields, http, _
            from odoo.api import Environment
            from odoo.exceptions import ValidationError
            from odoo.http import request
            """
        else:
           
            imports="""from odoo.exceptions import MissingError, UserError, ValidationError
            from odoo import api, fields, models, tools, _
            """
        file.write(imports)
        file.close()

def createModule(new_module_name):
    path_of_new_module = f"{working_directory}/{new_module_name}"
    os.makedirs(path_of_new_module)
    #create manifest and external init file
    manifest = ""
    with open(f'{path_of_new_module}/__manifest__.py','w') as file:
        file.write(manifest)
        file.close()
    #init file
    create_init(path_of_new_module,"models,contollers")
    return path_of_new_module 

#creating the folders and their files 
##views
def createViews(path_of_new_module):
    views_path = f"{path_of_new_module}/views"
    os.makedirs(views_path)
    #create views.xml and add odoo elements to it 
    views_xml_file = ET.Element('odoo')
    views_xml_file.text = " "
    tree = ET.ElementTree(views_xml_file).write(f"{views_path}/views.xml")
    

def createData(path_of_new_module):
    ## creating the data file
    data_path = f"{path_of_new_module}/data"
    os.makedirs(data_path)
    data_xml_file = ET.Element('odoo')
    data_tag = ET.SubElement(data_xml_file,"data", noupdate="0") 
    data_tag.text=" "
    tree = ET.ElementTree(data_xml_file).write(f"{data_path}/data.xml")

def createSecurity(path_of_new_module):
    ##security 
    security_path = f"{path_of_new_module}/security"
    os.makedirs(security_path)

    #write security csv
    csv_elements=["id","name","model_id:id","group_id:id","perm_read","perm_write","perm_create","perm_unlink"]
    with open(f'{security_path}/ir.model.access.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_elements)

    #rule.xml
    with open(f"{security_path}/ir.rule.xml",'w') as file:
        security_xml_file = ET.Element('odoo')
        data_tag = ET.SubElement(security_xml_file,"data") 
        data_tag.text=" "
        tree = ET.ElementTree(security_xml_file).write(f"{security_path}/ir.rule.xml")
        

def createControllers(path_of_new_module):
    controllers_path = f"{path_of_new_module}/controllers"
    os.makedirs(controllers_path)
    create_init(controllers_path,"contollers")
    create_py_files(controllers_path,"contollers")

def createModels(path_of_new_module):
    models_path = f"{path_of_new_module}/models"
    os.makedirs(models_path)
    create_init(models_path,"models")
    create_py_files(models_path,"models")

def createStatic(path_of_new_module):
    static_path = f"{path_of_new_module}/static"
    os.makedirs(static_path)
    css_path = f"{static_path}/css"
    os.makedirs(css_path)
    js_path = f"{static_path}/js"
    os.makedirs(js_path)
    description_path = f"{static_path}/description"
    os.makedirs(description_path)
    images_path = f"{static_path}/images"
    os.makedirs(images_path)

directories = os.listdir(working_directory)
print(directories)
new_module = sys.argv[1]

if new_module in directories:
    raise "Module name already exists"
else:
    created_module = createModule(new_module_name=new_module)
    createSecurity(created_module)
    createViews(created_module)
    createData(created_module)
    createControllers(created_module)
    createModels(created_module)
    createStatic(created_module)



