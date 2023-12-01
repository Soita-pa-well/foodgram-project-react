# from django.contrib.auth.base_user import BaseUserManager


# class Manager(BaseUserManager):
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError('Пользователь должен иметь email')
#         user = self.model(email=email,)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
