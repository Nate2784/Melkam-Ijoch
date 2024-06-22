from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, CompanyInformation,Charity,Project,Donation,AddCharity
from .forms import SignUpForm,UserProfileForm, DonationForm,AddCharityForm, ProjectForm #,ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_superuser

# Create your views here.

def home(request):
    info = CompanyInformation.objects.first()
    charityOrganizations = Charity.objects.all()
    return render(request, 'pages/index.html',{'company_info':info,"charityOrganizations":charityOrganizations})

from django.db.models import Q

def charities(request):
    info = CompanyInformation.objects.first()
    charityOrganizations = Charity.objects.all()
    query = request.GET.get('q')

    if query:
        charityOrganizations = charityOrganizations.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(location__icontains=query)
        )

    return render(request, 'pages/charity.html', {
        'company_info': info,
        'charityOrganizations': charityOrganizations
    })


def charity_detail(request, id):
    info = CompanyInformation.objects.first()
    charity = get_object_or_404(Charity, pk=id)
    projects = Project.objects.filter(Q(status=True) & Q(charity_ID=charity))
    query = request.GET.get('q')

    if query:
        projects = projects.filter(name__icontains=query)

    return render(request, 'pages/display.html', {
        'company_info': info,
        'charity': charity,
        'projects': projects
    })


def project_list(request):
    info = CompanyInformation.objects.first()
    charityOrganizations = Charity.objects.all()
    projects = Project.objects.filter(status = True)
    query = request.GET.get('q')

    if query:
        projects = projects.filter(
            Q(name__icontains=query) | 
            Q(charity_ID__name__icontains=query)
        )

    return render(request, 'pages/projects.html', {
        'company_info': info,
        'charityOrganizations': charityOrganizations,
        'projects': projects
    })


@login_required 
def make_donation(request, user_id, project_id, charity_id):
    info = CompanyInformation.objects.first()
    charityOrganizations = Charity.objects.all()
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user_ID_id = user_id
            donation.project_ID_id = project_id
            donation.charity_ID_id = charity_id
            donation.save()
            # Redirect to a success page or handle as needed
            return redirect('donations')  # Replace with your actual success URL name
    else:
        # Pre-fill the form with user ID, project ID, and charity ID
        form = DonationForm(initial={'user_ID': user_id, 'project_ID': project_id, 'charity_ID': charity_id})

    return render(request, 'pages/donation_form.html', {'company_info':info,"charityOrganizations":charityOrganizations,'form': form})


@login_required 
def user_donations(request):
    info = CompanyInformation.objects.first()
    charityOrganizations = Charity.objects.all()
    donations = Donation.objects.filter(user_ID=request.user).order_by('-donationDate')
    return render(request, 'pages/donations.html', {'company_info':info,"charityOrganizations":charityOrganizations,'donations': donations})

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Donation


@login_required 
def download_receipt(request, donation_id):
    donation = Donation.objects.get(id=donation_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{donation_id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 770, f"Melkam ejoch.")
    p.drawString(100, 750, f"Receipt for Donation {donation.id}")
    p.drawString(100, 735, f"User: {donation.user_ID.username}")
    p.drawString(100, 720, f"Project: {donation.project_ID.name}")
    p.drawString(100, 705, f"Charity: {donation.charity_ID.name}")
    p.drawString(100, 690, f"Amount: ${donation.amount}")
    p.drawString(100, 675, f"Donation Date: {donation.donationDate.strftime('%B %d, %Y')}")
    p.drawString(100, 660, f"Payment Method: {donation.paymentMethod}")
    p.drawString(100, 645, f"Transaction ID: {donation.paymentTransactionID}")
    
    p.drawString(100, 620, f"Thank you for your donation..")

    p.showPage()
    p.save()
    return response

def login_view(request):
    
    info = CompanyInformation.objects.first()
    charityOrganizations = Charity.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, 'auth/login.html', {'company_info':info})


def signup_view(request):
    info = CompanyInformation.objects.first()
    charityOrganizations = Charity.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)  
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                profile.avatar = form.cleaned_data.get('avatar') or 'default.jpg'
                profile.save()
            login(request, user)
            return redirect('Home')
    else:
        form = SignUpForm()  
    return render(request, 'auth/signup.html', {"charityOrganizations":charityOrganizations,'form': form,'company_info':info})


@login_required 
def profile_view(request):
    if request.user.is_authenticated:
        charityOrganizations = Charity.objects.all()
        profile = Profile.objects.get(user=request.user)
        info = CompanyInformation.objects.first()
        
        if request.method == 'POST':
            form = SignUpForm(request.POST, request.FILES, instance=request.user)

            if form.is_valid():
                form.save()

                return redirect('profile')

        else:
            form = SignUpForm(instance=request.user)
        return render(request, 'users/profile.html', {'profile': profile, 'company_info': info,'form': form})
    else:
        return redirect('login')

from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    info = CompanyInformation.objects.first()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'company_info': info,'form': form})
   
@login_required
def profile_update(request):
    info = CompanyInformation.objects.first()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form,'company_info':info})

@login_required
def profile_delete(request):
    user = request.user
    user.delete()
    return redirect('Home')


@login_required 
def profile_delete_confirm(request):
    info = CompanyInformation.objects.first()
    return render(request, 'users/profile_delete_confirm.html',{'company_info':info})


@login_required 
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required  
def add_charity_view(request):
    info = CompanyInformation.objects.first()
    if request.method == 'POST':
        form = AddCharityForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the authenticated user as the user_ID
            form.instance.user_ID = request.user
            # Set the default status (False)
            form.instance.status = False
            form.save()
            return redirect('profile')  # Redirect to a success page
    else:
        form = AddCharityForm()

    return render(request, 'users/add_charity.html', {'form': form,'company_info':info})

@user_passes_test(is_superuser)
def new_charity(request):
    charities =AddCharity.objects.all()
    info = CompanyInformation.objects.first()

    return render(request, 'admin/new_charity.html',{'charities':charities,'company_info':info})


@login_required  
def add_project(request):
    info = CompanyInformation.objects.first()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            project = form.save(commit=False)
            project.user_ID = request.user
            project.save()
            return redirect('profile') 
    
    else:
        form = ProjectForm(user=request.user)
    return render(request, 'users/add_project.html', {'form': form,'company_info':info})


@user_passes_test(is_superuser)
def new_project(request):
    projects = Project.objects.filter(Q(status=True) | Q(status=False))
    info = CompanyInformation.objects.first()

    return render(request, 'admin/new_project.html',{'company_info':info,'projects':projects})

@user_passes_test(is_superuser)
def set_charity_status(request, charity_id):
    charity = get_object_or_404(AddCharity, id=charity_id)
    charity.status = True
    charity.save()

    # Retrieve relevant data from AddCharity
    name = charity.name
    image = charity.image
    description = charity.description
    website = charity.website
    location = charity.location
    establishedYear = charity.establishedYear
    user_ID = charity.user_ID  

    # Create a new Charity object
    new_charity = Charity(
        user_ID=user_ID,  
        name=name,
        image=image,
        description=description,
        website=website,
        location=location,
        establishedYear=establishedYear
    )
    new_charity.save()

    return redirect('new_charity')


@user_passes_test(is_superuser)
def remove_charity(request, charity_id):

    add_charity = get_object_or_404(AddCharity, id=charity_id)

    try:
        Charity.objects.filter(name=add_charity.name).delete() 
    except Charity.DoesNotExist:
        pass 

    add_charity.status = False
    add_charity.save()

    return redirect('new_charity')

@user_passes_test(is_superuser)
def remove_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = False 
    project.save()
    return redirect('new_project') 

@user_passes_test(is_superuser)
def set_project_status(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = True
    project.save()
    return redirect('new_project') 
