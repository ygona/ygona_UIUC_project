import json
from datetime import datetime, timedelta
from collections import defaultdict

# loads JSON data from file
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Task 1: Count how many people have completed each training
def count_completed_trainings(data):
    
    training_people_count = defaultdict(int)
    count = 0
    
    for person in data:
        single_training = {} #dict to save each unique training
        for training in person['completions']:
            training_name = training['name']
            completed_date = datetime.strptime(training['timestamp'], '%m/%d/%Y')

            #if training name is not present or training is completed on or before the expiry date add it to the dict
            if training_name not in single_training or datetime.strptime(single_training[training_name]['timestamp'], '%m/%d/%Y') < completed_date:
                single_training[training_name] = training

        for training in single_training.values():
            training_people_count[training['name']] += 1
    
    with open('output_task1.json', 'w') as f:
        json.dump(training_people_count, f, indent=4)


# Task 2: List of all people that completed a specified training in a given fiscal year
def completed_trainings_in_fiscal_year(data, trainings, fiscal_year):
    fiscal_start = datetime(fiscal_year - 1, 7, 1)
    fiscal_end = datetime(fiscal_year, 6, 30)
    
    training_people = defaultdict(list)
    
    for person in data:
        for training in person['completions']:
            name = training['name']
            completed_date = datetime.strptime(training['timestamp'], '%m/%d/%Y')
            
            if name in trainings and fiscal_start <= completed_date <= fiscal_end:
                training_people[training['name']].append(person['name'])
    
    with open('output_task2.json', 'w') as f:
        json.dump(training_people, f, indent=4)

# Task 3: People with expired or soon-to-expire trainings based on a date
def find_expired_or_expiring_trainings(data, reference_date):
    ref_date = datetime.strptime(reference_date, '%Y-%m-%d')
    expiring_soon_days = ref_date + timedelta(days=30)
    
    people_with_expired_trainings = []
    
    for person in data:
        person_entry = {"name": person['name'], "trainings": []}
        single_training = {}
        for training in person['completions']:
            name = training['name']
            completed_date = datetime.strptime(training['timestamp'], '%m/%d/%Y')
            if name not in  single_training or datetime.strptime( single_training[name]['timestamp'], '%m/%d/%Y') < completed_date:
                 single_training[name] = training
        
        for training in  single_training.values():
            if training['expires']: #a check for expired or expiring soon trainings
                expiration_date = datetime.strptime(training['expires'], '%m/%d/%Y')
                if expiration_date < ref_date:
                    status =  "Expired"
                    
                elif ref_date <= expiration_date <= expiring_soon_days:
                    status = "Expires soon"
                else:
                    continue

                #output format in json file
                person_entry["trainings"].append({
                        "name": training['name'],
                        'completed_date': training['timestamp'],
                        'expiration_date': expiration_date.strftime('%m/%d/%Y'),
                        "status": status
                    })
        
        if person_entry['trainings']:
            people_with_expired_trainings.append(person_entry)
    
    with open('output_task3.json', 'w') as f:
        json.dump(people_with_expired_trainings, f, indent=4)


    

if __name__ == "__main__":
    data = load_data('trainings.txt')
    
    # Task 1: Count of people who completed trainings
    count_completed_trainings(data)
    
    # Task 2: Trainings completed in the specified fiscal year 
    trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    completed_trainings_in_fiscal_year(data, trainings, 2024)
    
    # Task 3: list of expired or expiring soon trainings
    find_expired_or_expiring_trainings(data, '2023-10-01')
    
