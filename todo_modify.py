import xml.etree.ElementTree as ET
from datetime import datetime

class TodoListModify:
    def __init__(self, xml_file:str):
        self.file:str = xml_file
        self.tree:ET.ElementTree = ET.parse(xml_file)
        self.root:ET.ElementTree = self.tree.getroot()
    
    def writeToFile(self):
        ET.indent(self.tree, space="\t")
        self.tree.write(self.file)
        
    def newProject(self, project_name:str, project_desc:str="New project") -> str:
        # root is the place where to add the project
        # generally right in the list
        new_id = self.getNewID(self.root,"project")
        project = ET.SubElement(self.root, "project")
        project.set("id", new_id)
        
        name = ET.SubElement(project,"name")
        name.text = project_name
        
        desc = ET.SubElement(project, "desc")
        desc.text = project_desc
        
        tasks = ET.SubElement(project, "tasks")
        return new_id
    
    def newTask(self, root:ET.ElementTree, task_name:str, task_due:str="00-00-00", task_desc:str="New task") -> str:
        # root is project or task so that we can determine the starting id
        tasks = root.find("tasks")
        if tasks is None:
            tasks = root.find("subtasks")
            if tasks is None:
                raise Exception("no tasks not subtasks were found")
        
        new_id = self.getNewID(root,"task")
        task = ET.SubElement(tasks, "task")
        task.set("id", new_id)
        task.set("name", task_name)
        
        # TODO validation of date format?
        due = ET.SubElement(task, "due_date")
        due.text = task_due
            
        desc = ET.SubElement(task, "desc")
        desc.text = task_desc
        
        status = ET.SubElement(task, "status")
        status.text = "0"
        status.set("last_change", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        subtasks = ET.SubElement(task, "subtasks")
        return new_id

    def getNewID(self, root:ET.Element, el_type:str) -> str:
        # look at the types that are on the same level
        # get the max id
        max_id = -1
        root_id = root.get("id")
        if root_id is None: 
            root_id = ""
        else: root_id += "."
        
        if el_type=="task":
            tasks = root.find("tasks") or root.find("subtasks")
            if tasks is not None:
                for task in tasks.findall("task"):
                    task_id = int(task.get("id").split(".")[-1])
                    max_id = max(max_id, task_id)
        else:
            projects = root.findall("project")
            
            for project in projects:
                p_id = int(project.get("id"))
                max_id = max(max_id,p_id)
                
        return root_id + str(max_id+1)
    
    def findElementTasks(self, root:ET.ElementTree, id:str) -> ET.Element:
        # TODO find usecase
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

    def findElement(self, id:str) -> ET.Element:
        # TODO redo into separate functions for tasks and projects
        element = self.root.find(f".//task[@id='{id}']")
        if element is None:
            element = self.root.find(f".//project[@id='{id}']")
            if element is None:
                raise ValueError(f"No task nor project was under id:{id}")
        return element
    
    def deleteElement(self, id:str):
        element = self.findElement(self.root,id)
        parent_id = self.getParentId(id)
        
        if parent_id is None:
            parent = self.root
        elif len(parent_id.split(".")) == 1: 
            parent = self.findElement(self.root,self.getParentId(id)).find("tasks")
        else:
            parent = self.findElement(self.root,self.getParentId(id)).find("subtasks")
            
        parent.remove(element)
        
    def getParentId(self, id:str):
        split_id = id.split(".")
        if len(split_id) == 1:
            return None
        else:
            return ".".join(split_id[0:-1])
        
    def updateStatus(self, task_id:str, status:str):
        # TODO
        pass