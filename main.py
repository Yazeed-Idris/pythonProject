import math
import requests

while True:
    def convert_to_hours(number):
        hours = int(math.floor(number / 60))
        minutes = number % 60
        hours_str = str(hours).zfill(2)
        minutes_str = str(minutes).zfill(2)
        return '{0}:{1}'.format(str(hours_str), str(minutes_str))


    print('Choose day by typing the number below')
    print('1. Sunday')
    print('2. Monday')
    print('3. Tuesday')
    print('4. Wednesday')
    print('5. Thursday')
    day_choice = int(input('Day: '))
    if day_choice == 1:
        day_choice = 'Sunday'
        day = 'U'
    elif day_choice == 2:
        day_choice = 'Monday'
        day = 'M'
    elif day_choice == 3:
        day_choice = 'Tuesday'
        day = 'T'
    elif day_choice == 4:
        day_choice = 'Wednesday'
        day = 'W'
    elif day_choice == 5:
        day_choice = 'Thursday'
        day = 'R'

    building = input('Input building number: ')
    time_range = input('Input start and finish time separated by "-" (E.g "1215-1300"): ')
    start_range = time_range[0:4]
    end_range = time_range[5:]
    rooms_dict = {}
    departments = [
        "ACFN",
        "AE",
        "ARE",
        "ARC",
        "MBA",
        "CHE",
        "CHEM",
        "CRP",
        "CE",
        "COE",
        "CEM",
        "CIE",
        "EE",
        "ELD",
        "ELI",
        "ERTH",
        "GS",
        "SE",
        "ICS",
        "ISOM",
        "IAS",
        "LS",
        "MGT",
        "MSE",
        "MATH",
        "ME",
        "CPG",
        "PETE",
        "PE",
        "PHYS",
        "PSE"
    ]

    start_range = (int(start_range[0:2]) * 60) + int(start_range[2:])
    end_range = (int(end_range[0:2]) * 60) + int(end_range[2:])

    for code in departments:
        print(f'Loading room numbers for {code}...')
        r = requests.get('https://registrar.kfupm.edu.sa/api/course-offering?term_code=202120&department_code=' + code)
        data = r.json()['data']
        for x in data:
            course_day = str(x['class_days']).upper().find(day)
            start_time = x['start_time']
            end_time = x['end_time']
            section_building = x['building']
            room = x['room']

            if str(building) == str(section_building):
                if course_day >= 0:
                    if str(room) not in rooms_dict.keys():
                        rooms_dict[str(room)] = [(start_time, end_time, 1)]
                    else:
                        rooms_dict[str(room)].append((start_time, end_time, 1))
                else:
                    if str(room) not in rooms_dict.keys():
                        rooms_dict[str(room)] = [(start_time, end_time, -1)]
                    else:
                        rooms_dict[str(room)].append((start_time, end_time, -1))
    available_rooms = {}
    for room_no, times in rooms_dict.items():
        flag = True
        for time in times:
            start_time = time[0]
            end_time = time[1]
            if start_time is not None and end_time is not None:
                start_time = (int(start_time[0:2]) * 60) + int(start_time[2:])
                end_time = (int(end_time[0:2]) * 60) + int(end_time[2:])
                if time[2] == 1:
                    if not (end_time - start_range <= 0 or end_range - start_time <= 0):
                        flag = False
        if flag:
            available_rooms[str(room_no)] = room_no

    if len(available_rooms) <= 0:
        print('No available rooms.')
    else:

        print(
            f'Available rooms in building {building} from {convert_to_hours(start_range)} to {convert_to_hours(end_range)} on {day_choice} are:')
        mokdysrooms = []
        for room in available_rooms:
            mokdysrooms.append(room)
        mokdysrooms.sort()
        for room in mokdysrooms:
            print(room)
    search_again = input('Search again? (Y/N): ')
    if search_again == 'N' or search_again == 'n':
        break
