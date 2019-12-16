from django.shortcuts import render
from .models import MeetingRoom, Bid
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import permission_required
from .forms import NewBid, CustomizeRoom
from django.contrib.auth.models import Group, User


def index(request):
    room_list = []
    meeting_rooms_list = MeetingRoom.objects.all().order_by('meeting_room_name')
    for room in meeting_rooms_list:
        first_bid = room.first_bid()
        room_list.append((room, first_bid))
    #room_list = sorted(room_list, key=lambda tup: tup[0])
    room_list = tuple(room_list)
    if request.user.has_perm('meeting_room.accept_decline_bid'):
        awaiting_solution_bids = Bid.get_awaiting_solution_bids()
    else:
        awaiting_solution_bids = []
    if request.user.has_perm('meeting_room.change'):
        is_manager = True
    else:
        is_manager = False
    return render(request, 'meeting_room/meeting_room.html', {'meeting_rooms_list': room_list,
                                                              'awaiting_solution_bids': awaiting_solution_bids,
                                                              'is_manager': is_manager,
                                                              })


@permission_required('meeting_room.accept_decline_bid')
def accept_bid(request, bid_pk):
    if request.POST or None:
        cur_bid = Bid.objects.get(id=bid_pk)
        cur_bid.accept_bid()
    else:
        return HttpResponse('Nothing here, return to main <a href="/mr/">page</a>')
    return HttpResponseRedirect('/mr/')


@permission_required('meeting_room.accept_decline_bid')
def decline_bid(request, bid_pk):
    if request.POST or None:
        cur_bid = Bid.objects.get(id=bid_pk)
        cur_bid.refuse_bid()
    else:
        return HttpResponse('Nothing here, return to main <a href="/mr/">page</a>')
    return HttpResponseRedirect('/mr/')


@login_required
def details(request, meeting_room_name):
    try:
        cur_meeting_room = MeetingRoom.objects.get(meeting_room_name=str(meeting_room_name))
    except MeetingRoom.DoesNotExist:
        return HttpResponse("<h1>Meeting room №" + str(meeting_room_name) + " not found</h1>")
    cur_meeting_room_bids = cur_meeting_room.all_bids(current_day_flag=True)
    if request.user.has_perm('meeting_room.change'):
        is_manager = True
    else:
        is_manager = False
    return render(request, 'meeting_room/meeting_room_details.html',
                  {'room': cur_meeting_room,
                   'bids': cur_meeting_room_bids,
                   'is_manager': is_manager},
                  )


def mr_login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'meeting_room/login.html', {'form': form})
    else:
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return HttpResponseRedirect('/mr')
            else:
                return render(request, 'meeting_room/login.html', {'form': form})
        else:
            return render(request, 'meeting_room/login.html', {'form': form})


def mr_logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/mr')


@login_required
def reserve_room(request, meeting_room_name=''):
    if request.method == 'GET':
        cur_meeting_room = MeetingRoom.objects.get(meeting_room_name=meeting_room_name)
        form = NewBid(
            initial={'meeting_room': cur_meeting_room,
                     'author': request.user
                     }
                      )
        return render(request, 'meeting_room/reserve_room.html', {'form': form})
    else:
        cur_form = NewBid(request.POST or None)
        if cur_form.is_valid():
            new_bid = cur_form.save(commit=False)
            new_bid.save()
            cur_meeting_room = new_bid.meeting_room
            form = NewBid(
                initial={'meeting_room': cur_meeting_room,
                         'author': request.user
                         }
            )
            return render(request, 'meeting_room/reserve_room.html', {'form': form})
        else:
            return render(request, 'meeting_room/reserve_room.html', {'form': cur_form})


@permission_required('meeting_room.change')
def customize_room(request, meeting_room_name):
    cur_meeting_room = MeetingRoom.objects.get(meeting_room_name=meeting_room_name)
    if request.method == 'GET':
        form = CustomizeRoom(instance=cur_meeting_room)
        return render(request, 'meeting_room/customize_room.html', {'form': form})
    else:
        cur_form = CustomizeRoom(request.POST or None, instance=cur_meeting_room)
        if cur_form.is_valid():
            cur_form.save()
            return HttpResponseRedirect('/mr/mr_{}/'.format(cur_meeting_room.meeting_room_name))
        else:
            return render(request, 'meeting_room/customize_room.html', {'form': cur_form})


@permission_required('auth.change_group')
def manage_users(request):
    manage_users_list = User.objects.filter(is_staff=False, is_active=True)
    cur_set = []
    for user in manage_users_list:
        if user != request.user:
            try:
                user.groups.get(name='managers')
                is_manager = True
            except Group.DoesNotExist:
                is_manager = False
            finally:
                cur_set.append((user, is_manager))
    cur_set = tuple(cur_set)
    return render(request, 'meeting_room/manage_users.html', {'cur_set': cur_set})


@permission_required('auth.change_group')
def group_add_member(request, user_id):
    chosen_user = User.objects.get(pk=user_id)
    group = Group.objects.get(name='managers')
    group.user_set.add(chosen_user)
    return HttpResponseRedirect('/mr/manage_users/')


@permission_required('auth.change_group')
def group_delete_member(request, user_id):
    chosen_user = User.objects.get(pk=user_id)
    group = Group.objects.get(name='managers')
    group.user_set.remove(chosen_user)
    return HttpResponseRedirect('/mr/manage_users/')
