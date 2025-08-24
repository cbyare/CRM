class Customer:
    def __init__(self, customer_id, name, age, address, mother_name, date_of_registration, gender, email):
        self.Id = customer_id
        self.Name = name
        self.Age = age
        self.Address = address
        self.MotherName = mother_name
        self.DateOfRegistration = date_of_registration
        self.Gender = gender
        self.Email = email

    def to_dict(self):
        return {
            "Id": self.Id,
            "Name": self.Name,
            "Age": self.Age,
            "Address": self.Address,
            "MotherName": self.MotherName,
            "DateOfRegistration": self.DateOfRegistration,
            "Gender": self.Gender,
            "Email": self.Email
        }