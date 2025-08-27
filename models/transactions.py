class Transaction:
    def __init__(self, transaction_id, service_id, customer_id, amount, transaction_type, action_user, status, date):
        self.Id = transaction_id
        self.ServiceId = service_id
        self.CustomerId = customer_id
        self.Amount = amount
        self.TransactionType = transaction_type
        self.ActionUser = action_user
        self.Status = status
        self.Date = date

    def to_dict(self):
        return {
            "Id": self.Id,
            "ServiceId": self.ServiceId,
            "CustomerId": self.CustomerId,
            "Amount": self.Amount,
            "TransactionType": self.TransactionType,
            "ActionUser": self.ActionUser,
            "Status": self.Status,
            "Date": self.Date
        }
