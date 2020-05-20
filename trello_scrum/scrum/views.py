from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from trello import TrelloClient

# Create your views here.
def index(request):
    board_name = 'testing board'
    client = TrelloClient(
    api_key='7ff7c48b8ecd61cc9943424e203abc0c',
    token='a5a4cf8de49ddba93215be50a54f795e6a6511efd1139d5df7d1c3d12a18dcbe',
    )

    all_boards = client.list_boards()
    
    board = next(b for b in all_boards if b.name == board_name)

    try:
        board
    except UnboundLocalError:
        board = 'No board was found'

    #Initializes a dictionary and start each member of the board with 0 points
    employees_points = {}
    for member in board.get_members():
        employees_points[member.full_name] = 0

    lists = board.all_lists()
    #Instead of just removing the lists you should be able to choose which lists
    #to remove
    lists.pop(0)
    lists.pop(-1)

    #Creates a dictionary of lists that contains each a dictionary of employee : points
    employee_lists_points = {lists[0].name: employees_points}

    for x in range(1, len(lists)):
        employee_lists_points[lists[x].name] = employees_points.copy()

    print (f"the NEEEEEEW list: {employee_lists_points}")

    #create a list of a dictionary of employees points and copies one for each
    #list.
    employees_in_lists = [employees_points]
    for x in range(1, len(lists)):
        employees_in_lists.append(employees_points.copy())

    for lst in lists:
        cards = lst.list_cards()
        for card in cards:
            custom_fields = card.custom_fields
            if len(custom_fields) >= 0:
                points_field = None
                
                points_field = next(field for field in custom_fields 
                if field.name == 'POINTS')
                
                points = 0
                try:
                    points = int(points_field.value)
                except UnboundLocalError:
                    print('Theres no field called points')
                    points = -10000

                print(points)

                #Check the members that are assigned to a card
                for id in card.member_id:
                    employee = client.get_member(id)
                    this_dict = employee_lists_points[lst.name]
                    if employee.full_name in this_dict:
                        this_dict[employee.full_name] += int(points)
                        #print(f'{employee.full_name} tiene {this_dict[employee.full_name]}')
    
    print (f"the NEEEEEEW CHANGED list: {employee_lists_points}")
    total_points = []
    x = 0
    for lst in employee_lists_points:
        this_trello_list = employee_lists_points[lst]
        print(f"This is a list of the dict {this_trello_list}")
        total_points.append(0)
        for employee in this_trello_list:
            print(f"This is an employee of the dict {employee}")
            total_points[x] += this_trello_list[employee]
        x += 1

    print(f'puntos totales por lista {total_points}')

    total_points_dict = {}
    x = 0
    for lst in lists:
        total_points_dict[lst.name] = total_points[x]
        x+=1

    context = {
        'board_name': board.name,
        'lists': lists,
        'total_points_dict': total_points_dict
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