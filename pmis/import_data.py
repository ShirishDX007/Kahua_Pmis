import csv
import pandas as pd
from django.contrib.auth.models import User
from pmis.models import Project, Task
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kahua.settings')
django.setup()


def import_task_data(csv_file_path):
    """
    Imports task data from a CSV file.

    Args:
        csv_file_path (str): The path to the CSV file.

    Returns:
        None
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Iterate over the DataFrame rows and create Task objects
        for index, row in df.iterrows():
            # Assuming CSV columns are: task_name, status, start_date, end_date, assigned_to_email, project_id
            task_name = row['task_name']
            date_created = row['date_created']
            status = row['status']
            project_id = row['project_id']
            assigned_to_id = row['assigned_to_id']

            task_start_date = row['start_date']
            task_end_date = row['end_date']
            
           
            # Fetch the Project object
            project = Project.objects.get(id=project_id)

            # Fetch the User object (assuming assigned_to_email is a valid email)
            assigned_to_user = User.objects.get(email=assigned_to_id)

            # Create the Task object
            task = Task.objects.create(
                    name=task_name,
                    date_created=date_created,  
                    status=status,
                    project=project,
                    assigned_to=assigned_to_user,
                    start_date=start_date,
                    end_date=end_date,
                    
                    
            )
            task.save()

        print("Task data imported successfully.")

    except Exception as e:
        print(f"Error importing task data: {e}")


# Example usage:
import_task_data('tasks.csv')

