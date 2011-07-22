#Wrote a separete function to be able to set another Exif parser in future
#if needed so without touching the main app code.
import EXIF

def get_exif(photo_path):
    data = EXIF.process_file(open(photo_path, 'rb'))
    return data

def get_exif_taken_date(photo_path):
    full_exif = get_exif(photo_path)
    taken_date_tuple=full_exif["EXIF DateTimeOriginal"]
    taken_date=taken_date_tuple.values
    return taken_date