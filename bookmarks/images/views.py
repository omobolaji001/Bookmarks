from django.shortcuts import render, redirect
from .forms import ImageCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def image_create(request):
    """ Handles image creation form """
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')

            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html',
                      {'section': 'images', 'form': form})