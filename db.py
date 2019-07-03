from meta import Table

TABLES = []


item = Table("item")
beneficiery = Table("beneficiery")
distribution = Table("distribution")
distributed = Table("distributed")
admin = Table("admin")


item.init_table(["id", "name", "type", "quantity"])
# items are stored as as string of comma separated values in both tables
# example --> items = "bucket,clothes,food"

distribution.init_table(["id", "items", "timestamp"])
distributed.init_table(["bid", "item", "id", "timestamp", "quantity"])
admin.init_table(["id"])


TABLES.append(beneficiery)
TABLES.append(item)
TABLES.append(distributed)
TABLES.append(distribution)
TABLES.append(admin)
