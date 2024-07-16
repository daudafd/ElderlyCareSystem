# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from .models import Client
from django.db.models import Avg, Count
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, auth
from .forms import ClientRegistrationForm, UserRegistrationForm
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# @admin_only
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def staff(request):
    users = User.objects.filter(is_staff=False)  # Fetch all users except those with is_staff=True
    return render(request, 'staff.html', {'users': users})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_client(request):
    users = User.objects.all()  # Query all users to pass to the template for dropdown

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            assigned_user = form.cleaned_data.get('assigned_user')  # Get selected user from form data

            print("Form cleaned data:", form.cleaned_data)

            if assigned_user:
                client.user = assigned_user  # Explicitly assign user to client
            client.save()
            return redirect('client')  # Redirect to the 'client' view to display the client list
    else:
        form = ClientRegistrationForm()

    return render(request, 'add_client.html', {'form': form, 'users': users})


@login_required(login_url='/login/')
@allowed_users(allowed_roles=['admin'])
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            # Handle password mismatch error
            return render(request, 'staff.html', {'error': 'Passwords do not match!'})

        # Create a new user object
        User = get_user_model()
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()

        # Optional: Use signals for group assignment (replace 'user' with your group name)
        # @receiver(user_registered)
        # def assign_user_group(sender, user, request, **kwargs):
        #     user_group = Group.objects.get(name='user')
        #     user.groups.add(user_group)

        # Or, assign group directly within the view function
        group = Group.objects.get(name='user')
        user.groups.add(group)

        # Handle successful user creation (e.g., redirect to a success page)
        return redirect('staff')  # Replace 'success_url' with your desired redirect

    return render(request, 'staff.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def client(request):
    clients = Client.objects.all()
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client')  # Stay on the same page to refresh the client list
    else:
        form = ClientRegistrationForm()
    return render(request, 'client.html', {'clients': clients, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def user_client(request):
    clients = Client.objects.all()

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_client')  # Stay on the same page to refresh the client list
    else:
        form = ClientRegistrationForm()

    return render(request, 'user_client.html', {'clients': clients, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    users = User.objects.all()  # Query all users for the dropdown

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            assigned_user = form.cleaned_data.get('assigned_user')  # Get selected user from form data

            print("Form cleaned data:", form.cleaned_data)

            if assigned_user:
                client.user = assigned_user  # Explicitly assign user to client
            client.save()
            return redirect('client')
    else:
        form = ClientRegistrationForm(instance=client)

    return render(request, 'edit_client.html', {'form': form, 'users': users, 'client': client})



@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def client_profile(request, client_id):
    # Fetch the client object by its primary key (client_id)
    client = get_object_or_404(Client, pk=client_id)

    context = {
        'client': client,  # Pass the client object to the template
    }
    return render(request, 'client_profile.html', context)


@login_required(login_url='login')
def chart(request):
    data_entries = Client.objects.all()
    avg_age = Client.objects.all().aggregate(Avg('age'))['age__avg']
    avg_weight = Client.objects.all().aggregate(Avg('weight'))['weight__avg']
    avg_height = Client.objects.all().aggregate(Avg('height'))['height__avg']
    count_entries = Client.objects.all().aggregate(Count('id'))['id__count']

    context = {
        'data_entries': data_entries,
        'avg_age': avg_age,
        'avg_weight': avg_weight,
        'avg_height': avg_height,
        'count_entries': count_entries,
    }
    return render(request, 'chart.html', context)


def client_statistics(request):
    # Query to count clients by gender
    gender_counts = Client.objects.values('gender').annotate(count=Count('gender'))

    # Prepare data for chart
    genders = [item['gender'] for item in gender_counts]
    counts = [item['count'] for item in gender_counts]

    # Render the template with the data
    return render(request, 'client_statistics.html', {'genders': genders, 'counts': counts})


@login_required(login_url='login')
def generate_pdf(request):
    data_entries = Client.objects.all()
    avg_age = Client.objects.all().aggregate(Avg('age'))['age__avg']
    avg_weight = Client.objects.all().aggregate(Avg('weight'))['weight__avg']
    avg_height = Client.objects.all().aggregate(Avg('height'))['height__avg']
    count_entries = Client.objects.all().aggregate(Count('id'))['id__count']
    chart_image_base64 = request.POST.get('chart_image_base64')
    chart_image_url = f"data:image/png;base64,{chart_image_base64}"

    context = {
        'data_entries': data_entries,
        'avg_age': avg_age,
        'avg_weight': avg_weight,
        'avg_height': avg_height,
        'count_entries': count_entries,
        'chart_image_url': chart_image_url,
    }

    template = get_template('pdf_template.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    HTML(string=html).write_pdf(response)
    return response

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('input_username')
        password = request.POST.get('input_password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
