class UsageRecords:
    def __init__(self, Usage_id, customer_id, Usage_type, quantity, Usage_date, duaration, destination, cost, status, mobile, message):
        self.Usage_id = Usage_id
        self.customer_id = customer_id
        self.Usage_type = Usage_type
        self.quantity = quantity
        self.Usage_date = Usage_date
        self.duaration = duaration
        self.destination = destination
        self.cost = cost
        self.status = status
        self.mobile = mobile
        self.message = message

    def to_dict(self):
        return {
            "Usage_id": self.Usage_id,
            "customer_id": self.customer_id,
            "Usage_type": self.Usage_type,
            "quantity": self.quantity,
            "Usage_date": self.Usage_date,
            "duaration": self.duaration,
            "destination": self.destination,
            "cost": self.cost,
            "status": self.status,
            "mobile": self.mobile,
            "message": self.message
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            Usage_id=data.get("Usage_id"),
            customer_id=data.get("customer_id"),
            Usage_type=data.get("Usage_type"),
            quantity=data.get("quantity"),
            Usage_date=data.get("Usage_date"),
            duaration=data.get("duaration"),
            destination=data.get("destination"),
            cost=data.get("cost"),
            status=data.get("status"),
            mobile=data.get("mobile"),
            message=data.get("message")
        )