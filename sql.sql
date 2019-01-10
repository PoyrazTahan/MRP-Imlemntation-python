CREATE TABLE MRP_Data( "MRP_ID" integer primary key autoincrement, "Week" numeric, "Material_ID" numeric, "Gross_Req" numeric, "Schedule_recipt" numeric, "Proj_Balance" numeric, "Inventory_Level" numeric, "Net_Req" numeric, "Plan_Order" numeric, "Plan_Release" numeric, foreign key (Material_ID) references Material(Material_ID) )

Select Material_ID, Week, Gross_Req, Schedule_recipt, Proj_Balance, Inventory_Level, Net_Req, Plan_Release, Plan_Order
from MRP_Data
where week = 18;

Select Material_ID, Week, Gross_Req, Schedule_recipt, Proj_Balance, Inventory_Level, Net_Req, Plan_Release, Plan_Order
from MRP_Data
where Material_ID = 1;
