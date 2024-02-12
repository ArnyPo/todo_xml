import xml.etree.ElementTree as ET
import datetime

FILE = "test.xml"

def newProject(root, project_name:str, project_desc:str="New project"):
    # root is the place where to add the project
    # generally right in the list
    new_id = getNewID(root,"project")
    project = ET.SubElement(root, "project")
    project.set("id", new_id)
    
    name = ET.SubElement(project,"name")
    name.text = project_name
    
    desc = ET.SubElement(project, "desc")
    desc.text = project_desc
    
    tasks = ET.SubElement(project, "tasks")
    return project
    
def newTask(root, task_name, task_due, task_desc="New task"):
    # root is project or task so that we can determine the starting id
    tasks = root.find("tasks") or root.find("subtasks")
    new_id = getNewID(root,"task")
    task = ET.SubElement(tasks, "task")
    task.set("id", new_id)
    task.set("name", task_name)
    
    due = newDate(task, task_due)
        
    desc = ET.SubElement(task, "desc")
    desc.text = task_desc
    
    subtasks = ET.SubElement(task, "subtasks")
    return task
    
def newDate(root, date):
    # date format is YYYY-MM-DD HH:MM:SS
    iso_date =  datetime.datetime.fromisoformat(date).timetuple()
    
    due = ET.SubElement(root,"due_date")
    
    year = ET.SubElement(due, "year")
    year.text = str(iso_date.tm_year)
    month = ET.SubElement(due,"month")
    month.text = str(iso_date.tm_mon)
    day = ET.SubElement(due, "day")
    day.text = str(iso_date.tm_mday)
    
    # TODO what to do when no time was inputed - tuple has 0,0,0
    time = ET.SubElement(due, "time")
    time.text = str(iso_date.tm_hour) + "-" + str(iso_date.tm_min) + "-" + str(iso_date.tm_sec)
    
    return due

def findElementTasks(root, id:str):
    # if we are searching for specific tasks
    if "." in id:
        element = root.find(f".//task[@id='{id}']")
        if element is not None:
            element = element.find("subtasks")
        else:
            raise ValueError(f"No task was found under id:{id}")       
        
    # if we are searching for a project
    else:
        element = root.find(f".//project[@id='{id}']")
        if element is not None:
            element = element.find("tasks")
        else:
            raise ValueError(f"No project was found under id:{id}")
        
    return element

def findElement(root, id):
    return root.find(f".//task[@id='{id}']") or root.find(f".//project[@id='{id}']")
    
def getNewID(root, type) -> str:
    # look at the types that are on the same level
    # get the max id
    max_id = 0
    root_id = root.get("id")
    if root_id is None: 
        root_id = ""
    else: root_id += "."
    
    if type=="task":
        tasks = root.find("tasks") or root.find("subtasks")
        
        for task in tasks.findall("task"):
            task_id = int(task.get("id").split(".")[-1])
            max_id = max(max_id, task_id)
    else:
        projects = root.findall("project")
        
        for project in projects:
            p_id = int(project.get("id"))
            max_id = max(max_id,p_id)
            
    return root_id + str(max_id+1)
            
if __name__ == '__main__':
    tree = ET.parse(FILE)
    root = tree.getroot()  
    
    newTask(findElement(root,"1"),"n","2024-01-01")
    
    ET.indent(tree, space="\t")
    tree.write(FILE)