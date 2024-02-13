import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List

class TodoListRead:
    def __init__(self, xml_file:str):
        self.file:str = xml_file
        self.tree:ET.ElementTree = ET.parse(xml_file)
        self.root:ET.ElementTree = self.tree.getroot()

    def printTaskElem(self, task:ET.Element, print_subtasks:bool=False):
        """Method prints all the necessary information about a Task element

        Args:
            task (ET.Element): task to be printed
            print_subtasks (bool, optional): whether to also print subtasks, if yes, it only prints the id and name of the subtask. Defaults to False.
        """
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
        """Mathod priting a task based on the id of the task

        Args:
            task_id (str): id of the task
            subtasks (bool, optional): whether to also print subtasks. Defaults to False.
        """
        # TODO add checking that the task_id does not reference a project, raise ValueError
        task = self.root.find(f".//task[@id='{task_id}']")
        self.printTaskElem(task,subtasks)
    
    def printTaskList(self, task_list:List[ET.Element]):
        """Prints all the tasks in a list of tasks

        Args:
            task_list (List[ET.Element]): task list
        """
        for task in task_list:
            self.printTaskElem(task)
    
    def printAllTasks(self):
        """Prints all the tasks in a file
        """
        tasks = self.root.findall(".//task")
        for task in tasks:
            self.printTaskElem(task)
            print()
            
    def printProjectElem(self, project:ET.Element):
        """Prints all the necessary information about a Project element

        Args:
            project (ET.Element): project to be printed
        """
        id = project.get("id")
        name = project.findtext("name")
        desc = project.findtext("desc")
        
        print(f"Project@{id} {name}")
        print(f"Desription: \n  {desc}")

    def printReccursive(self, root:ET.ElementTree=None):
        """Reccursively prints all the tasks and projects based on the starting point - root

        Args:
            root (ET.ElementTree, optional): Optional speciication where to start the reccursive printing. Defaults to None - root of the file.
        """
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
                    
    def getTasksProjectID(self, project_id:str) -> List[ET.Element]:
        """Method that ouputs all the tasks under an id - for example a project id

        Args:
            project_id (str): id of element (project or task) from where to find all the tasks

        Returns:
            List[ET.Element]: list of the tasks
        """
        project = self.findElement(project_id)
        return project.findall(".//task")
    
    def getSortedTasks(self) -> List[ET.Element]:
        """Method that ouptus a list of all the tasks that are sorted based on the due date

        Returns:
            List[ET.Element]: sorted list of tasks
        """
        tasks = self.root.findall(".//task")
        tasks_dates = []
        
        for task in tasks:
            due_date = datetime.strptime(task.findtext("due_date"),"%Y-%m-%d %H:%M:%S")
            tasks_dates.append((task.get("id"),due_date))
        
        sorted_tasks_dates = sorted(tasks_dates, key=lambda x: x[1])
        sorted_tasks = [task for task,date in sorted_tasks_dates]
        return sorted_tasks
        
    def getSortedTasks(self, id:str) -> List[ET.Element]:
        """Method that output a list of tasks under a project or id (determined by the id) sorted based on the due date

        Args:
            id (str): starting element id

        Returns:
            List[ET.Element]: sorted list of tasks
        """
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
        """Method that finds either a task or project element specified by an id

        Args:
            id (str): id of a task or project

        Raises:
            ValueError: if no task or project was found under the id

        Returns:
            ET.Element: task or project correspoding to the id
        """
        # [ ] same function from todo_modify, check for identity
        element = self.root.find(f".//task[@id='{id}']")
        if element is None:
            element = self.root.find(f".//project[@id='{id}']")
            if element is None:
                raise ValueError(f"No task nor project was under id:{id}")
        return element
        