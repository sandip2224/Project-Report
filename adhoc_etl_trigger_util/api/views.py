from django.http import JsonResponse
import subprocess
import pyodbc
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# Main view
def main_view(request):
    return render(request, 'main.html')

def execute_steps(request):
    try:
        # Execute Step 1
        step1_success = execute_step1()

        # Execute Step 2 only if Step 1 succeeds
        step2_success = False
        if step1_success:
            step2_success = execute_step2()

        # Execute Step 3 only if Step 2 succeeds
        step3_success = False
        if step2_success:
            step3_success = execute_step3()

        # Return the success status of each step in the JSON response
        return JsonResponse({'success': True, 'step1_success': step1_success, 'step2_success': 'step2_success', 'step3_success': step3_success})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Define function to execute stored procedure in DB1
def execute_step1():
    try:
        # Connect to DB1
        conn1 = pyodbc.connect('DRIVER={Your_DB1_Driver};SERVER=Your_Server;DATABASE=Your_DB1;UID=Your_User;PWD=Your_Password')

        # Create a cursor
        cursor1 = conn1.cursor()

        # Execute the stored procedure
        cursor1.execute("EXEC Your_Stored_Procedure_Name")

        # Commit the transaction
        conn1.commit()

        # Close the cursor and connection
        cursor1.close()
        conn1.close()

        return True  # Step 1 executed successfully
    except Exception as e:
        print(f"Error executing step 1: {e}")
        return False  # Step 1 failed
# Step 2:
def execute_step2():
    try:
        # Connect to DB2
        conn2 = pyodbc.connect('DRIVER={Your_DB2_Driver};SERVER=Your_Server;DATABASE=Your_DB2;UID=Your_User;PWD=Your_Password')

        # Create a cursor
        cursor2 = conn2.cursor()

        # Execute 12 stored procedures one at a time
        for i in range(1, 13):
            cursor2.execute(f"EXEC Your_Stored_Procedure_Name_{i}")

        # Commit the transaction
        conn2.commit()

        # Close the cursor and connection
        cursor2.close()
        conn2.close()

        return True  # Step 2 executed successfully
    except Exception as e:
        print(f"Error executing step 2: {e}")
        return False  # Step 2 failed

# Step 3: Execute a local .exe file
def execute_step3():
    try:
        # Replace 'your_exe_file.exe' with the actual path to your .exe file
        subprocess.run(['your_exe_file.exe'], check=True)
        return True  # Step 3 executed successfully
    except Exception as e:
        print(f"Error executing step 3: {e}")
        return False  # Step 3 failed
