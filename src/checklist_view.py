"""
考えろ、バカ：
    - Checklists will have a tree structure.
        - The parent nodes are checklists.
        - Leaf nodes are checklist items.
        - If a parent task's status is changed to completed, all of its children will be changed as well.
        - If all of a parent task's children tasks are completed, it will also be automatically completed.
        - If one of a completed parent task's child tasks is un-completed, the parent task will be as well.

    - Until it's discussed more, I'll treat the schedule variable as the number of days until which you want the list
      to reset.

    CURRENT SETBACKS:
        - There might be unfortunate times whenever you accidentally complete a parent task, subsequently completing
          all of the subtasks. In which case, it might be impossible to auto 'un-complete' the subtasks.
"""


class ChecklistItem:
    def __init__(self, task=None, schedule=None):
        self.task = task
        self.parent = None
        self.children = []
        self.completed = False
        self.schedule = schedule

    def add_child(self, sub_task):
        sub_task.set_parent(self)
        self.children.append(sub_task)

    def mark_task(self):
        self.completed = True

        for item in self.get_children():
            item.mark_task()

    def unmark_task(self):
        self.completed = False

    def set_parent(self, parent):
        self.parent = parent

    def get_task(self):
        return self.task

    def get_completion(self):
        return self.completed

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def get_schedule(self):
        return self.schedule


def print_checklist(root):
    for item in root.children:
        if root.parent is None:
            print(root.get_task())

        temp = root
        while temp.get_parent() is not None:
            temp = temp.get_parent()
            print("    ", end="")

        if item.get_completion():
            print("x " + item.get_task())
        else:
            print("o " + item.get_task())

        print_checklist(item)


if __name__ == "__main__":
    test_checklist = ChecklistItem("Backpack Checklist")

    """
    As a proof of concept, I'll make a checklist similar to the following, x is complete, o is incomplete:
    Backpack Checklist
    o back pocket
        o laptop
        x げんき
            x げんき workbook 
    o front pocket
        o pens
        o headphones
    """
    test_checklist.add_child(ChecklistItem("back pocket"))
    test_checklist.add_child(ChecklistItem("front pocket"))

    sub_checklist = test_checklist.children[0]
    sub_checklist.add_child(ChecklistItem("laptop"))
    sub_checklist.add_child(ChecklistItem("げんき"))

    sub_checklist = sub_checklist.children[1]
    sub_checklist.add_child(ChecklistItem("げんき workbook"))

    sub_checklist = test_checklist.children[1]
    sub_checklist.add_child(ChecklistItem("pens"))
    sub_checklist.add_child(ChecklistItem("headphones"))

    sub_checklist = test_checklist.children[0].children[1]
    sub_checklist.mark_task()

    print_checklist(test_checklist)
