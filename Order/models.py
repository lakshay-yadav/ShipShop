# from django.db import models
# from Authentication.models import CustomUser
# from UserProfile.models import Address


# # Create your models here.

# class Payment(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     payment_id = models.CharField(max_length=100)
#     payment_method = models.CharField(max_length=100)
#     amount_paid = models.CharField(max_length=100) # this is the total amount paid
#     status = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.payment_id
    

# class Order(models.Model):
#     STATUS = (
#         ('New', 'New'),
#         ('Accepted', 'Accepted'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#     )

#     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
#     payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
#     order_number = models.CharField(max_length=20)
#     address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
#     order_total = models.FloatField()
#     status = models.CharField(max_length=10, choices=STATUS, default='New')
#     is_ordered = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def order_created(self):
#         return self.created_at.strftime('%B %d %Y')

#     def hour_update(self):
#         return self.created_at.strftime('%H:%M %p')
        
#     def __str__(self):
#         return self.address.first_name
    
    
