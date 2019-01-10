CREATE TABLE BOM("Part_ID" numeric , "SubPart_ID" numeric, "SubPart_Quantity" numeric, primary key (Part_ID, SubPart_Id) ,foreign key (Part_ID) references Material(Material_ID))
CREATE TABLE Cust_Order("Order_ID" numeric primary key,"Part_ID" numeric , "Demand" numeric, "Order_Week" numeric, foreign key (Part_ID) references Material (Material_ID))
CREATE TABLE Material ("Material_ID" numeric primary key, "Material_Name" text, "Material_Desc" text, "Lead_time" numeric, "Batch_Size" numeric)
CREATE TABLE `schedule_receipt` ( `sc_rec_id` INTEGER PRIMARY KEY AUTOINCREMENT, `material_id` INTEGER, `quantity` INTEGER, `week` INTEGER, FOREIGN key (material_id) REFERENCES Material (Material_ID) )
CREATE TABLE sqlite_sequence(name,seq)

CREATE TABLE MRP_Data( 
    "MRP_ID" integer primary key autoincrement, 
    "Week" numeric,
    "Material_ID" numeric, 
    "Gross_Req" numeric, 
    "Schedule_recipt" numeric,
    "Proj_Balance" numeric, 
    "Inventory_Level" numeric, 
    "Net_Req" numeric, 
    "Plan_Order" numeric, 
    "Plan_Release" numeric,  
    foreign key (Material_ID) references Material(Material_ID) )


select Material_ID, Week, Material_ID, Gross_Req, Schedule_recipt, Proj_Balance, inventory_Level, Net_Req, Plan_Release, Plan_Order
from MRP_Data
where Material_ID = 1;

select Material_ID, Week, Material_ID, Gross_Req, Schedule_recipt, Proj_Balance, inventory_Level, Net_Req, Plan_Release, Plan_Order
from MRP_Data
where Week = 18;