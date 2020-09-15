from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail

from .models import Food
from .forms import EmailFoodForm, CommentForm

def food_list(request):

    object_list = Food.objects.all()
    paginator = Paginator(object_list,3)
    page = request.GET.get('page')
    try:
        foods = paginator.page(page)
    except PageNotAnInteger:         #If page is not an integer deliver the first page
        foods = paginator.page(1)     
    except EmptyPage:            #if page is out of range deliver last page of results
        foods = paginator.page(paginator.num_pages)

    context = {'page':page,'foods':foods}

    return render(request, 'foodblog/food/list.html', context)

def food_detail(request, slug):
    food=get_object_or_404(Food,slug=slug,status='published')

    comments = food.comments.filter(active=True) 
    commented=False 
    if request.method == 'POST': 
        comment_form = CommentForm(data=request.POST) 
        if comment_form.is_valid():  
            new_comment = comment_form.save(commit=False) 
            new_comment.food = food 
            new_comment.save() 
            commented=True 
    else: 
        comment_form = CommentForm()

    context = {'food':food,
            'commented':commented,'comments':comments,'comment_form':comment_form}

    return render(request, 'foodblog/food/detail.html', context)

def food_share(request, food_id):
    food = get_object_or_404(Food, id=food_id, status='published')
    sent = False
    form = EmailFoodForm()
    if request.method == 'POST':
        form = EmailFoodForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            food_url = request.build_absolute_uri(food.get_absolute_url())
            subject = '{} recommends you reading "{}"'.format(cd['name'],food.title)
            message = 'Read "{}" post at {} \n\n{}\'s comments: {}'.format(food.title,
                        food_url, cd['name'],cd['comments'])
            send_mail(subject, message,'admin@myblog.com',[cd['to']])
            sent = True
            
    context = {'food':food,'form':form,'sent':sent}

    return render(request, 'foodblog/post/share.html', context)