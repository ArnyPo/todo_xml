import xml.etree.ElementTree as ET
from datetime import datetime

class TodoListModify:
    def __init__(self, xml_file:str):
        self.file:str = xml_file
        self.tree:ET.ElementTree = ET.parse(xml_file)
        self.root:ET.ElementTree = self.tree.getroot()
    
    def writeToFile(self):
        """CLosing method that writes all the changes done to the XML tree to the file
        """
        ET.indent(self.tree, space="\t")
        self.tree.write(self.file)
        
    def newProject(self, project_name:str, project_desc:str="New project") -> str:
        """Method creating a new Projcet element in the root

        Args:
            project_name (str): name of the project
            project_desc (str, optional): project description. Defaults to "New project".

        Returns:
            str: id of the new project
        """
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
        """Method creating a new Task element in the specified position

        Args:
            root (ET.ElementTree): specification of the placement of the new task - project or task element
            task_name (str): name of the task
            task_due (str, optional): due date of the task in ISO format - YYYY-MM-DD hh:mm:ss. Defaults to "00-00-00".
            task_desc (str, optional): description of the task. Defaults to "New task".

        Raises:
            Exception: if no tasks or subtasks elements were found under root

        Returns:
            str: id of the new task
        """
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
        """Method analysing the current layer of XML and determinig the new id that can be 
        assigned to a new element. It finds the maximum of the existing ids and adds one

        Args:
            root (ET.Element): placement of the new element
            el_type (str): element type - determines formating of the new id

        Returns:
            str: new id
        """
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
        """Method that finds the element (task or project) based on its id

        Args:
            id (str): id of the element to be found

        Raises:
            ValueError: if no element was found under the id

        Returns:
            ET.Element: found element
        """
        # TODO redo into separate functions for tasks and projects
        element = self.root.find(f".//task[@id='{id}']")
        if element is None:
            element = self.root.find(f".//project[@id='{id}']")
            if element is None:
                raise ValueError(f"No task nor project was under id:{id}")
        return element
    
    def deleteElement(self, element:ET.Element):
        """Method that removes an element

        Args:
            element (ET.Element): element to be removed
        """
        parent_id = self.getParentId(element.get("id"))
        
        if parent_id is None:
            parent = self.root
        elif len(parent_id.split(".")) == 1: 
            parent = self.findElement(self.root,self.getParentId(id)).find("tasks")
        else:
            parent = self.findElement(self.root,self.getParentId(id)).find("subtasks")
            
        parent.remove(element)
        
    def getParentId(self, id:str) -> str:
        """Method that analyses the id and returns the id of the parent. This means that it only 
        removes the last number alongside with the dot - 1.4.2 -> 1.4. When there is only one number
        it return None indicating that the root is the parent.

        Args:
            id (str): id of the element

        Returns:
            str: id of the parent, or None when root
        """
        split_id = id.split(".")
        if len(split_id) == 1:
            return None
        else:
            return ".".join(split_id[0:-1])
        
    def updateStatus(self, task_id:str, new_status:str):
        """Updates the status based on the id of the task. It also modifies the "last change" 
        attribute of the task to the current time.

        Args:
            task_id (str): id of the task
            new_status (str): new status - 0|1|2
        """
        task = self.findElement(task_id)
        
        status = task.find("status")
        status.text = new_status
        status.set("last_change", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def modifyTask(self, task:ET.Element, element:str, value:str):
        """Modifies task element - either the due date of the description based on the input.

        Args:
            task (ET.Element): task to modify
            element (str): element of the task to modify - due_date, desc
            value (str): value to update the element with

        Raises:
            ValueError: _description_
        """
        # TODO date check
        to_modify = task.find(element)
        if to_modify is None:
            raise ValueError(f"Element {element} not found in task")
        to_modify.text = value
        