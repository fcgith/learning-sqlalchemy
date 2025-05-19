from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import OrderCreate, Order, OrderProduct, OrderUpdate, OrderStatus, OrderProductCreate
from app.models.product import Product
from app.models.user import User


def get_order_by_id(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def check_order_user(db: Session, order_id: int, user: User) -> Order:
    order = get_order_by_id(db, order_id)
    if order.user_id != user.id and not user.admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return order


def check_order_product(db: Session, order_id: int, order_product_id: int, user: User) -> OrderProduct:
    order = check_order_user(db, order_id, user)
    order_product = db.query(OrderProduct).filter(
        OrderProduct.order_id == order_id,
        OrderProduct.id == order_product_id
    ).first()
    if not order_product:
        raise HTTPException(status_code=404, detail="Order product not found")
    return order_product


def check_product(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def update_order_price(db: Session, order: Order, product, quantity: int, add: bool = False):
    if isinstance(product, int):
        product = check_product(db, product)
    cost = product.price * quantity
    if product.discount:
        cost -= (product.discount.percentage / 100) * cost

    if not add:
        order_product = db.query(OrderProduct).filter(
            OrderProduct.order_id == order.id,
            OrderProduct.product_id == product.id
        ).first()
        if not order_product:
            raise HTTPException(status_code=404, detail="Order product not found")
    else:
        order_product = OrderProduct(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            total_price=cost
        )

    if not add:
        order.total_price -= order_product.total_price
    order_product.quantity = quantity
    order_product.total_price = cost
    order.order_products.append(order_product)
    order.total_price += cost

    db.commit()
    db.refresh(order)
    return order


def create_order(db: Session, user_id: int, order: OrderCreate):
    total_cost = 0
    order_products = []

    for op in order.order_products:
        product = db.query(Product).filter(Product.id == op.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {op.product_id} not found")

        cost = product.price * op.quantity
        if product.discount:
            cost -= (product.discount.percentage / 100) * cost

        total_cost += cost
        order_products.append(OrderProduct(
            product_id=op.product_id,
            quantity=op.quantity,
            total_price=cost
        ))

    db_order = Order(user_id=user_id, total_price=total_cost)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for op in order_products:
        op.order_id = db_order.id
        db.add(op)
    db.commit()
    db.refresh(db_order)

    return db_order


def update_order(db: Session, order_id: int, order_update: OrderUpdate, user: User):
    order = check_order_user(db, order_id, user)

    if order.status > OrderStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Order is already paid and cannot be modified")

    for product_id in order_update.remove_products:
        order_product = db.query(OrderProduct).filter(
            OrderProduct.order_id == order_id,
            OrderProduct.product_id == product_id
        ).first()
        if order_product:
            order.total_price -= order_product.total_price
            db.delete(order_product)

    for op in order_update.new_products:
        product = check_product(db, op.product_id)
        cost = product.price * op.quantity
        if product.discount:
            cost -= (product.discount.percentage / 100) * cost

        order_product = db.query(OrderProduct).filter(
            OrderProduct.order_id == order.id,
            OrderProduct.product_id == op.product_id
        ).first()
        if order_product:
            order.total_price -= order_product.total_price
            order_product.quantity = op.quantity
        else:
            order_product = OrderProduct(
                order_id=order.id,
                product_id=op.product_id,
                quantity=op.quantity,
                total_price=cost
            )
            db.add(order_product)

        order_product.total_price = cost
        order.total_price += cost

    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int, user: User):
    order = check_order_user(db, order_id, user)
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}


def get_order_products(db: Session, order_id: int, user: User):
    order = check_order_user(db, order_id, user)
    return order.order_products


def add_order_product(db: Session, order_id: int, opc: OrderProductCreate, user: User):
    order = check_order_user(db, order_id, user)
    product = check_product(db, opc.product_id)

    cost = product.price * opc.quantity
    if product.discount:
        cost -= (product.discount.percentage / 100) * cost

    order_product = db.query(OrderProduct).filter(
        OrderProduct.order_id == order_id,
        OrderProduct.product_id == opc.product_id
    ).first()
    if not order_product:
        order_product = OrderProduct(
            order_id=order_id,
            product_id=opc.product_id,
            quantity=opc.quantity,
            total_price=cost
        )
        db.add(order_product)
    else:
        order_product.quantity += opc.quantity
        order_product.total_price += cost

    order.total_price += cost
    db.commit()
    db.refresh(order)
    return order_product


def update_order_product(db: Session, order_id: int, order_product_id: int, quantity: int, user: User):
    order_product = check_order_product(db, order_id, order_product_id, user)
    order = update_order_price(db, order_product.order, order_product.product, quantity)
    order_product.quantity = quantity
    order_product.total_price = order_product.product.price * quantity
    if order_product.product.discount:
        order_product.total_price -= (order_product.product.discount.percentage / 100) * order_product.total_price
    db.commit()
    db.refresh(order_product)
    return order_product


def remove_order_product(db: Session, order_id: int, order_product_id: int, user: User):
    order_product = check_order_product(db, order_id, order_product_id, user)
    order = order_product.order
    order.total_price -= order_product.total_price
    db.delete(order_product)
    db.commit()
    db.refresh(order)
    return order


def advance_order(db: Session, order_id: int, admin: User):
    order = check_order_user(db, order_id, admin)
    order.status = OrderStatus.PAID.value
    db.commit()
    db.refresh(order)
    return order