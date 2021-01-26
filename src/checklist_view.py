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
    def __init__(self, task=None):
        self.task = task
        self.parent = None
        self.children = []
        self.completed = False

    def add_child(self, sub_task):
        sub_task.set_parent(self)
        self.children.append(sub_task)

    def mark_task(self):
        self.completed = True

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


class Checklist:
    def __init__(self, schedule=0):
        self.root = ChecklistItem()
        self.schedule = schedule


def print_checklist(root):
    for item in root.children:

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
    test_checklist = Checklist()

    """
    As a proof of concept, I'll make a checklist similar to the following, x is complete, o is incomplete:
    Backpack Checklist
    o back pocket
        x laptop
        o げんき third edition Japanese textbook and workbook with bonus learning exercises
    o front pocket
        o pens
        o headphones
    """

    test_checklist.root.add_child(ChecklistItem("back pocket"))
    test_checklist.root.children[0].add_child(ChecklistItem("laptop"))
    test_checklist.root.children[0].children[0].mark_task()
    test_checklist.root.children[0].add_child(ChecklistItem("げんき third edition Japanese textbook and workbook with "
                                                            "bonus learning exercises"))
    test_checklist.root.add_child(ChecklistItem("front pocket"))
    test_checklist.root.children[1].add_child(ChecklistItem("pens"))
    test_checklist.root.children[1].add_child(ChecklistItem("headphones"))

    print_checklist(test_checklist.root)
