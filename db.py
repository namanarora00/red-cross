from meta import Table


item = Table("item")
beneficiery = Table("beneficiery")
distribution = Table("distribution")
distributed = Table("distributed")

item.init_table(["id", "name", "type", "quantity"])
# items are stored as as string of comma separated values in both tables
# example --> items = "bucket,clothes,food"

distribution.init_table(["id", "items", "timestamp"])
distributed.init_table(["bid", "item", "id", "timestamp", "quantity"])
