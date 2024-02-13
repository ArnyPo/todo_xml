from todo_modify import TodoListModify as TM
from todo_reading import TodoListRead as TR

FILE = "test.xml"

tm = TM(FILE)
# id1 = tm.newProject("BC", "Bachelor thesis")
# id2 = tm.newTask(tm.findElement(id1),"Read papers","2024-02-02")
# id3 = tm.newTask(tm.findElement(id1),"Write introuction","2024-02-07")
# id21 = tm.newTask(tm.findElement(id2),"Leehman et al. 2023")
# tm.writeToFile()

tr = TR(FILE)
tr.printTaskID("0.0",True)