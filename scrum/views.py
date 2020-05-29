# Django dependencies
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

# External dependencies
from trello import TrelloClient
from trello import exceptions

# Project dependencies
from .scrum_member import ScrumMember

# Python dependencies
import copy
import datetime

# Create your views here.
def index(request):
    
    # We need to give users a way to change this, NO HARD CODE
    board_name: str = 'Goals & Tasks'
    client = TrelloClient(
    api_key='1c3f61d629a7c460858c84e3fdbc2de6',
    token='747a42d4a4391bba1eaaf4ec9dbf9eae499d5b97bc0b427fe7d40a87cf5415ef',
    )
    
    # The api has a number of maximum number of request you can make, this checks for that limit
    limit_reached: bool = False

    all_boards = client.list_boards()
    
    board = next(b for b in all_boards if b.name == board_name)

    try:
        board
    except UnboundLocalError:
        board = 'No board was found'
        print(board)


    all_lists = board.all_lists()
    #Instead of just removing the lists with the names here you should be able to choose which lists
    #to remove NO HARD CODE
    lists_to_track = [
        "Backlog To Do's (planeado para esta semana)", 
        "Doing (ya lo empece)", 
        "QA", 
        "Done"
    ]
    lists = []
    # We go through all the lists and only save the ones that match the name that was given to us
    for lst in all_lists:
        for name in lists_to_track:
            if (lst.name == name):
                lists.append(lst)
                break
    
    #Initializes a list of Scrum members that can have points based on the board members
    scrum_employees = []
    for member in board.get_members():
        scrum_employees.append(ScrumMember(client, member.id, member.full_name))
    
    #Initializes the points of the employees to 0 for each list
    for emp in scrum_employees:
        for lst in lists:
            emp.set_points(lst.name, 0)

    for lst in lists:
        try:
            cards = lst.list_cards()
        except exceptions.ResourceUnavailable:
            limit_reached = True
            break
        for card in cards:
            custom_fields = card.custom_fields
            if len(custom_fields) >= 0:
                points_field = None
                
                for field in custom_fields:
                    # ESTE FIELD NAME DEBERIA DE SER ELEGIDO POR EL USUARIO NO HARD CODED
                    if field.name == 'Puntos':
                        points_field = field
                
                points = 0
                try:
                    points = points_field.value

                except AttributeError:
                    print('Theres no field called points')
                    continue

                print(points)

                #Check the members that are assigned to a card
                for id in card.member_id:
                    employee = client.get_member(id)
                    #Add points to each member in the card based on this card's points
                    for scrum_emp in scrum_employees:
                        if(scrum_emp.full_name == employee.full_name):
                            scrum_emp.add_points(lst.name, points)
    
    for emp in scrum_employees:
        print(f'IM {emp.full_name} and here are my points {emp.points}')

    #Create dictionary of total points per trello list
    lists_total_points = {}
    x = 0
    for lst in lists:
        print(f'THE LIST {lst}')
        lists_total_points[lst.name] = 0
        for employee in scrum_employees:
            lists_total_points[lst.name] += employee.points[lst.name]
        x += 1

    print(f'puntos totales por lista {lists_total_points}')

    # A list containing just the names of each list without any more data
    lists_names = []
    for lst in lists:
        lists_names.append(lst.name)

    context = {
        'limit_reached': limit_reached,
        'board_name': board.name,
        'lists_names': lists_names,
        'employees': scrum_employees,
    }
    return render(request, 'scrum/index.html', context)



def etapa(request, list_name):

    board_name = 'testing board'
    client = TrelloClient(
    api_key='7ff7c48b8ecd61cc9943424e203abc0c',
    token='658c983f20351e7e441bac31ca229440040f3ae7a56fb44534c0c898763c85dc',
    )

    all_boards = client.list_boards()
    board = None

    for b in all_boards:
        if b.name == board_name:
            board = b
            break
    
    try:
        board
    except UnboundLocalError:
        board = 'No board was found'

    employees_points = {}
    for member in board.get_members():
        employees_points[member.full_name] = 0

    lists = board.all_lists()
    this_list = None
    for lst in lists:
        if lst.name == list_name:
            this_list = lst
    try:
        this_list
    except UnboundLocalError:
        this_list = "No list with matching name was found "

    cards = this_list.list_cards()
    for card in cards:
        if card.name.find('[') >= 0:
            splitted_card = card.name.split('[')
            points_array = splitted_card[1].split(']')
            points = points_array[0]
            print(points)
            try:
                int(points)
            except TypeError:
                print('The points where not parsed correctly')
                points = -10000
            for id in card.member_id:
                employee = client.get_member(id)
                if employee.full_name in employees_points:
                    employees_points[employee.full_name] += int(points)
                    #print(f'{employee.full_name} tiene {employees_points[employee.full_name]}')
                
    total_points = 0
    for employee in employees_points:
        total_points += employees_points[employee]

    print(f'puntos totales de la lista {total_points}')

    context = {
        'this_list': this_list,
        'total_points': total_points,
        'employees_points': employees_points

    }
    return render(request, 'scrum/etapa.html', context)

def member(request, member_name):
    board_name = 'testing board'
    client = TrelloClient(
    api_key='7ff7c48b8ecd61cc9943424e203abc0c',
    token='658c983f20351e7e441bac31ca229440040f3ae7a56fb44534c0c898763c85dc',
    )

    all_boards = client.list_boards()
    board = None

    for b in all_boards:
        if b.name == board_name:
            board = b
            break
    
    try:
        board
    except UnboundLocalError:
        board = 'No board was found'

    employee_points = 0

    lists = board.all_lists()
    lists.pop(0)
    lists.pop(-1)

    points_in_lists = []
    for x in range(len(lists)):
        points_in_lists.append(0)

    print(points_in_lists)

    x = 0
    for lst in lists:
        cards = lst.list_cards()
        for card in cards:
            if card.name.find('[') >= 0:
                splitted_card = card.name.split('[')
                points_array = splitted_card[1].split(']')
                points = points_array[0]
                print(points)
                try:
                    int(points)
                except TypeError:
                    print('The points where not parsed correctly')
                    points = -10000
                for id in card.member_id:
                    employee = client.get_member(id)
                    if employee.full_name == member_name:
                        points_in_lists[x] += int(points)
                        #print(f'{employee.full_name} tiene {points_in_lists[x]}')
        x += 1

    print(f'puntos totales por lista {points_in_lists}')

    total_points_dict = {}
    total_points = 0
    x = 0
    for lst in lists:
        total_points_dict[lst.name] = points_in_lists[x]
        total_points += points_in_lists[x]
        x+=1

    context = {
        'member_name': member_name,
        'total_points': total_points,
        'total_points_dict': total_points_dict
    }
    return render(request, 'scrum/member.html', context)