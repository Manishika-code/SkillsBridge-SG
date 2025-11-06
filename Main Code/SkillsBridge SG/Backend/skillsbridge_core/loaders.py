from .utils.data_fetcher import fetch_all_records
from .models import Course, CourseIGP, CourseIntake, GESRecord
import pdfplumber
import requests
from io import BytesIO
from rapidfuzz import process, fuzz
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pdfminer.high_level import extract_text

RESOURCE_ID_SP = "d_aa3b89617725a58af2587ccea25e6950"
RESOURCE_ID_NYP = "d_93384114c34e72d1cb7908b95618267a"
RESOURCE_ID_NP = "d_120ad7e0334d2c2a37ad62ae262f75fa"
RESOURCE_ID_TP = "d_fd432802d65c2b23a8e235be777780f7"
# note: RP's dataset is currently outdated, we can only get 2019
# if we want the latest one, we need to find a way to 
# parse in excel for this case
RESOURCE_ID_RP = "d_410aa9ff5ce5617a0cbebe9092c4a2e0"
RESOURCE_ID_GES = "d_3c55210de27fcccda2ed0c63fdd2b352"
RESOURCE_ID_INTAKE_BY_INST = "d_437e089ba21c5221b0d42e3b2636b7f0"
RESOURCE_ID_INTAKE_BY_COURSE_POLY = "d_6b264092cd066c55d8e2db9e68e7ffdb"
RESOURCE_ID_INTAKE_BY_COURSE_UNI = "d_78a8224856234eafbbc44d3d3edacd19"

NTU_IGP_URL = "https://www.ntu.edu.sg/docs/default-source/undergraduate-admissions/igp/ntu_igp.pdf?sfvrsn=5bf56f6c_1"

# custom titlecasing (specifically for NYP's since theirs
# is ALL CAPS for some reason)
import re


def load_intake_by_institution():
    """
    Load the past 5 years of student intake data by institution (gender-separated).
    Populates CourseIntake records with only institution-level aggregation
    (no course linkage).
    """
    print("📊 Loading intake by institution (gender-separated)...")

    records = fetch_all_records("d_437e089ba21c5221b0d42e3b2636b7f0")

    # Determine available years and select the most recent 5
    years = sorted(
        {int(r["year"]) for r in records if r.get("year") and r["year"].isdigit()},
        reverse=True,
    )
    recent_years = years[:5]
    print(f"📅 Importing last {len(recent_years)} years: {recent_years}")

    # Institution mapping (dataset uses abbreviations like 'nus', 'ntu' columns)
    inst_columns = {
        "nus": "National University of Singapore",
        "ntu": "Nanyang Technological University",
        "smu": "Singapore Management University",
        "sit": "Singapore Institute of Technology",
        "sutd": "Singapore University of Technology and Design",
        "suss": "Singapore University of Social Sciences",
    }

    # Build intermediate dictionary keyed by (year, institution)
    data = {}
    for rec in records:
        year = rec.get("year")
        if not year or not year.isdigit() or int(year) not in recent_years:
            continue
        year = int(year)
        sex = rec.get("sex", "").strip().upper()  # 'MF' or 'F'
        for key, inst_name in inst_columns.items():
            val = rec.get(key)
            if not val or not val.strip().isdigit():
                continue
            count = int(val.strip())
            data.setdefault((year, inst_name), {})[sex] = count

    imported = 0
    for (year, inst_name), sexes in data.items():
        total = sexes.get("MF", 0)
        female = sexes.get("F", 0)
        male = max(total - female, 0) if total else 0

        # Create or update aggregate intake record
        CourseIntake.objects.update_or_create(
            course=None,  # no specific course link
            institution=inst_name,  # ✅ store institution name
            year=year,
            defaults={
                "total_intake": total,
                "intl_pct": 0.0,  # not provided in dataset
                "male_pct": (male / total * 100) if total else 0,
                "female_pct": (female / total * 100) if total else 0,
                "source_url": "https://data.gov.sg/dataset/student-intake-by-institution-and-sex",
            },
        )
        imported += 1

    print(f"✅ Imported {imported} institution-level intake entries successfully.")

def load_intake_by_course(resource_id, level_label):
    """
    Load 5 years of course-level intake data (gender separated) from Data.gov.sg.
    """
    print(f"📊 Loading intake by course for {level_label.upper()} (last 5 years)...")

    records = fetch_all_records(resource_id)

    years = sorted({int(r["year"]) for r in records if r.get("year") and r["year"].isdigit()}, reverse=True)
    recent_years = years[:5]
    print(f"📅 Importing years: {recent_years}")

    data = {}
    for rec in records:
        year = rec.get("year")
        if not year or not year.isdigit() or int(year) not in recent_years:
            continue
        year = int(year)
        sex = rec.get("sex", "").strip().upper()
        course_raw = rec.get("course", "").strip()
        if not course_raw:
            continue
        intake = rec.get("intake")
        if not intake or not intake.strip().isdigit():
            continue
        intake = int(intake.strip())

        data.setdefault((year, course_raw), {})[sex] = intake

    imported, unmatched = 0, []

    for (year, cname), sexes in data.items():
        total = sexes.get("MF", 0)
        female = sexes.get("F", 0)
        male = max(total - female, 0) if total else 0

        # Clean course name
        course_name = (
            format_polytechnic_course(cname) if level_label == "poly"
            else format_degree_course(cname)
        )

        institution = (
            "Various Polytechnics" if level_label == "poly"
            else "Various Universities"
        )
        course = find_best_course_match(course_name, institution)
        if not course:
            unmatched.append(course_name)
            continue

        CourseIntake.objects.update_or_create(
            course=course,
            year=year,
            defaults={
                "total_intake": total,
                "male_pct": (male / total * 100) if total else 0,
                "female_pct": (female / total * 100) if total else 0,
                "intl_pct": 0.0,
            },
        )
        imported += 1

    print(f"✅ Imported {imported} {level_label.upper()} course intake records successfully.")
    if unmatched:
        print(f"⚠️ Skipped {len(unmatched)} unmatched courses.")
  
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

def load_ges_records():
    """
    Load the past 5 years of Graduate Employment Survey (GES) data
    from Data.gov.sg and store per-year trends in GESRecord.
    """
    print("📊 Importing Graduate Employment Survey (GES) data...")

    records = fetch_all_records(RESOURCE_ID_GES)

    # Extract valid years and select last 5
    years = sorted({int(rec["year"]) for rec in records if rec.get("year") and rec["year"].isdigit()}, reverse=True)
    if not years:
        print("⚠️ No valid GES year data found.")
        return

    recent_years = years[:5]
    print(f"📅 Importing GES data for years: {recent_years}")

    # Filter to recent years
    records = [r for r in records if int(r.get("year", 0)) in recent_years]

    imported, unmatched = 0, []

    for rec in records:
        course_name = format_degree_course(rec.get("degree", "").strip())
        institution = rec.get("university", "").strip()
        year = int(rec.get("year", 0))

        if not course_name or not institution or not year:
            continue

        # Match to an existing Course (more robust)
        course = find_best_course_match(course_name, institution)
        if not course:
            unmatched.append(course_name)
            continue

        # Extract stats safely
        try:
            emp_rate = float(rec.get("employment_rate_overall", 0)) or None
            median_salary = float(rec.get("basic_monthly_median", 0)) or None
        except (ValueError, TypeError):
            emp_rate, median_salary = None, None

        # Create/update GESRecord for this course/year
        GESRecord.objects.update_or_create(
            course=course,
            year=year,
            defaults={
                "employment_rate": emp_rate,
                "median_salary": median_salary,
                "source_url": "https://data.gov.sg/dataset/graduate-employment-survey",
            },
        )
        imported += 1

    print(f"✅ Imported {imported} GES entries across {len(recent_years)} years.")
    if unmatched:
        print(f"⚠️ Skipped {len(unmatched)} unmatched courses.")

def load_dataset_uni():
    records = fetch_all_records(RESOURCE_ID_GES)
    # filter to latest year 
    years = [int(rec["year"]) for rec in records if rec.get("year")]
    latest_year = max(years)
    print(latest_year)
    records = [rec for rec in records if int(rec["year"]) == latest_year]
    
    for rec in records:
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

def clean_gpa_value(value: str) -> str:
    """
    Cleans raw GPA values from PDF extraction.
    Converts things like '364' -> '3.64' or '3,85' -> '3.85'
    """
    if not value or value.strip() in {"-", "#", "N/A"}:
        return ""
    value = value.replace(",", ".").strip()

    # If it looks like '364' or '385', fix to '3.64' or '3.85'
    if re.match(r"^[34]\d{2}$", value):
        value = f"{value[0]}.{value[1:]}"
    elif re.match(r"^[34]\.\d{1,2}$", value):
        pass  # already fine
    elif not re.match(r"^[0-4]\.\d{1,2}$", value):
        # not a valid GPA
        return ""
    return value

def clean_alevel_value(value: str) -> str:
    """
    Cleans A-Level indicative grades (e.g. 'AAA/A', 'BBB/C', etc.)
    Removes stray characters and whitespace.
    """
    if not value or value.strip() in {"-", "#", "N/A"}:
        return ""
    value = re.sub(r"[^A-Z/]", "", value.strip().upper())
    return value


def normalize_name(name: str) -> str:
    if not name:
        return ""
    name = name.lower()

    # Expand common abbreviations
    replacements = {
        r'\bbeng\b': 'bachelor of engineering',
        r'\bbsc\b': 'bachelor of science',
        r'\bba\b': 'bachelor of arts',
        r'\bbba\b': 'bachelor of business administration',
        r'\b(hons?)\b': '',
        r'&': 'and',
        r'[\(\)\[\]\-/,]': ' ',
        r'\s+': ' '
    }
    for pattern, repl in replacements.items():
        name = re.sub(pattern, repl, name)

    # Remove generic words that don’t help
    stopwords = {'bachelor', 'of', 'with', 'honours', 'in', 'the', 'degree'}
    tokens = [w for w in name.split() if w not in stopwords]
    return " ".join(tokens).strip()

def find_best_course_match(course_name, institution, threshold=88, top_n=3):
    if not institution:
        print(f"⚠️ No institution provided for '{course_name}'. Skipping.")
        return None

    normalized_inst = normalize_name(institution)

    inst_aliases = {
        "national university of singapore": "NUS",
        "nanyang technological university": "NTU",
        "singapore management university": "SMU",
        "singapore institute of technology": "SIT",
        "singapore university of social sciences": "SUSS",
        "ngee ann polytechnic": "NP",
        "nanyang polytechnic": "NYP",
        "singapore polytechnic": "SP",
        "republic polytechnic": "RP",
        "temasek polytechnic": "TP",
        "various polytechnics": "POLY_GROUP",  
    }

    matched_inst = None
    for key, abbr in inst_aliases.items():
        if normalize_name(key) in normalized_inst or abbr.lower() in normalized_inst:
            matched_inst = key
            break


    if not matched_inst:
        print(f"⚠️ Unknown institution '{institution}'. Skipping '{course_name}'.")
        return None

    if matched_inst == "various polytechnics" or matched_inst == "POLY_GROUP":
        poly_insts = [
            "ngee ann polytechnic",
            "nanyang polytechnic",
            "singapore polytechnic",
            "republic polytechnic",
            "temasek polytechnic",
        ]
        all_courses = Course.objects.filter(
            institution__in=[p.title() for p in poly_insts]
        )
    else:
        all_courses = Course.objects.filter(institution__icontains=matched_inst)

    if not all_courses.exists():
        print(f"⚠️ No courses found for {matched_inst}.")
        return None

    target = normalize_name(course_name)
    target_tokens = set(target.split())

    results = []
    for c in all_courses:
        db_name = normalize_name(c.course_name)
        db_inst = normalize_name(c.institution)

        # Fuzzy similarity
        score_name = fuzz.token_set_ratio(target, db_name)
        score_inst = fuzz.partial_ratio(normalized_inst, db_inst)

        # Weighted keyword match for core discipline words
        overlap_tokens = target_tokens & set(db_name.split())
        keyword_score = len(overlap_tokens) / max(len(target_tokens), 1) * 100

        # Combine (heavier weight to name similarity)
        final_score = 0.85 * score_name + 0.15 * score_inst + 0.10 * keyword_score
        results.append((final_score, c.course_name, c))

    results.sort(key=lambda x: x[0], reverse=True)

    # Major conflict filter (optional)
    professional_majors = {"medicine", "law", "dentistry", "pharmacy", "nursing", "economics"}
    target_majors = {k for k in professional_majors if k in target}

    def is_conflict(name):
        found = {k for k in professional_majors if k in normalize_name(name)}
        return target_majors and found.isdisjoint(target_majors)

    for i, (score, name, obj) in enumerate(results[:top_n], start=1):
        if score < threshold:
            continue
        if is_conflict(name):
            print(f"🚫 [{matched_inst}] Rejected [{score:.1f}%] '{course_name}' → '{name}' (major mismatch)")
            continue
        print(f"[{score:.1f}%] ✅ [{matched_inst}] Using option {i}: '{course_name}' → {name}")
        return obj

    print(f"⚠️ [{matched_inst}] All top {top_n} matches failed for '{course_name}'. Best was {results[0][1]} ({results[0][0]:.1f}%).")
    return None


def load_ntu_igp():
    """
    Parse the NTU AY2024/25 IGP PDF.
    Extracts A-Level, Polytechnic GPA, and Placement data into Course and CourseIGP tables.
    """
    institution = "Nanyang Technological University"
    PDF_URL = NTU_IGP_URL
    source_url = PDF_URL

    print(f"📄 Loading NTU IGP data from {source_url} ...")

    # Record containers
    records_alevel = {}
    records_poly = {}
    records_places = {}

    # --- Download PDF ---
    response = requests.get(PDF_URL)
    response.raise_for_status()

    with pdfplumber.open(BytesIO(response.content)) as pdf:
        current_table = None

        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""

            # Detect table section by header text
            if "Table 1" in text:
                current_table = "alevel"
            elif "Table 2" in text:
                current_table = "poly"
            elif "Table 3" in text:
                current_table = "places"

            tables = page.extract_tables()
            if not tables or not current_table:
                continue

            for table in tables:
                for row in table:
                    if not row:
                        continue

                    course_raw = (row[0] or "").strip()
                    if not course_raw or "NTU Programmes" in course_raw:
                        continue

                    if re.match(r"^[-\s]+$", course_raw):
                        continue

                    course_name = format_degree_course(course_raw)

                    # --- Table 1: A-Level ---
                    if current_table == "alevel" and len(row) >= 3:
                        tenth = clean_alevel_value(row[1] or "")
                        ninetieth = clean_alevel_value(row[2] or "")
                        if tenth or ninetieth:
                            records_alevel[course_name] = {"10th": tenth, "90th": ninetieth}

                    # --- Table 2: Polytechnic GPA ---
                    elif current_table == "poly" and len(row) >= 3:
                        tenth = clean_gpa_value(row[1] or "")
                        ninetieth = clean_gpa_value(row[2] or "")
                        if tenth or ninetieth:
                            records_poly[course_name] = {"10th": tenth, "90th": ninetieth}

        # --- Table 3: Placement fallback using raw text ---
        print("📊 Extracting placement data from text (fallback)...")
        for page in pdf.pages:
            text = page.extract_text() or ""
            if "Places taken up" not in text:
                continue

            lines = [l.strip() for l in text.splitlines() if l.strip()]
            current_college = None

            for line in lines:
                # Detect college headers like "College of Engineering"
                if line.lower().startswith("college of") or line.lower().startswith("school of") or line.lower().startswith("nanyang"):
                    current_college = line
                    continue

                # Match lines like "Aerospace Engineering 108"
                m = re.match(r"^(.+?)\s+(\d{2,4})$", line)
                if m:
                    course_name = format_degree_course(m.group(1))
                    num = int(m.group(2))
                    records_places[course_name] = {
                        "placements": num,
                        "college": current_college
                    }

    # --- Debug summary ---
    print(f"✅ Found {len(records_alevel)} A-Level, {len(records_poly)} Polytechnic, and {len(records_places)} placement entries.")
    for k, v in list(records_places.items())[:10]:
        print(f"  {k}: {v}")

    # --- Merge and Save ---
    all_courses = set(records_alevel.keys()) | set(records_poly.keys()) | set(records_places.keys())
    imported, unmatched = 0, []

    for course_name in all_courses:
        alevel = records_alevel.get(course_name)
        poly = records_poly.get(course_name)
        place_entry = records_places.get(course_name, {})
        placements = place_entry.get("placements")
        college = place_entry.get("college")

        course = find_best_course_match(course_name, institution)
        if not course:
            unmatched.append(course_name)
            print(f"⚠️ Skipping unmatched: {course_name}")
            continue
        else:
            print(f"✅ Matched {course_name} → {course.course_name}")

        # --- A-Level record ---
        if alevel:
            alevel_text = f"{alevel['10th']} – {alevel['90th']}".replace("– –", "").strip(" –")
            CourseIGP.objects.update_or_create(
                course=course,
                qualification="alevel",
                defaults={
                    "indicative_grade": alevel_text or "N/A",
                    "grade_type": "Rank Points",
                    "source_url": source_url,
                    "placements": placements,
                },
            )

        # --- Polytechnic record ---
        if poly:
            poly_text = f"{poly['10th']} – {poly['90th']}".replace("– –", "").strip(" –")
            CourseIGP.objects.update_or_create(
                course=course,
                qualification="poly",
                defaults={
                    "indicative_grade": poly_text or "N/A",
                    "grade_type": "GPA",
                    "source_url": source_url,
                    "placements": placements,
                },
            )

        imported += 1

    # --- Final summary ---
    print(f"✅ Imported {imported} NTU course records successfully.")
    if unmatched:
        print(f"⚠️ Skipped {len(unmatched)} unmatched:")
        for u in unmatched:
            print(f"  - {u}")

def load_nus_igp(html_path):
    institution = "National University of Singapore"
    source_url = "https://www.nus.edu.sg/oam/admissions/indicative-grade-profile"
    print(f"📄 Loading NUS IGP from {html_path}")

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    records_alevel = {}
    records_poly = {}
    records_places = {}  # <-- new

    tables = soup.find_all("table")
    for tbl in tables:
        caption = tbl.find_previous("p")
        caption_text = caption.get_text(strip=True).lower() if caption else ""

        if "a-level" in caption_text:
            current = "alevel"
        elif "polytechnic" in caption_text:
            current = "poly"
        elif "places" in caption_text or "taken up" in caption_text:
            current = "places"
        else:
            continue

        current_faculty = None
        for row in tbl.find_all("tr"):
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) == 1 and cols[0] == "":
                continue

            # Faculty header row
            if len(cols) == 1 or (len(cols) == 3 and cols[1] == "" and cols[2] == ""):
                text = cols[0].replace("\n", " ").strip()
                if text:
                    current_faculty = text
                continue

            if len(cols) < 2:
                continue

            # --- A-Level and Poly tables ---
            if current in ["alevel", "poly"] and len(cols) >= 3:
                course_name, tenth, ninetieth = cols[0], cols[1], cols[2]
                if not course_name or "programme" in course_name.lower():
                    continue

                clean_name = format_degree_course(course_name)

                if current == "alevel":
                    records_alevel[clean_name] = {"10th": tenth, "90th": ninetieth}
                elif current == "poly":
                    records_poly[clean_name] = {"10th": tenth, "90th": ninetieth}

            # --- Placement table ---
            elif current == "places" and len(cols) >= 2:
                course_name = cols[0].strip()
                num_str = cols[1].strip().replace(",", "")
                if not course_name or not num_str.isdigit():
                    continue
                clean_name = format_degree_course(course_name)
                records_places[clean_name] = int(num_str)

    print(f"Parsed {len(records_alevel)} A-Level, {len(records_poly)} Polytechnic, and {len(records_places)} placement entries")

    # --- Merge & Save ---
    all_courses = set(records_alevel.keys()) | set(records_poly.keys()) | set(records_places.keys())
    unmatched = []

    for cname in all_courses:
        course = find_best_course_match(cname, institution)
        placements = records_places.get(cname)
        if not course:
            unmatched.append(cname)
            continue

        # --- A-Level ---
        if cname in records_alevel:
            v = records_alevel[cname]
            igp_str = f"{v['10th']}".strip(" –")
            CourseIGP.objects.update_or_create(
                course=course,
                qualification="alevel",
                defaults={
                    "indicative_grade": igp_str,
                    "grade_type": "Rank Points",
                    "source_url": source_url,
                    "placements": placements,
                },
            )

        # --- Polytechnic ---
        if cname in records_poly:
            v = records_poly[cname]
            igp_str = f"{v['10th']}".strip(" –")
            CourseIGP.objects.update_or_create(
                course=course,
                qualification="poly",
                defaults={
                    "indicative_grade": igp_str,
                    "grade_type": "GPA",
                    "source_url": source_url,
                    "placements": placements,
                },
            )

    print(f"Imported {len(all_courses) - len(unmatched)} successfully.")
    if unmatched:
        print(f"Skipped {len(unmatched)} unmatched:")
        for u in unmatched:
            print("  -", u)

def load_smu_igp(html_path):
    """
    Parse SMU Indicative Grade Profile (IGP) data for both
    A-Level (letter grades) and Polytechnic GPA applicants,
    including placement counts.
    """
    institution = "Singapore Management University"
    source_url = "https://admissions.smu.edu.sg/admissions-requirements/indicative-grade-profile"

    print(f"📄 Loading SMU IGP data from {html_path} ...")

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    tables = soup.find_all("table")

    records_alevel = {}
    records_poly = {}
    records_places = {}

    # --- TABLE 1: A-Level grades (letter form) ---
    for tbl in tables:
        caption = tbl.find_previous("p")
        caption_text = caption.get_text(strip=True).lower() if caption else ""
        if "a-level" not in caption_text:
            continue

        rows = tbl.find_all("tr")[1:]  # skip header
        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) < 3:
                continue
            course_name, tenth, ninetieth = cols[0], cols[1], cols[2]
            if not course_name or "programme" in course_name.lower():
                continue
            clean_name = format_degree_course(course_name)
            records_alevel[clean_name] = {"10th": tenth, "90th": ninetieth}

    # --- TABLE 2: Polytechnic GPA ---
    for tbl in tables:
        caption = tbl.find_previous("p")
        caption_text = caption.get_text(strip=True).lower() if caption else ""
        if "polytechnic" not in caption_text:
            continue

        rows = tbl.find_all("tr")[1:]
        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) < 3:
                continue
            course_name, tenth, ninetieth = cols[0], cols[1], cols[2]
            if not course_name or "programme" in course_name.lower():
                continue
            clean_name = format_degree_course(course_name)
            records_poly[clean_name] = {"10th": tenth, "90th": ninetieth}

    # --- TABLE 3: Placements ---
    for tbl in tables:
        caption = tbl.find_previous("p")
        caption_text = caption.get_text(strip=True).lower() if caption else ""
        if "places" not in caption_text and "taken up" not in caption_text:
            continue

        for row in tbl.find_all("tr"):
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) < 2:
                continue
            course_name = cols[0].strip()
            num_str = cols[1].strip().replace(",", "")
            if not course_name or not num_str.isdigit():
                continue
            clean_name = format_degree_course(course_name)
            records_places[clean_name] = int(num_str)

    print(f"Parsed {len(records_alevel)} A-Level, {len(records_poly)} Polytechnic, and {len(records_places)} placement entries")

    # --- Merge & Save ---
    all_courses = set(records_alevel.keys()) | set(records_poly.keys()) | set(records_places.keys())
    unmatched, imported = [], 0

    for cname in all_courses:
        course = find_best_course_match(cname, institution)
        if not course:
            unmatched.append(cname)
            continue

        placements = records_places.get(cname)

        # --- A-Level (letter grades) ---
        if cname in records_alevel:
            v = records_alevel[cname]
            igp_str = f"{v['10th']}".strip(" –")
            CourseIGP.objects.update_or_create(
                course=course,
                qualification="alevel",
                defaults={
                    "indicative_grade": igp_str,
                    "grade_type": "Rank Points",
                    "source_url": source_url,
                    "placements": placements,
                },
            )

        # --- Polytechnic (GPA) ---
        if cname in records_poly:
            v = records_poly[cname]
            igp_str = f"{v['10th']}".strip(" –")
            CourseIGP.objects.update_or_create(
                course=course,
                qualification="poly",
                defaults={
                    "indicative_grade": igp_str,
                    "grade_type": "GPA",
                    "source_url": source_url,
                    "placements": placements,
                },
            )

        imported += 1

    print(f"✅ Imported {imported} SMU course entries successfully.")
    if unmatched:
        print(f"⚠️ Skipped {len(unmatched)} unmatched:")
        for u in unmatched:
            print("  -", u)

def extract_placement_from_row(flat_text):
    # Remove commas
    merged = flat_text.replace(",", "")
    
    # Only join split digits like "1 81" but NOT "181 94"
    merged = re.sub(r"(\d)\s(?=\d\s|[0-9]$)", r"\1", merged)
    
    # Find all integers not part of % or $
    candidates = [
        int(x) for x in re.findall(r"\b\d+\b", merged)
        if not re.search(rf"{x}%", merged) and not re.search(rf"\${x}", merged)
    ]
    
    # Filter out unrealistic values (e.g. below 10 or above 1000)
    candidates = [x for x in candidates if 10 <= x <= 1000]
    
    if candidates:
        # Pick the one that looks like a placement count (usually highest)
        return max(candidates)
    return None


def load_sit_igp(pdf_path):
    institution = "Singapore Institute of Technology"
    source_url = "https://www.singaporetech.edu.sg/admissions/indicative-grade-profile"

    print(f"📄 Loading SIT IGP data from {pdf_path} ...")

    records = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Skip empty or header rows
                    if not row or not any(row): 
                        continue
                    # Find any row that starts with "B" (BEng, BSc, etc.)
                    if re.match(r"^(B[A-Z])", row[0].strip()):
                        course_name = " ".join(row[0].split())
                        # Clean row of extra columns
                        flat = [c.strip() if c else "" for c in row]

                        # Try to parse the next row if it's numeric (the IGP row)
                        if len(flat) >= 6:
                            merged_row_text = " ".join(flat)
                            placements = extract_placement_from_row(merged_row_text)
                            
                            # Employment rate (last % before $)
                            percents = re.findall(r"\d+(?:\.\d+)?%", merged_row_text)
                            employment = percents[-1] if percents else None
                            
                            # Salary
                            m = re.search(r"\$[\d,]+", merged_row_text)
                            salary = m.group(0) if m else None
                            
                            # IGP (first 4 percentages)
                            igp_data = ", ".join(percents[:4]) if percents else "N/A"
                            
                            records.append({
                                "course_name": course_name,
                                "igp_data": igp_data,
                                "placements": placements,
                                "employment": employment,
                                "salary": salary
                            })

    print(f"✅ Extracted {len(records)} course rows from PDF.")

    # Verify sample output
    for r in records[:5]:
        print(r)

    print(f"✅ Parsed {len(records)} course entries.")

    imported, unmatched = 0, []
    for rec in records:
        cname = rec["course_name"]
        course = find_best_course_match(cname, institution)
        if not course:
            unmatched.append(cname)
            continue

        CourseIGP.objects.update_or_create(
            course=course,
            qualification="poly",
            defaults={
                "indicative_grade": "view on website",#["igp_data"] or "Not available",
                "grade_type": "GPA",
                "placements": rec["placements"],
                "source_url": source_url,
            },
        )
        imported += 1

    print(f"Imported {imported} courses successfully.")
    if unmatched:
        print(f"⚠️ Skipped {len(unmatched)} unmatched:")
        for u in unmatched:
            print(f"  - {u}")

def load_all():
    load_dataset_sp() 
    load_dataset_nyp()
    load_dataset_np()
    load_dataset_tp()
    load_dataset_rp()
    load_dataset_uni()
    load_intake_by_institution()
    load_ges_records()

