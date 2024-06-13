# management/commands/import_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils.dateparse import parse_datetime

from tdapp.models import *
from tdapp.serializers import *

import json

class Command(BaseCommand):
    help = 'Import JSON data into Django models'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)

        for user_data in data['users']:
            # Create or update CustomUser
            user_id = user_data['id']
            user_data['password'] = make_password(user_data['password'])  # Hash password
            user_data['last_login'] = parse_datetime(user_data['last_login'])
            user_data['date_joined'] = parse_datetime(user_data['date_joined'])

            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_instance = user_serializer.save()
            else:
                self.stdout.write(self.style.ERROR(f'Error importing user data: {user_serializer.errors}'))
                continue

            # Create or update projects for the user
            for project_data in user_data.get('projects', []):
                project_serializer = ProjectSerializer(data=project_data)
                if project_serializer.is_valid():
                    project_instance = project_serializer.save()
                else:
                    self.stdout.write(self.style.ERROR(f'Error importing project data: {project_serializer.errors}'))
                    continue

                # Create or update tasks for the project
                for task_data in project_data.get('tasks', []):
                    task_data['assigned_to'] = user_instance.id
                    task_data['project_name'] = project_instance.project_id

                    task_serializer = TaskSerializer(data=task_data)
                    if task_serializer.is_valid():
                        task_instance = task_serializer.save()
                    else:
                        self.stdout.write(self.style.ERROR(f'Error importing task data: {task_serializer.errors}'))
                        continue

                    self.stdout.write(self.style.SUCCESS(f'Successfully imported task: {task_instance.task_name}'))

                self.stdout.write(self.style.SUCCESS(f'Successfully imported project: {project_instance.project_name}'))

            self.stdout.write(self.style.SUCCESS(f'Successfully imported user: {user_instance.email}'))
