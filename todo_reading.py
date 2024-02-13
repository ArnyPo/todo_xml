import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List

class TodoListRead:
    def __init__(self, xml_file:str):
        self.file:str = xml_file
        self.tree:ET.ElementTree = ET.parse(xml_file)
        self.root:ET.ElementTree = self.tree.getroot()

    def printTaskElem(self, task:ET.Element, print_subtasks:bool=False):
        task_id = task.get("id")
        name = task.get("name")
        desc = task.findtext("desc")
        date = task.findtext("due_date")
        status = task.find("status") # TODO convert num into words, possible user-deifinition
        status_change = status.get("last_change")
        
        print(f"Task@{task_id} {name}")
        print(f"Due: {date}")
        print(f"Status: {status.text} - last changed {status_change}")
        print(f"Desription: \n  {desc}")
        
        if print_subtasks: 
            subtasks = task.findall("subtasks/task")
        else: subtasks = None
        if subtasks is not None:
            print("Subtasks:")
            for task in subtasks:
                st_id = task.attrib.get("id")
                st_name = task.attrib.get("name")
                print(f"ID: {st_id} Name: {st_name}")
                
    def printTaskID(self, task_id:str, subtasks:bool=False):
        task = self.root.find(f".//task[@id='{task_id}']")
        self.printTaskElem(task,subtasks)
    
    def printTaskList(self, task_list:List[ET.Element]):
        for task in task_list:
            self.printTaskElem(task)
    
    def printAllTasks(self):
        tasks = self.root.findall(".//task")
        for task in tasks:
            self.printTaskElem(task)
            print()
            
    def printProjectElem(self, project:ET.Element):
        id = project.get("id")
        name = project.findtext("name")
        desc = project.findtext("desc")
        
        print(f"Project@{id} {name}")
        print(f"Desription: \n  {desc}")

    def printReccursive(self, root:ET.ElementTree=None):
        if root is None:
            root = self.root
            projects = root.findall(".//project")
            for project in projects:
                self.printProjectElem(project)
                self.printReccursive(project.find("tasks"))
        else:
            tasks = root.findall("task")
            if tasks is not None:
                for task in tasks:
                    self.printTaskElem(task)
                    self.printReccursive(task.find("subtasks"))
                    
    def getTasksProjectID(self, project_id:str):
        project = self.findElement(project_id)
        return project.findall(".//task")
    
    def getSortedTasks(self) -> List[ET.Element]:
        tasks = self.root.findall(".//task")
        tasks_dates = []
        
        for task in tasks:
            due_date = datetime.strptime(task.findtext("due_date"),"%Y-%m-%d %H:%M:%S")
            tasks_dates.append((task.get("id"),due_date))
        
        sorted_tasks_dates = sorted(tasks_dates, key=lambda x: x[1])
        sorted_tasks = [task for task,date in sorted_tasks_dates]
        return sorted_tasks
        
    def getSortedTasks(self, id:str) -> List[ET.Element]:
        # TODO merge with the function without id
        root = self.findElement(id)
        tasks = root.findall(".//task")
        tasks_dates = []
        
        for task in tasks:
            due_date = datetime.strptime(task.findtext("due_date"),"%Y-%m-%d %H:%M:%S")
            tasks_dates.append((task.get("id"),due_date))
        
        sorted_tasks_dates = sorted(tasks_dates, key=lambda x: x[1])
        sorted_tasks = [task for task,date in sorted_tasks_dates]
        return sorted_tasks
        
    def findElement(self, id:str) -> ET.Element:
        # TODO same function from todo_modify, check for identity
        element = self.root.find(f".//task[@id='{id}']")
        if element is None:
            element = self.root.find(f".//project[@id='{id}']")
            if element is None:
                raise ValueError(f"No task nor project was under id:{id}")
        return element
        