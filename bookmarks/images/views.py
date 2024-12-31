from django.shortcuts import render, redirect, get_object_or_404
from .models import Image
from .forms import ImageCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


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


def image_detail(request, id, slug):
    """ Details view of an image """
    image = get_object_or_404(Image, id=id, slug=slug)

    return render(request, 'images/image/detail.html',
                  {'section': 'images', 'image': image})


@login_required
@require_POST
def image_like(request):
    """ Allow users to like and unlike images """
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass

    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    """ Return the list of images """
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    template = 'images/image/list_images.html' if images_only else 'images/image/list.html'
    context = {'section': 'images', 'images': images}

    return render(request, template, context)
