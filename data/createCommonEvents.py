import json

with open('CommonEvents.json', 'r') as fp:
    # common_events = json.load(fp)
    lines = fp.readlines()

# print(common_events[3])
eriko_line = lines[4]
print(eriko_line)

hazel_line = eriko_line.replace('eriko', 'hazel').replace('Eriko', 'Hazel').replace('actor ID 1', 'actor ID 2')
print(hazel_line)

maika_line = eriko_line.replace('eriko', 'maika').replace('Eriko', 'Maika').replace('actor ID 1', 'actor ID 3')
print(maika_line)
