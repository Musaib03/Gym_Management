from django.db import models

# Memberships Model
class Membership(models.Model):
    membership_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # in months
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.membership_type

# Members Model
class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    dob = models.DateField(blank=True, null=True)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Trainers Model
class Trainer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Payments Model
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Online', 'Online'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Payment {self.id} - {self.member}"

# Classes Model
class Class(models.Model):
    class_name = models.CharField(max_length=100)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)
    schedule_time = models.TimeField()
    duration = models.IntegerField()  # in minutes

    def __str__(self):
        return self.class_name

# Attendance Model
class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    attendance_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Attendance {self.id} - {self.member}"

# Equipment Model
class Equipment(models.Model):
    CONDITION_STATUS_CHOICES = [
        ('New', 'New'),
        ('Good', 'Good'),
        ('Needs Repair', 'Needs Repair'),
        ('Out of Service', 'Out of Service'),
    ]

    equipment_name = models.CharField(max_length=100)
    purchase_date = models.DateField()
    condition_status = models.CharField(max_length=20, choices=CONDITION_STATUS_CHOICES)
    maintenance_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.equipment_name
