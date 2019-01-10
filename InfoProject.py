from dataBase import DataBase as DB
import math
import pdb
from table import Table


class App():
    def __init__(self,db_file):
        self.db = DB(db_file) 
        self.Material_Map = None
        
        query1 = "SELECT * FROM Cust_Order ORDER BY Order_Week ASC"  
        query2 = "SELECT * FROM schedule_receipt"  

        self.Order_Table = self.db.run_select_query(query1) 
        self.last_order = self.Order_Table[-1][-1]
        self.Schedule_Receipt_Table = self.db.run_select_query(query2)

    def start(self):
        self.set_bom()

        self.initialize_table(self.last_order)

        for i, order in enumerate(self.Order_Table):
            self.calculate_MRP(order, i)
        
        keys = self.Material_Map.keys()
        
        
        for key in keys:
            self.recordMRP(self.Material_Map[str(key)])
        

    def recordMRP(self, table):
        #query_deletion = """Delete from  'MRP_Data' """

        #self.db.run_select_query(query_deletion)

        query = """insert Into MRP_Data (Week, Material_ID, Gross_Req, Schedule_recipt, Proj_Balance,\
            Net_Req, Plan_Order, Plan_Release, Inventory_Level) values """
        rng = len(table.demand)
        tmp = []
        for i in range(1,rng):
            tmp_str = """( %s, %s, %s, %s, %s, %s, %s, %s, %s) """ % (i , table.id, table.demand[i], table.scheduled_rec[i], table.proj_balance[i], table.net_req[i], table.release[i], table.planned_rec[i], table.inventory[i])
            tmp.append(tmp_str)
        
        query = query + ',\n'.join(tmp)

        self.db.run_insert_query(query)


    def set_bom(self):
        query = "SELECT * FROM BOM"
        query2 = "SELECT * FROM Material"  
        BOM_Table = self.db.run_select_query(query)
        Material_Table = self.db.run_select_query(query2)
        
        table_map = {}
        for i, row in enumerate(Material_Table):
            m_id, m_name, _, m_lead, m_batch = row
            table_map[str(m_id)] = Table(m_id, m_name, m_lead, m_batch)
            if i == 0:
                table_map[str(m_id)].isRoot = True

        
        keys = table_map.keys()
        for table_id in keys:
            for j, BOMrow in enumerate(BOM_Table):
                if int(table_id) == BOMrow[0]:
                    piece_id = BOMrow[1]
                    piece = table_map[str(piece_id)]
                    subpart_quantity = BOMrow[2]

                    piece.ingredientOf.append(table_map[table_id])
                    table_map[table_id].children.append((piece, subpart_quantity))
        self.Material_Map = table_map

    def calculate_MRP(self, order, counter):
        _ ,ordered_partID, demand, delivery_week = order
        ordered_material = self.Material_Map[str(ordered_partID)]
        
        start_week = 0
        end_week = delivery_week + 1
        if counter == 0: 
            start_week = 1
        else:
            start_week = self.Order_Table[counter - 1][-1]
        self.inv_check(start_week+1, end_week,ordered_material)
        net_req = max(0,demand - ordered_material.scheduled_rec[delivery_week] - ordered_material.inventory[delivery_week] + ordered_material.proj_balance[delivery_week])
        planned_rec = ordered_material.batch_size * (math.ceil(net_req / ordered_material.batch_size))

        ordered_material.demand[delivery_week] += demand
        ordered_material.net_req[delivery_week] += net_req
        
        if net_req >0:
            deadline = delivery_week - ordered_material.lead_time
            if net_req >0 and deadline < 1:
                print("[Warning!] Deadline week is a negative value. It cannot be calculated.")
                exit(1) 
            ordered_material.planned_rec[delivery_week] += planned_rec
            ordered_material.inventory[delivery_week+1] += planned_rec - net_req
            ordered_material.release[deadline] += planned_rec
            if deadline >0:
                self.calculate_for_pieces(ordered_material, deadline, 0)
            

    def calculate_for_pieces(self, ingredientOfTable, deadline_from_ingredientOf, counter):
        amount_of_children = len(ingredientOfTable.children) 
        
        if amount_of_children == 0:
            return

        for tpl in ingredientOfTable.children:
            piece, quantity = tpl
            deadline_for_piece = deadline_from_ingredientOf - piece.lead_time

            start_week = 1
            end_week = deadline_from_ingredientOf + 1
            
            for i, value in reversed(list(enumerate(piece.demand))):
                if value != 0:
                    start_week = i + 1
                    break
        
            self.inv_check(start_week, end_week, piece)

            demand = ingredientOfTable.release[deadline_from_ingredientOf] * quantity
            net_req = demand - piece.scheduled_rec[deadline_from_ingredientOf] + piece.proj_balance[deadline_from_ingredientOf] - piece.inventory[deadline_from_ingredientOf]

            planned_rec = piece.batch_size * (math.ceil(net_req / piece.batch_size))

            if net_req >0 and deadline_for_piece < 1:
                print("[Warning!] Deadline week is a negative value. It cannot be calculated.")
                exit(1)

            piece.demand[deadline_from_ingredientOf] += demand
            piece.net_req[deadline_from_ingredientOf] += net_req
            piece.planned_rec[deadline_from_ingredientOf] += planned_rec
            piece.release[deadline_for_piece] += planned_rec
            piece.inventory[deadline_from_ingredientOf+1] += planned_rec - net_req 

            self.calculate_for_pieces(piece, deadline_for_piece, 0)


    def initialize_table(self, rng):
        keys = self.Material_Map.keys()
        mrp_period = len(self.Material_Map['1'].demand)
        tmp = None
        flag = False
        if  mrp_period == 0:
            tmp = [0 for j in range(rng+2)]
            flag = True
        else:
            additionZeros = rng+2-mrp_period
            tmp = [0 for j in range(additionZeros)]
        for i in keys:
            self.Material_Map[i].demand.extend(tmp)
            self.Material_Map[i].scheduled_rec.extend(tmp)
            self.Material_Map[i].proj_balance.extend(tmp)
            self.Material_Map[i].net_req.extend(tmp)
            self.Material_Map[i].planned_rec.extend(tmp)
            self.Material_Map[i].release.extend(tmp)
            
            self.Material_Map[i].inventory.extend(tmp)
        
        if flag:
            self.set_scheduledRec_values_for_mrp_table()

    def inv_check(self, start_week, end_week, Table):
        for i in range(start_week,end_week):
            if (Table.demand[i-1] - Table.scheduled_rec[i-1] - Table.inventory[i-1] + Table.proj_balance[i-1]) < 0:
                Table.inventory[i] += -1 * (Table.demand[i-1] - Table.scheduled_rec[i-1] - Table.inventory[i-1] + Table.proj_balance[i-1])

    def get_total_lead_time(self, Table):
        total_lt = Table.lead_time
        while len(Table.ingredientOf) != 0:
            Table = Table.ingredientOf[0]
            total_lt += Table.lead_time
        return total_lt


    def set_scheduledRec_values_for_mrp_table(self):
        for row in self.Schedule_Receipt_Table:
            _, material_id, quantity, weekIndex = row
            self.Material_Map[str(material_id)].scheduled_rec[weekIndex-1] = quantity






