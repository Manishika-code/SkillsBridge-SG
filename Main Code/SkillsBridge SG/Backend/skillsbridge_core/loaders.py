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
RESOURCE_ID_GES = "d_3c55210de27fcccda2ed0c63fdd2b352"

# custom titlecasing (specifically for NYP's since theirs
# is ALL CAPS for some reason)
import re
import re

def format_polytechnic_course(name: str) -> str:
    """
    Clean and format Polytechnic course names.
    Example:
        'Cybersecurity & Digital Forensics (Nanyang Polytechnic)' ->
        'Diploma in Cybersecurity & Digital Forensics (Nanyang Polytechnic)'
    """
    if not name:
        return ""

    # Cleanup symbols and spaces
    name = re.sub(r"[*^#]+", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    name = re.sub(r"\(\s+", "(", name)
    name = re.sub(r"\s+\)", ")", name)

    # Extract institution
    institution = None
    match = re.search(r"\(([^)]+)\)$", name)
    if match:
        institution = match.group(1).strip()
        name = name[: match.start()].strip()

    # Add "Diploma in" if missing
    if not name.lower().startswith("diploma"):
        name = f"Diploma in {name}"

    # Capitalize nicely
    lowercase_words = {"in", "of", "and", "on", "at", "for", "to", "the", "with", "by"}
    acronyms = {"AI", "ICT", "IT", "NYP", "SP", "RP", "TP", "NP"}

    words = name.split()
    formatted = []
    for i, w in enumerate(words):
        if w.upper() in acronyms:
            formatted.append(w.upper())
        elif i != 0 and w.lower() in lowercase_words:
            formatted.append(w.lower())
        else:
            formatted.append(w.capitalize())

    formatted_name = " ".join(formatted)

    if institution:
        formatted_name += f" ({institution})"

    return formatted_name

def format_degree_course(name: str) -> str:
    """
    Clean and format University degree names.
    Example:
        'Mechanical Engineering (Nanyang Technological University)' ->
        'Bachelor of Engineering in Mechanical Engineering (Nanyang Technological University)'
    """
    if not name:
        return ""

    name = re.sub(r"[*^#]+", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    name = re.sub(r"\(\s+", "(", name)
    name = re.sub(r"\s+\)", ")", name)

    # Extract institution
    institution = None
    match = re.search(r"\(([^)]+)\)$", name)
    if match:
        institution = match.group(1).strip()
        name = name[: match.start()].strip()

    # Skip if already has full degree prefix
    if re.match(r"^(bachelor|b\.)", name.lower()):
        formatted_name = name
    else:
        # Guess degree type
        course_lower = name.lower()
        if any(word in course_lower for word in ["engineering", "mechanical", "civil", "electrical", "aerospace", "chemical", "biomedical", "marine"]):
            degree_type = "Engineering"
        elif any(word in course_lower for word in ["computing", "computer", "information", "data", "ai", "ict", "infocomm"]):
            degree_type = "Computing"
        elif any(word in course_lower for word in ["business", "accountancy", "economics", "finance", "marketing", "management"]):
            degree_type = "Business"
        elif any(word in course_lower for word in ["design", "art", "media", "communication"]):
            degree_type = "Arts"
        elif any(word in course_lower for word in ["science", "physics", "chemistry", "biology", "mathematics", "nursing", "therapy"]):
            degree_type = "Science"
        else:
            degree_type = None

        if degree_type:
            formatted_name = f"Bachelor of {degree_type} in {name}"
        else:
            formatted_name = f"Bachelor of {name}"

    # Capitalize properly
    lowercase_words = {"in", "of", "and", "on", "at", "for", "to", "the", "with", "by"}
    acronyms = {"AI", "ICT", "IT", "NTU", "NUS", "SIT", "SMU", "SUSS"}

    words = formatted_name.split()
    formatted = []
    for i, w in enumerate(words):
        if w.upper() in acronyms:
            formatted.append(w.upper())
        elif i != 0 and w.lower() in lowercase_words:
            formatted.append(w.lower())
        else:
            formatted.append(w.capitalize())

    formatted_name = " ".join(formatted)

    if institution:
        formatted_name += f" ({institution})"

    return formatted_name

def load_dataset_sp():
    records = fetch_all_records(RESOURCE_ID_SP)
    for rec in records:
        Course.objects.update_or_create(
            course_code = rec.get("course_code"),
            institution = "Singapore Polytechnic",
            defaults = {
                "course_name": format_polytechnic_course(rec.get("course_name")),
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
                "course_name": format_polytechnic_course(rec.get("course_name")),
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
                "course_name": format_polytechnic_course(rec.get("course_name")),
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
                "course_name": format_polytechnic_course(rec.get("course_name")),
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
                "course_name": format_polytechnic_course(rec.get("course_name")),
                "url": rec.get("reference"),
                "school": rec.get("school"), 
            },
        )


def load_dataset_uni():
    records = fetch_all_records(RESOURCE_ID_GES)
    # filter to latest year 
    years = [int(rec["year"]) for rec in records if rec.get("year")]
    latest_year = max(years)
    print(latest_year)
    records = [rec for rec in records if int(rec["year"]) == latest_year]
    
    for rec in records:
        print(rec)
        Course.objects.update_or_create(
            course_name = format_degree_course(rec.get("degree")),
            institution = rec.get("university"),
            defaults={
                "school": rec.get("school"),
                "employment_rate": rec.get("employment_rate_overall"),
                "median_salary": rec.get("basic_monthly_median"),
                "level": "uni"
            },
        )



def load_all():
    load_dataset_sp() 
    load_dataset_nyp()
    load_dataset_np()
    load_dataset_tp()
    load_dataset_rp()
    load_dataset_uni()

