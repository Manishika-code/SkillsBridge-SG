from .utils.data_fetcher import fetch_all_records
from .models import Course

RESOURCE_ID_SP = "d_aa3b89617725a58af2587ccea25e6950"
RESOURCE_ID_NYP = "d_93384114c34e72d1cb7908b95618267a"
RESOURCE_ID_NP = "d_120ad7e0334d2c2a37ad62ae262f75fa"
RESOURCE_ID_TP = "d_fd432802d65c2b23a8e235be777780f7"
# note: RP's dataset is currently outdated, we can only get 2019
# if we want the latest one, we need to find a way to 
# parse in excel for this case
RESOURCE_ID_RP = "d_410aa9ff5ce5617a0cbebe9092c4a2e0"

# custom titlecasing (specifically for NYP's since theirs
# is ALL CAPS for some reason)
def format_course_name(name: str) -> str:
    if not name:
        return ""
    # Always lowercase first
    words = name.lower().split()
    
    # Words to keep lowercase unless first
    lowercase_words = {"in", "of", "and", "on", "at", "for", "to", "the"}
    acronyms = {"AI", "ICT", "IT"}
    
    formatted = []
    for i, w in enumerate(words):
        # Handle acronyms
        if w.upper() in acronyms:
            formatted.append(w.upper())
        # Keep "in", "of", etc. lowercase (unless first word)
        elif i != 0 and w in lowercase_words:
            formatted.append(w)
        else:
            formatted.append(w.capitalize())
    
    return " ".join(formatted)

def load_dataset_sp():
    records = fetch_all_records(RESOURCE_ID_SP)
    for rec in records:
        Course.objects.update_or_create(
            course_code = rec.get("course_code"),
            institution = "Singapore Polytechnic",
            defaults = {
                "course_name": format_course_name(rec.get("course_name")),
                "course_description": rec.get("course_description"),
                "url": rec.get("reference"),
                "school": rec.get("school"),
            },
        )

def load_dataset_nyp():
    records = fetch_all_records(RESOURCE_ID_NYP)
    for rec in records:
        Course.objects.update_or_create(
            course_code = rec.get("jae_course_code"),
            institution = "Nanyang Polytechnic",
            defaults = {
                "course_name": format_course_name(rec.get("course_name")),
                "url": rec.get("url"),
            },
        )

def load_dataset_np():
    records = fetch_all_records(RESOURCE_ID_NP)
    for rec in records:
        Course.objects.update_or_create(
            course_code = rec.get("course_code"),
            institution = "Ngee Ann Polytechnic",
            defaults = {
                "course_name": format_course_name(rec.get("course_name")),
                "course_description": rec.get("course_description"),
                "url": rec.get("reference"),
                "school": rec.get("school"),
            },
        )

def load_dataset_tp():
    records = fetch_all_records(RESOURCE_ID_TP)
    for rec in records:
        Course.objects.update_or_create(
            course_code = rec.get("moe_course_code"),
            institution = "Temasek Polytechnic",
            defaults = {
                "course_name": format_course_name(rec.get("course_name")),
                "course_description": rec.get("course_description"),
                "url": rec.get("reference"),
                "school": rec.get("school"),
            },
        )

def load_dataset_rp():
    records = fetch_all_records(RESOURCE_ID_RP)
    for rec in records:
        Course.objects.update_or_create(
            course_code = rec.get("course_code"),
            institution = "Republic Polytechnic",
            defaults = {
                "course_name": format_course_name(rec.get("course_name")),
                "url": rec.get("reference"),
                "school": rec.get("school"), 
            },
        )


def load_all():
    load_dataset_sp() 
    load_dataset_nyp()
    load_dataset_np()
    load_dataset_tp()
    load_dataset_rp()

