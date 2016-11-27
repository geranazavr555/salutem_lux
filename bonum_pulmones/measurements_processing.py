import os

from salutem_lux import settings


def handle_uploaded_file(file, name):
    if not os.path.exists(settings.FILES_PATH):
        os.mkdir(settings.FILES_PATH)

    with open(os.path.join(settings.FILES_PATH, name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def process(filename):
    raise NotImplementedError
