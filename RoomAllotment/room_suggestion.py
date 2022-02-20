


def assignRoomsBySeniority(applications, rooms):
    applications = sorted(applications, key = lambda a : (a.stdID.level, a.stdID.term, -a.RequestID))
    applications = reversed(applications)
    applications = list(applications)
    assignRooms(applications, rooms)
    return applications 

def assignRoomsByCgpa(applications, rooms):
    applications = sorted(applications, key = lambda a : (a.stdID.cgpa, -a.RequestID))
    applications = reversed(applications)
    applications = list(applications)
    assignRooms(applications, rooms)
    return applications

def assignRoomsByAddress(applications, rooms):
    applications = sorted(applications, key = lambda a : (1 if a.stdID.present_address != 'Dhaka' and a.stdID.permanent_address != 'Dhaka' else 0, -a.RequestID))
    applications = reversed(applications)
    applications = list(applications)
    assignRooms(applications, rooms)
    return applications

def assignRoomsByEca(applications, rooms):
    applications = sorted(applications, key = lambda a : (int(a.debate) + int(a.sports) + int(a.other), -a.RequestID))
    applications = reversed(applications)
    applications = list(applications)
    assignRooms(applications, rooms)
    return applications

def assignRooms(applications, rooms):
    for a in applications:
        a.possible_room_no = None

        for r in rooms:
            if r == a.requestedRoomNo and r.vacantSeats > 0:
                a.possible_room_no = r.RoomNo
                r.vacantSeats -= 1
                break

        if a.possible_room_no:
            continue

        for r in rooms:
            if r.vacantSeats > 0:
                a.possible_room_no = r.RoomNo
                r.vacantSeats -= 1
                break


        
    return 
