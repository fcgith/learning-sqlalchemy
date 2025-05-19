from datetime import datetime

from sqlalchemy import event, exc
from sqlalchemy.orm import Session

from app.models.order import OrderProduct, OrderStatus, Order
from app.models.product import Product
from app.models.sales import Sales, ItemSales

"""
    Stock update on order submission and status change
"""


def store_original_status(mapper, connection, target):
    target._original_status = target.status


def verify_product_stock_availability_and_update(mapper, connection, target):
    # Catch and update product stock on
    session = Session(connection)
    product = session.query(Product).filter(Product.id == target.product_id).first()

    if not product:
        raise exc.SQLAlchemyError(f"Product {target.product_id} not found")
    if product.stock < target.quantity:
        raise exc.SQLAlchemyError(f"Insufficient stock for product {target.name} (#{target.product_id})")

    product.stock -= target.quantity
    session.commit()


event.listen(OrderProduct, "before_insert", verify_product_stock_availability_and_update)
event.listen(OrderProduct, "before_update", verify_product_stock_availability_and_update)


def restore_stock_on_order_cancellation(mapper, connection, target):
    # Restore stock if the order is canceled before paid

    if (target.status == OrderStatus.CANCELLED.value
            and hasattr(target, '_original_status')
            and target._original_status != OrderStatus.CANCELLED.value):
        session = Session(connection)

        for op in target.order_products:
            product = session.query(Product).filter(Product.id == op.product_id).first()
            if product:
                product.stock += op.quantity

        session.commit()


event.listen(Order, "before_update", store_original_status)
event.listen(Order, "after_update", restore_stock_on_order_cancellation)

"""
    Sales logging
"""


def log_sale_on_order_status_change(mapper, connection, target):
    # Catch and log order and items sold

    if (target.status != OrderStatus.PENDING.value
            and hasattr(target, '_original_status')
            and target._original_status == OrderStatus.PENDING.value):
        session = Session(connection)

        sale = Sales(order_id=target.id,
                     user_id=target.user_id,
                     status=target.status,
                     total_price=target.total_price or 0.0,
                     date=datetime.now())

        for op in target.order_products:
            item_sale = ItemSales(product_id=op.product_id,
                                  quantity=op.quantity,
                                  unit_price=op.total_price / op.quantity if op.quantity > 0 else 0,
                                  total_price=op.total_price)
            sale.item_sales.append(item_sale)

        session.add(sale)
        session.commit()


event.listen(Order, "before_update", store_original_status)
event.listen(Order, "after_update", log_sale_on_order_status_change)
