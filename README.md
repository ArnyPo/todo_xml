# Todo_xml
XML based TODO list organiser written in Python.

Contains methods to add new proejects and tasks, to modify them and then to read and parse them.

A GUI is in the works.

## XML templates for tasks and projects
The overall schema of the projects and tasks. The main identifier of each part is the id, that is then nested. All project have one `int` number. The nested tasks add dot `.` and under `int` number (1.0.3). Tasks can be nested either in `subtasks` of `task` or in `tasks` of `project`


**Tasks**
```xml
<task id="0" name="">
    <due_date></due_date>
    <desc></desc>
    <status last_change="2024-01-01 00:00:00">0|1|2</status> 
    <subtasks></subtasks>
</task>
```
Tasks have a due date in the ISO format (the same format is used un status). A description is just a string. Status tracks changes and right now the thinking is that 0 indicates Not started, 1 In progress and 2 Done. Subtasks can have more tasks in them.

**Projects**
```xml
<project id="0">
    <name></name>
    <des></desc>
    <tasks></tasks>
</project>
```
Projects are identified by an id. Name and descriptions can be any string. Tasks have the tasks in them, though, none by default. 