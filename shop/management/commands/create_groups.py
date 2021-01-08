from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group, Permission
import logging

# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
#
# from .models import Order
#
# customer_group, created = Group.objects.get_or_create(name='customer')
# ct = ContentType.objects.get_for_model(Order)
# permission = Permission.objects.create(codename='can_place_order', name='Can place order', content_type=ct)
# customer_group.permissions.add(permission)
from shop.models import CustomUser

GROUPS = {
    "Administration": {
        # general permissions

        # "log entry": ["add", "delete", "change", "view"],
        "group": ["add", "delete", "change", "view"],
        "permission": ["add", "delete", "change", "view"],
        # "custom_user": ["add", "delete", "change", "view"],
        "content type": ["add", "delete", "change", "view"],
        "session": ["add", "delete", "change", "view"],

        # django app model specific permissions
        "product": ["add", "delete", "change", "view"],
        "order": ["add", "delete", "change", "view"],
        # "staff time sheet": ["add", "delete", "change", "view"],
        # "staff": ["add", "delete", "change", "view"],
        # "client": ["add", "delete", "change", "view"],
    },

    "Customer": {
        # django app model specific permissions
        "order": ["add", "delete", "change", "view"],
    },
}

USERS = {
    "my_member_user": ["Customer", "imasif@gmail.com", "1234"],
    "Admin": ["Administration", "imasifkhan1010@gmail.com", "1234"],
}


class Command(BaseCommand):
    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):

        for group_name in GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for app_model in GROUPS[group_name]:

                # Loop permissions in group/model
                for permission_name in GROUPS[group_name][app_model]:

                    # Generate permission name as Django would generate it
                    name = "Can {} {}".format(permission_name, app_model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

            for user_name in USERS:

                new_user = None
                if user_name == "Admin":
                    new_user, created = CustomUser.objects.get_or_create(
                        first_name="Admin",
                        last_name="User",
                        email=USERS[user_name][1],
                        active=True, is_staff=True, is_superuser=True,)
                else:
                    new_user, created = CustomUser.objects.get_or_create(
                        first_name="Auto created",
                        last_name="User",
                        email=USERS[user_name][1],)

                new_user.set_password(USERS[user_name][2])
                new_user.save()

                if USERS[user_name][0] == str(new_group):
                    new_group.user_set.add(new_user)

                    print("Adding {} to {}".format(user_name, new_group))
