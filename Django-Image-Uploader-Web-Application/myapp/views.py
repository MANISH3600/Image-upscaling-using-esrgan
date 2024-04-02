from django.shortcuts import render
from .forms import UserRegsitrationForm,UpdateUserForm,ProfileUpdateForm
from .models import ImageUploader
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from PIL import Image
from .utils import enhance_image
from django.core.files.base import ContentFile
from io import BytesIO

def convert_image(binary_data, format='JPEG'):
    try:
        # Create a BytesIO object to read binary data
        image_buffer = BytesIO(binary_data)
        
        # Open the image using PIL
        with Image.open(image_buffer) as img:
            # Convert the image to the desired format (JPEG or PNG)
            output_buffer = BytesIO()
            img.save(output_buffer, format=format)
            
            # Return the converted image data
            return output_buffer.getvalue()
    except Exception as e:
        print("Error converting image:", e)
        return None


def home(request):
    if request.method == "POST" and 'upload' in request.POST:
        img_name = request.POST.get('img_name')
        img = request.FILES.get('img')
        u_profile = request.POST.get('u_profile')

        img_uploader = ImageUploader(
            image_name=img_name,
            image=img,
            user=request.user,
            user_profile=u_profile,
            date=datetime.now()
        )

        enhanced_image = enhance_image(img)

        if enhanced_image is not None:
            # Save the enhanced image as PNG format
            output_buffer = BytesIO()
            output_buffer.write(enhanced_image)
            img_uploader.enhanced_image.save('enhanced_' + img.name + '.png', ContentFile(output_buffer.getvalue()), save=False)
            img_uploader.save()

            messages.success(request, 'Your Image Uploaded and Enhanced Successfully !!')

    images = ImageUploader.objects.all()
    return render(request, 'home.html', {'images': images})

def signup(request):
        if request.method == "POST":
                fm = UserRegsitrationForm(request.POST)
                if fm.is_valid():
                        fm.save()
                        messages.success(request,'Signup Done !!')

        else:
                fm  = UserRegsitrationForm()

        context = {'fm':fm}
        return render(request,'signup.html',context)

@login_required
def profile(request):

        if request.method == "POST":
                u_form = UpdateUserForm(instance = request.user,data=request.POST)
                p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    messages.success(request, f'Your Profile has been updated!')


        
        
        else:
                u_form = UpdateUserForm(instance = request.user)
                p_form = ProfileUpdateForm(instance = request.user.profile)

        return render(request,'profile.html',{'u_form':u_form,'p_form':p_form})


def user_profile(request,user):

        users = User.objects.get(username=user)
        image = ImageUploader.objects.filter(user=user)


        return render(request,'user-profile.html',{'users':users,'image':image})
