from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Polls_Create
from .forms import Polls_CreateForm,Polls_UpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url='login')
def polls_read(request):
    # return HttpResponse("Hello world!!!")

    Polls_items = Polls_Create.objects.all()
    #Polls_items = Polls_Create.objects.filter(user=request.user)

    # Pagination - Starts
    poll_paginator_obj = Paginator(Polls_items, 5)
    poll_page_number = request.GET.get("page")
    # or
    #todo_page_number = request.GET["page"]
    poll_page = poll_paginator_obj.get_page(poll_page_number)
    # Pagination - Ends

    context = {
        'Polls_items': Polls_items,
        'poll_page': poll_page,

    }

    return render(request,'vote/home.html',context)

@login_required(login_url='login')
def polls_create(request):
    # return HttpResponse("Hello world!!!")

    #Polls_items = Polls_Create.objects.all()

    if request.method == "POST":
        poll_create_form = Polls_CreateForm(request.POST)
        if poll_create_form.is_valid():
            poll_save = poll_create_form.save(commit=False)
            poll_save.user = request.user
            poll_save.save()
            return redirect("/")
    else:
        poll_create_form = Polls_CreateForm()

    context = {
        'poll_create_form': poll_create_form

    }

    return render(request,'vote/create.html',context)


def polls_vote(request, pk):

    Item_to_be_polled = Polls_Create.objects.get(id=pk)

    if request.method == "POST":
        polled_selected_option = request.POST['poll']

        if polled_selected_option == 'option1':
            Item_to_be_polled.option_one_count+=1
        elif polled_selected_option == 'option2':
            Item_to_be_polled.option_two_count+=1
        elif polled_selected_option == 'option3':
            Item_to_be_polled.option_three_count+=1
        else:
            # return HttpResponse(400,'Invalid entry')
            messages.error(request, "Invalid entry")

        Item_to_be_polled.voted = True

        # voted_list = []
        # print(request.user)
        # print(type(request.user))
        # Item_to_be_polled.voted_list+=list(request.user)

        # Item_to_be_polled.voted_info=request.user

        # print("Item_to_be_polled.voted_info: ",Item_to_be_polled.voted_info)
        # Item_to_be_polled.is_current_user_voted = False
        # if Item_to_be_polled.user == request.user:
        #     Item_to_be_polled.is_poll_created_user_voted = True
        #     print("Inside if")
        # elif Item_to_be_polled.user != request.user:
        #     Item_to_be_polled.is_current_user_voted = True
        #     print("Elif")

        Item_to_be_polled.save()

        return redirect('result', Item_to_be_polled.id)

    
    # Trigger_found = False
    # # Item_to_be_polled.is_current_user_voted = False
    # # print("Polls_Create.objects.filter(user=request.user,id=pk,voted=True).exists(): ",Polls_Create.objects.filter(user=request.user,id=pk,voted=True).exists()) 
    # if Item_to_be_polled.user == request.user:
    #     if Polls_Create.objects.filter(id=pk,is_poll_created_user_voted=True).exists():
    #         Trigger_found = True
    #         messages.warning(request, "First--- You already voted for this Poll!!!!!")
    #         print("Trigger_found: ",Trigger_found)
    #         return redirect('/')
    # elif Item_to_be_polled.user != request.user:
    #     if Polls_Create.objects.filter(id=pk,is_current_user_voted=True).exists():
    #         Trigger_found = True
    #         messages.warning(request, "Second--- You already voted for this Poll!!!!!")
    #         print("Trigger_found: ",Trigger_found)
    #         return redirect('/')
    # print("Trigger_not_found: ",Trigger_found)

    # if Polls_Create.objects.filter(user=Item_to_be_polled.user,id=pk,is_poll_created_user_voted=True).exists() or Polls_Create.objects.filter(user=request.user,id=pk,is_current_user_voted=True).exists():
    #     # print("--- First If ---")
    #     # Trigger_found = True
    #     # messages.warning(request, "First--- You already voted for this Poll!!!!!")
    #     # if Polls_Create.objects.filter(user=request.user,id=pk,voted=True).exists():        
    #         # print("--- Second If ---")
    #     Trigger_found = True
    #     messages.warning(request, "Second--- You already voted for this Poll!!!!!")
    #     print("Trigger_found: ",Trigger_found)
    #     return redirect('/')


    context = {
        'Item_to_be_polled': Item_to_be_polled,
        # 'Trigger_found': Trigger_found

    }

    return render(request,'vote/vote.html',context)

def polls_result(request, pk):
    
    Item_polled = Polls_Create.objects.get(id=pk)

    context = {
        'Item_polled': Item_polled

    }

    return render(request,'vote/result.html',context)


@login_required(login_url='login')
def polls_yet_to_poll(request):
    
    Items_to_be_polled = Polls_Create.objects.filter(voted=False)


    # Pagination - Starts
    poll_paginator_obj = Paginator(Items_to_be_polled, 5)
    poll_page_number = request.GET.get("page")
    # or
    #todo_page_number = request.GET["page"]
    poll_page = poll_paginator_obj.get_page(poll_page_number)
    # Pagination - Ends

    context = {
        'Items_to_be_polled': Items_to_be_polled,
        'poll_page': poll_page,

    }

    return render(request,'vote/yet_to_poll.html',context)


@login_required(login_url='login')
def polls_already_polled(request):
    
    Items_already_polled = Polls_Create.objects.filter(voted=True)


    # Pagination - Starts
    poll_paginator_obj = Paginator(Items_already_polled, 5)
    poll_page_number = request.GET.get("page")
    # or
    #todo_page_number = request.GET["page"]
    poll_page = poll_paginator_obj.get_page(poll_page_number)
    # Pagination - Ends


    context = {
        'Items_already_polled': Items_already_polled,
        'poll_page': poll_page,

    }

    return render(request,'vote/already_polled.html',context)


@login_required(login_url='login')
def polls_all_results(request):
    
    Items_already_polled = Polls_Create.objects.filter(voted=True)

    # Pagination - Starts
    poll_paginator_obj = Paginator(Items_already_polled, 5)
    poll_page_number = request.GET.get("page")
    # or
    #todo_page_number = request.GET["page"]
    poll_page = poll_paginator_obj.get_page(poll_page_number)
    # Pagination - Ends


    context = {
        'Items_already_polled': Items_already_polled,
        'poll_page': poll_page,

    }

    return render(request,'vote/all_results.html',context)


def polls_details(request,pk):

    Polls_items_details = Polls_Create.objects.get(id=pk)

    context = {
        'Polls_items_details': Polls_items_details

    }

    return render(request,'vote/poll_details.html',context)


def polls_update(request, pk):

    Polls_item_to_be_modify = Polls_Create.objects.get(id=pk)

    if request.method == 'POST':
        Polls_update_form = Polls_UpdateForm(request.POST, instance=Polls_item_to_be_modify)
        if Polls_update_form.is_valid():
            Polls_update_form.save()
            return redirect('/')
    else:
        Polls_update_form = Polls_UpdateForm(instance=Polls_item_to_be_modify)

    context = {
        'Polls_update_form': Polls_update_form,
    }

    return render(request, 'vote/update.html', context)


def polls_delete(request, pk):
    Polls_item_to_be_deleted = Polls_Create.objects.get(id=pk)

    if request.method == 'POST':
        Polls_item_to_be_deleted.delete()
        return redirect('/')

    return render(request, 'vote/delete.html')


def polls_duplicate_polling_restricting(request,pk):
    
    Items_already_polled_by_user = Polls_Create.objects.filter(user=request.user,id=pk,voted=True)

    Trigger_found = False 

    if Polls_Create.objects.filter(user=request.user,id=pk,voted=True).exists():
        Trigger_found = True
        messages.warning(request, "You already voted for this Poll!!!!!")
    

    print("Items_already_polled_by_user: ",Items_already_polled_by_user)

    context = {
        'Items_already_polled_by_user': Items_already_polled_by_user,
        'Trigger_found': Trigger_found

    }

    return render(request,'vote/vote.html',context)
