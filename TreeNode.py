class TreeNode:
    def __init__(self, key):
        self.key = key
        self.data = {} # (url: priority points)
        self.sorted = []
        self.isSorted = False
        self.leftPointer = None
        self.rightPointer = None

    def add_data(self, data, level): # levels here: 0, 1
        self.isSorted = False
        if not data in self.data:
            self.data[data] = 2 - level

        else:
            self.data[data] += 2 - level

    def get_sorted(self):
        if self.isSorted == True:
            return self.sorted
        
        self.sorted = [(url, prior) for url, prior in self.data.items()]
        self.sorted.sort(key = lambda data_tuple: -data_tuple[1])

        self.isSorted = True

        return self.sorted
    

    def __str__(self):
        string = "\n"
        for url, priority in self.get_sorted():
            string += f"{url} (Importance: {priority})\n"
            
        return string

