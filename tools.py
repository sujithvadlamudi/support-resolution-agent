def get_order_status(order_id: str) -> dict:
    """Pretend order-tracking system. Returns fake but realistic data."""
    fake_database = {
        "4521": {"status": "in_transit", "days_since_ordered": 10, "estimated_delivery_days": 12},
        "7890": {"status": "delivered", "days_since_ordered": 3, "estimated_delivery_days": 3},
        "3345": {"status": "confirmed", "days_since_ordered": 1, "estimated_delivery_days": 5},
    }
    return fake_database.get(order_id, {"status": "not_found", "message": "No order with this ID exists."})