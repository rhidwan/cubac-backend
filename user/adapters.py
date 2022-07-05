from allauth.account.adapter import DefaultAccountAdapter


class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field

        user = super().save_user(request, user, form, False)
        user_field(user, 'gender', request.data.get('gender', ''))
        user_field(user, 'full_name', request.data.get('full_name', ''))
        user_field(user, 'date_of_birth', request.data.get('date_of_birth', ''))
        user.save()
        return user