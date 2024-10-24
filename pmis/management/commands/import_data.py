import csv
from django.core.management import BaseCommand, CommandError
from pmis.models import Project, Task, Client
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = "import task data from csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='path to csv file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    print(row)

                    try:
                        task_start_date = datetime.strptime(row['task_start_date'], '%d-%m-%Y')
                        task_end_date = datetime.strptime(row['task_end_date'], '%d-%m-%Y')
                        date_created = datetime.strptime(row['date_created'], '%d-%m-%Y')
                    except ValueError as ve:
                        self.stderr.write(f"Date conversion error: {ve}")
                        continue

                    try:
                        # Get the project correctly (removed the unnecessary unpacking)
                        project = Project.objects.get(id=row['project_id'])
                    except Project.DoesNotExist:
                        self.stderr.write(f"Project with id {row['project_id']} does not exist")
                        continue

                    try:
                        # Handle assigned_to as user (adjust this according to what 'assigned_to' contains)
                        assigned_to = Client.objects.get(id=row['assigned_to_id'])  # assuming 'assigned_to_id' refers to user id
                    except Client.DoesNotExist:
                        self.stderr.write(f"User with id {row['assigned_to_id']} does not exist")
                        continue
                    
                    # Create task
                    try:
                        task = Task.objects.create(
                            name=row['name'],
                            date_created=date_created,  # Use parsed dates
                            task_start_date=task_start_date,
                            task_end_date=task_end_date,
                            assigned_to=assigned_to,
                            status=int(row['status']),
                            project=project
                        )
                        task.full_clean()  # Validate the task object
                        task.save()
                    except ValidationError as e:
                        self.stderr.write(self.style.ERROR(f"Validation error for task '{row['name']}': {e}"))
                        continue
        except FileNotFoundError:
            raise CommandError(f"File not found: {csv_file_path}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error importing data: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("Data imported successfully"))
