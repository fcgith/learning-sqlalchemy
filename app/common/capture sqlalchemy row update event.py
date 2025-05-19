# from datetime import datetime
#
# from sqlalchemy import event, exc
# from sqlalchemy.orm import Session
#
#
# # Their function is used before row update to store data for after the update
# def store_original_status(mapper, connection, target):
#     target._original_status = target.status
#
#
# def database_event_catcher(mapper, connection, target):
#     # Restore stock if the order is canceled before paid
#     pass
#     # target - the object/db row bein updated
#     # connection - the database connection
#     # mapper - the mapper that mapped the object to the row
#
# # These two call the functions before row update and then another after row update
# #event.listen(Order, "before_update", store_original_status)
# #event.listen(Order, "after_update", database_event_catcher)
#
# print("Event services initialized")