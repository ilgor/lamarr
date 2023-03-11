import in_place

with in_place.InPlace('templates/aws_creds.html') as file:
    for line in file:
        line = line.replace('action="/dev/', 'action="/')
        file.write(line)
