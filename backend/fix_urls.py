import os
import in_place


file_location_css = 'templates/static/css/'
files_css = os.listdir(file_location_css)

for file_name in files_css:
    with in_place.InPlace(f'{file_location_css}{file_name}') as file:
        for line in file:
            line = line.replace('url(/static', 'url(../../static')
            file.write(line)


file_location = 'templates/static/js/'
files = os.listdir(file_location)

for file_name in files:
    with in_place.InPlace(f'{file_location}{file_name}') as file:
        for line in file:
            line = line.replace('href="/', 'href="/dev/')
            line = line.replace('src="/', 'src="/dev/')
            line = line.replace('get("/', 'get("/dev/')
            file.write(line)

with in_place.InPlace('templates/index.html') as file:
    for line in file:
        line = line.replace('href="/', 'href="/dev/')
        line = line.replace('src="/', 'src="/dev/')
        file.write(line)

with in_place.InPlace('templates/aws_creds.html') as file:
    for line in file:
        line = line.replace('action="/', 'action="/dev/')
        file.write(line)
