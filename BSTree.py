from TreeNode import *

all_letters = "abcdefghijklmnopqrstuvwxyz"

letter_to_num = {}
num_to_letter = []

for index in range(len(all_letters)):
    letter_to_num[all_letters[index]] = index
    num_to_letter.append(all_letters[index])


def getDirection(node: TreeNode, goal_key):
    current_Key = node.key

    length_goal_key = len(goal_key) - 1

    for index in range(len(current_Key)):
        if index > length_goal_key:
            return node.leftPointer, False

        if letter_to_num[current_Key[index]] > letter_to_num[goal_key[index]]:
            return node.leftPointer, False
        
        elif letter_to_num[current_Key[index]] < letter_to_num[goal_key[index]]:
            return node.rightPointer, True
        
    return node.rightPointer, True # true for right, false for left
        


# traverse order <left><root><right>

class BSTree:
    def __init__(self):
        self.root = None


    def insert(self, key, data, lvl):
        if self.root == None:
            self.root = TreeNode(key)
            self.root.add_data(data, lvl)

        else:
            self._insert(self.root, key, data, lvl)

    def _insert(self, node: TreeNode, key, data, lvl):
        nextNode, Direction = getDirection(node, key)

        if nextNode == None:
            newNode = TreeNode(key)
            newNode.add_data(data, lvl)
            
            if Direction == True:
                node.rightPointer = newNode
            else:
                node.leftPointer = newNode

            return True

        elif nextNode.key == key:
            nextNode.add_data(data, lvl)
            return True
            
        else:
            return self._insert(nextNode, key, data, lvl)


    def search(self, key) -> TreeNode | None:
        return self._search(self.root, key)
    
    def _search(self, node: TreeNode, key) -> TreeNode | None:

        nextNode, _ = getDirection(node, key)

        if nextNode == None:
            return None

        elif nextNode.key == key:
            return nextNode
            
        else:
            return self._search(nextNode, key)
            
    
    def inorder_traversal(self):
        return self._inorder_traversal(self.root, 0)
    
    def _inorder_traversal(self, node: TreeNode, count):
        
        if node.leftPointer:
            count = self._inorder_traversal(node.leftPointer, count)
            

        print(f"[{node.key}] = {node.data};")
        count += 1

        if node.rightPointer:
            count = self._inorder_traversal(node.rightPointer, count)
            
        return count