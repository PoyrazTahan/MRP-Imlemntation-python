class Table:
    def __init__(self, id, name, lead_time, batch_size):
        self.id = id
        self.name = name
        self.lead_time = lead_time
        self.batch_size = batch_size

        self.demand = []
        self.scheduled_rec = []
        self.proj_balance = []
        self.net_req = []
        self.planned_rec = []
        self.release = []
        self.inventory = []

        self.isRoot = False
        self.children = []
        self.ingredientOf = []

    def toString(self):
        print("\nID:", self.id, " Name:", self.name, " LeadTime:", self.lead_time, " Batch:", self.batch_size, "ROOT: ",
              self.isRoot, end= ' ### ')
        print ("Children id: ", end='')
        for i in self.children:
            print ("(", i[0].id, i[1], ")", end=' ')
            if len(self.parent) != 0:
                print ("  Parent id: ", end='')
                for i in self.parent:
                    print(i.id, end=' ')
                    print("hello")

