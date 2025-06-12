from users.models import User

email = 'admin@example.com'
first_name = 'Admin'
last_name = 'User'
password = 'admin12345'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password
    )
    print('Суперпользователь создан!')
else:
    print('Суперпользователь уже существует.') 