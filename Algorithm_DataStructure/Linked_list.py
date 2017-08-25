# Python built-in datastructure doesn't contain linked list

# We can use Class to build one! It should include two major things:

# 1. Data Type

class Element(object):
    def __init__(self,value):
        self.value = value
        self.next = None

# 2. Storage Structure
class LinkedList(object):
    def __init__(self,head=None):
        self.head = head

    def append(self,new_element):
        current = self.head
        if self.head:
            while current.next:
                current = current.next
            current.next = new_element
        else:
            self.head = new_element
    def insert_first(self,new_element):
        "Insert new element as the head of the LinkedList"
        current = self.head
        if self.head:
            self.head = new_element
            new_element.next = current
        else:
            self.head = new_element

    def delete_first(self):
        "Delete the first element in the LinkedList"
        current = self.head
        if self.head:
            self.head = self.head.next
            return current
        else:
            return None


    def get_position(self,position):
        pointer = self.head
        if position:
            if position == 1:
                return self.head
            else:
                while (position > 1) :
                    pointer = pointer.next
                    position -= 1
                return pointer
        else:
            return None

    def insert(self,new_element,position):
        if position == 1:
            new_element.next = self.head
            self.head = new_element
        elif position:
            insert_address = self.get_position(position - 1)
            next_address = self.get_position(position)
            insert_address.next = new_element
            new_element.next = next_address

    def delete(self, value):
        """Delete the first node with a given value."""
        pointer = self.head
        last_pointer_store = None
        while pointer.value != value and pointer.next:
            last_pointer_store = pointer
            pointer = pointer.next
        if pointer == self.head:
            self.head = self.head.next
        else:
            last_pointer_store.next = pointer.next

# Use linke_list to realize "stack"
class Stack(object):
    def __init__(self,top = None):
        self.l1 = LinkedList(top)
    def push(self,new_element):
        self.l1.insert_first(new_element)

    def pop(self):
        # remove the first element off the top of the stack and
        # return it!
        pop_obj = self.l1.delete_first()
        return pop_obj



e1 = Element(1)
e2 = Element(2)
e3 = Element(3)
e4 = Element(4)

l1 = LinkedList(e1)
l1.append(e2)
l1.append(e3)
#print l1.head.next.next.value
#print l1.get_position(3).value
l1.insert(e4,3)
#print l1.get_position(3).value
l1.delete(1)
#print l1.get_position(1).value
#print l1.get_position(2).value
#print l1.get_position(3).value
stack = Stack(e1)
stack.push(e2)
stack.push(e3)
print stack.pop().value
print stack.pop().value
print stack.pop().value
print stack.pop()
stack.push(e4)
print stack.pop().value

