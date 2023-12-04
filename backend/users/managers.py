# from django.contrib.auth.base_user import BaseUserManager


# class UserManager(BaseUserManager):
#     def create_user(self, email, username, password, **extra_fields):
#         if not email:
#             raise ValueError('Почта не может быть пустой!')
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, username, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)

#         if not extra_fields.get('is_superuser'):
#             raise ValueError(
#                 'Суперпользователь должен иметь is_superuser=True!'
#             )
#         return self.create_user(email, username, password, **extra_fields)
