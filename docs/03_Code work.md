### run project with local server on lan

```bash
python manage.py tailwind runserver 0.0.0.0:8000
```

## project working

- register, login, logout

### Date: 12/02/2025

Working on register and login,

Not login and it using user.username from admin name when admin is login in web header
user (admin) and customer account relation problem

**Example account**

```plaintext
dilip@gmail.com
+3JC*Y>N$$+f.GN
```

## Backup code

here is some views that for reset password from the admin panal
but i need reset password for uesr side not with admin panal

this code for backup to use if needed

```python
path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
```

### Message alert type in Django

```python
from django.contrib import messages

# Success message with alert-success tag
messages.success(request, "Operation completed successfully!", extra_tags="alert-success")

# Info message with alert-info tag
messages.info(request, "Here's some important information.", extra_tags="alert-info")

# Warning message with alert-warning tag
messages.warning(request, "Please be cautious.", extra_tags="alert-warning")

# Error message with alert-danger tag
messages.error(request, "An error occurred.", extra_tags="alert-danger")

```
