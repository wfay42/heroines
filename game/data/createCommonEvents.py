import json

with open('CommonEvents.json', 'r') as fp:
    # common_events = json.load(fp)
    lines = fp.readlines()

with open('CommonEvents.json', 'r') as fp:
    input_common_events = json.load(fp)

# mapping of heroine name to their CommonEvent ID for their Naga event
# which we can use as an input
INPUT_EVENTS_MAPPING = {
    'eriko': 3,
    'hazel': 4,
    'maika': 5
}

input_eriko_event = input_common_events[INPUT_EVENTS_MAPPING['eriko']]
print(input_eriko_event)

with open('eriko.json', 'w') as fp:
    json.dump(input_eriko_event, fp, indent=2)

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

 .list[*] where .code = 313
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
"""

#

# hazel_line = eriko_line.replace('eriko', 'hazel').replace('Eriko', 'Hazel').replace('actor ID 1', 'actor ID 2')
# print(hazel_line)

# maika_line = eriko_line.replace('eriko', 'maika').replace('Eriko', 'Maika').replace('actor ID 1', 'actor ID 3')
# print(maika_line)
