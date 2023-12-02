import json

with open('CommonEvents.json', 'r') as fp:
    # common_events = json.load(fp)
    lines = fp.readlines()

with open('CommonEvents.json', 'r') as fp:
    input_common_events = json.load(fp)

# mapping of heroine name to their CommonEvent ID for their Naga event
# which we can use as an input
INPUT_EVENTS_MAPPING = {
    'eriko-naga': 3,
    'hazel-naga': 4,
    'maika-naga': 5,

    'eriko-wolf': 9,
    'hazel-wolf': 10,
    'maika-wolf': 11,
}

STATE_MAPPING = {
    'Naga': 12,
    'Naga Confusion': 13,
    'Wolf': 14,
    'Wolf Confusion': 15
}

def replace_naga_portrait_string(input):
    return input.replace('-naga-bitten-03c', '-wolf-01'
        ).replace('-naga-bitten-03d', '-wolf-02'
        ).replace('-naga-bitten-04c', '-wolf-03'
        ).replace('-naga-bitten-05', '-wolf-04')

## Do straight string manipulation
def string_manip():
    eriko_line = lines[4]
    eriko_new_line = replace_naga_portrait_string(eriko_line)
    with open('eriko-strreplace.json', 'w') as fp:
        fp.write(eriko_new_line)

def get_new_state(input_state):
    output_state = input_state
    if input_state == STATE_MAPPING['Naga']:
        output_state = STATE_MAPPING['Wolf']
    elif input_state == STATE_MAPPING['Naga Confusion']:
        output_state = STATE_MAPPING['Wolf Confusion']
    return output_state

def is_state_conditional(parameters):
    # p[0] == 4 means Actor is being inspected
    # p[2] == 6 means State is what is being compared
    return parameters[0] == 4 and parameters[2] == 6

def update_affected_by(event_item_parameters_list):
    """
    Updates the conditional parameter list for 'if character affected by <state>'
    event_item_parameters_list is updated and returned
    """

    # only operate on conditionals around State
    if not is_state_conditional(event_item_parameters_list):
        return

    input_state = event_item_parameters_list[3]
    output_state = get_new_state(input_state)
    event_item_parameters_list[3] = output_state
    return event_item_parameters_list

def is_variable_conditional(parameters):
    # p[0] == 1 means the condition is on Variable
    return parameters[0] == 1

def update_monster_level(event_item_parameters_list):
    """
    Updates the conditional parameter list for 'if character's monster level = [1,2,3,4]'
    event_item_parameters_list is updated and returned
    """
    if not is_variable_conditional(event_item_parameters_list):
        return

    input_var = event_item_parameters_list[1]
    # TODO: only works going from Naga to Wolf
    output_var = input_var + 5
    event_item_parameters_list[1] = output_var
    return event_item_parameters_list



def update_change_state(event_item_parameters_list):
    input_state = event_item_parameters_list[3]
    output_state = get_new_state(input_state)
    event_item_parameters_list[3] = output_state
    return event_item_parameters_list

def update_battle_portrait_357(event_item_parameters_list):
    obj = event_item_parameters_list[3]
    value = obj['Filename:str']
    new_value = replace_naga_portrait_string(value)
    obj['Filename:str'] = new_value

def update_battle_portrait_657(event_item_parameters_list):
    value = event_item_parameters_list[0]
    new_value = replace_naga_portrait_string(value)
    event_item_parameters_list[0] = new_value

def walk_event_list(input_event):
    """
    This walks through the list of actions in a CommonEvent and alters the steps as needed
    """
    event_list = input_event.get('list')
    for event_item in event_list:
        if event_item['code'] == 111:
            # should find the state for Naga and replace with Wolf
            update_affected_by(event_item['parameters'])
            update_monster_level(event_item['parameters'])
        elif event_item['code'] == 313:
            # change state
            update_change_state(event_item['parameters'])
        elif event_item['code'] == 357:
            # update the Battle Portrait. Need to go nested a bit
            update_battle_portrait_357(event_item['parameters'])
        elif event_item['code'] == 657:
            # the other place to update Battle Portrait. Nested differently
            update_battle_portrait_657(event_item['parameters'])

    input_name = input_event['name']
    input_event['name'] = input_name.replace('Naga', 'Wolf')
    return input_event


input_eriko_event = input_common_events[INPUT_EVENTS_MAPPING['eriko-wolf']]
print(input_eriko_event)

output_eriko_event = walk_event_list(input_common_events[INPUT_EVENTS_MAPPING['eriko-wolf']])
walk_event_list(input_common_events[INPUT_EVENTS_MAPPING['hazel-wolf']])
walk_event_list(input_common_events[INPUT_EVENTS_MAPPING['maika-wolf']])

with open('eriko-new.json', 'w') as fp:
    json.dump(output_eriko_event, fp, indent=2)

with open('CommonsEvents_.json', 'w') as fp:
    json.dump(input_common_events, fp)

"""
Things to update
 .name = is "Naga Battle Eriko"
 .list[*] where .code = 357 (update portrait)
    .parameters[4]."Filename:str" - is "eriko-naga-bitten-03d"
    .parameters[4]."Targets:arraystr" -  "[\"actor ID 1\"]"
 .list[*] where .code = 657 (update portrait actor ID)
    .parameters[0] - "Filename = eriko-naga-bitten-03d"
 There must be something else to alter to say what is the input state (Naga),
 and also the output state (not Naga Confusion)
 Those may be array-index based and thus fragile to change.
 Maybe if I can key on it based on the "code" ?

 .list[*] where .code = 313 (Change State)
    .parameters - [0, 1, 0, 13]
    0 - "Fixed" instead of "Variable"
    1 - Character ID (1 being Eriko)
    0 - "Add" condition rather than Remove
    13 - condition to add. 13 is Naga Confusion
 .list[*] where .code = 111 is the conditional
     .parameters - [4, 1, 6, 12]
    4 - I guess this selects "Actor" on tab 2 as what the conditional is on
    1 - Character ID (1 being Eriko)
    6 - Conditional on "State" which is the 6th radio button
    12 - State ID 12 is "Naga"

 Naga Level variables are 2,3,4
 Wolf Level variables are 7,8,9
"""

#

# hazel_line = eriko_line.replace('eriko', 'hazel').replace('Eriko', 'Hazel').replace('actor ID 1', 'actor ID 2')
# print(hazel_line)

# maika_line = eriko_line.replace('eriko', 'maika').replace('Eriko', 'Maika').replace('actor ID 1', 'actor ID 3')
# print(maika_line)
