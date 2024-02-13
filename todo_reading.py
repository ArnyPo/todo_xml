import xml.etree.ElementTree as ET

class TodoListRead:
    def __init__(self, xml_file:str):
        self.file:str = xml_file
        self.tree:ET.ElementTree = ET.parse(xml_file)
        self.root:ET.ElementTree = self.tree.getroot()
    
    def getTasksTimeSorted(self, root:ET.ElementTree):
        pass

    def printTaskElem(self, task:ET.Element, subtasks:bool=False):
        # TODO make a recursive method
        task_id = task.get("id")
        name = task.get("name")
        desc = task.find("desc")
        date = task.find("due_date")
        status = task.find("status")
        status_change = status.get("last_change")
        
        print(f"Task@{task_id} {name}")
        print(f"Due: {date}")
        print(f"Status: {status} - last changed {status_change}")
        print(f"Desription: \n  {desc}")
        
        if subtasks: subtasks = task.findall("subtasks/task")
        if subtasks is not None:
            print("Subtasks:")
            for task in subtasks:
                st_id = task.attrib.get("id")
                st_name = task.attrib.get("name")
                print(f"ID: {st_id} Name: {st_name}")
                
    def printTaskID(self, task_id:str, subtasks:bool=False):
        task = self.root.find(f".//task[@id='{task_id}']")
        self.printTaskElem(task,subtasks)
    
    def printTasks(self,parent_id:str):
        pass
    
    def printAllTasks(self):
        tasks = self.root.findall(".//task")
        for task in tasks:
            self.printTask(task)
        
        