import io
import unicodedata

import fpdf
from fpdf.enums import XPos, YPos


class PDF(fpdf.FPDF):
    """
    A custom PDF class for generating a Harvard-style resume.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default font to Helvetica with UTF-8 support
        self.set_font("Helvetica", size=11)
        self.set_left_margin(20)
        self.set_right_margin(20)
        self.set_top_margin(15)
        self.set_auto_page_break(auto=True, margin=15)

    def add_line_break(self, height=5):
        """Add a line break with specified height."""
        self.ln(height)


def normalize_text(text):
    """
    Normalize Unicode text to ASCII equivalents for PDF compatibility.
    """
    if not text:
        return ""

    # Replace common Unicode characters with ASCII equivalents
    replacements = {
        "\u201c": '"',  # Left double quotation mark
        "\u201d": '"',  # Right double quotation mark
        "\u2018": "'",  # Left single quotation mark
        "\u2019": "'",  # Right single quotation mark
        "\u2013": "-",  # En dash
        "\u2014": "--",  # Em dash
        "\u2011": "-",  # Non-breaking hyphen
        "\u2026": "...",  # Horizontal ellipsis
        "\u00a0": " ",  # Non-breaking space
        "\u2022": "-",  # Bullet point
        "\u00b7": " - ",  # Middle dot (convert to dash with spaces)
        "\u00e9": "e",  # é (e with acute accent)
        "\u00ed": "i",  # í (i with acute accent)
        "\u00f1": "n",  # ñ (n with tilde)
        "\u00fc": "u",  # ü (u with diaeresis)
    }

    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)

    # Normalize remaining Unicode characters to closest ASCII equivalents
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if ord(c) < 128)

    return text


def parse_personal_info(personal_info_dict):
    """
    Parse the personal information string into components.
    Expected format: "Name | Address | Phone | Email"
    """
    # personal_info_dict = normalize_text(personal_info_dict)
    # parts = [part.strip() for part in personal_info_dict.split(" | ")]

    name = personal_info_dict.get("name")
    address = personal_info_dict.get("address")
    phone = personal_info_dict.get("phone")
    email = personal_info_dict.get("email")
    website = personal_info_dict.get("website")
    linkedin = personal_info_dict.get("linkedin")
    location = personal_info_dict.get("location")

    result = {"name": "", "address": "", "phone": "", "email": ""}

    if name:
        result["name"] = normalize_text(name)
    if address:
        result["name"] = normalize_text(address)
    if phone:
        result["phone"] = normalize_text(phone)
    if email:
        result["email"] = normalize_text(email)
    if location:
        result["location"] = normalize_text(location)
    if website:
        result["website"] = normalize_text(website)
    if linkedin:
        result["linkedin"] = normalize_text(linkedin)

    return result


def add_header(pdf_obj, personal_info):
    """
    Add the header section with name and contact information.
    """
    # Name (larger, bold, centered)
    pdf_obj.set_font("Helvetica", "B", size=16)
    pdf_obj.cell(
        0, 8, personal_info["name"], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C"
    )
    pdf_obj.add_line_break(2)

    # Contact information (smaller, centered)
    pdf_obj.set_font("Helvetica", size=10)
    contact_parts = []
    if personal_info["location"]:
        contact_parts.append(personal_info["location"])
    if personal_info["phone"]:
        contact_parts.append(personal_info["phone"])
    if personal_info["email"]:
        contact_parts.append(personal_info["email"])
    if personal_info["website"]:
        contact_parts.append(personal_info["website"])
    if personal_info["linkedin"]:
        contact_parts.append(personal_info["linkedin"])

    if contact_parts:
        contact_line = " | ".join(contact_parts)
        pdf_obj.cell(0, 5, contact_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf_obj.add_line_break(8)


def add_section_title(pdf_obj, title):
    """
    Add a section title with Harvard formatting.
    """
    pdf_obj.set_font("Helvetica", "B", size=12)
    pdf_obj.cell(0, 6, title.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Add underline
    pdf_obj.set_draw_color(0, 0, 0)
    pdf_obj.line(
        pdf_obj.get_x(),
        pdf_obj.get_y() - 1,
        pdf_obj.w - pdf_obj.r_margin,
        pdf_obj.get_y() - 1,
    )
    pdf_obj.add_line_break(3)


def add_simple_section(pdf_obj, title, items):
    """
    Add a simple section with bullet points (for skills, languages, interests, etc.).
    """
    if not items:
        return

    add_section_title(pdf_obj, title)
    pdf_obj.set_font("Helvetica", size=11)

    # Normalize items and join with bullet points
    normalized_items = [normalize_text(item) for item in items]
    bullet_items = " - ".join(normalized_items)
    pdf_obj.multi_cell(0, 5, bullet_items, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf_obj.add_line_break(5)


def add_education_section(pdf_obj, education_items):
    """
    Add the education section with Harvard formatting.
    """
    if not education_items:
        return

    add_section_title(pdf_obj, "Education")
    pdf_obj.set_font("Helvetica", size=11)

    for item in education_items:
        # Parse education string to extract components
        # Expected format examples:
        # "Trinity Washington University – Washington, DC – B.A. in Psychology (Anticipated Fall 2025)"
        # "Courses: City Seminar I & II, ..."

        if item.startswith("Courses:"):
            # Handle course listing
            pdf_obj.set_font("Helvetica", size=10)
            pdf_obj.multi_cell(
                0, 4, normalize_text(item), new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )
            pdf_obj.set_font("Helvetica", size=11)
        else:
            # Main education entry
            pdf_obj.set_font("Helvetica", "B", size=11)

            # Try to parse university, location, and degree info
            normalized_item = normalize_text(item)
            parts = normalized_item.split(" - ")
            if len(parts) >= 3:
                university = parts[0].strip()
                location = parts[1].strip()
                degree_info = " - ".join(parts[2:]).strip()

                # University and location on same line
                pdf_obj.cell(0, 5, university, new_x=XPos.RIGHT, new_y=YPos.TOP)
                pdf_obj.set_font("Helvetica", size=11)
                pdf_obj.cell(
                    0, 5, location, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R"
                )

                # Degree information
                pdf_obj.set_font("Helvetica", size=11)
                pdf_obj.multi_cell(
                    0, 5, degree_info, new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
            else:
                # Simple format
                pdf_obj.multi_cell(
                    0, 5, normalized_item, new_x=XPos.LMARGIN, new_y=YPos.NEXT
                )
                pdf_obj.set_font("Helvetica", size=11)

        pdf_obj.add_line_break(2)

    pdf_obj.add_line_break(3)


def add_experience_section(pdf_obj, experiences):
    """
    Add the experience section with Harvard formatting.
    """
    if not experiences:
        return

    add_section_title(pdf_obj, "Experience")

    for exp in experiences:
        # Job title and company (bold)
        pdf_obj.set_font("Helvetica", "B", size=11)
        job_title = exp.get(
            "name", ""
        )  # In the JSON, "name" appears to be the job title
        company = exp.get("position", "")  # "position" appears to be the company

        # Job title and company on left, dates on right
        job_company = (
            f"{job_title}, {company}" if job_title and company else job_title or company
        )
        job_company = normalize_text(job_company)
        pdf_obj.cell(0, 5, job_company, new_x=XPos.RIGHT, new_y=YPos.TOP)

        # Dates on the right
        start_date = normalize_text(exp.get("start_date", ""))
        end_date = normalize_text(exp.get("end_date", ""))
        date_range = f"{start_date} - {end_date}" if start_date and end_date else ""

        pdf_obj.set_font("Helvetica", size=11)
        pdf_obj.cell(0, 5, date_range, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

        # Job descriptions as bullet points
        pdf_obj.set_font("Helvetica", size=11)
        descriptions = exp.get("descriptions", [])
        for desc in descriptions:
            normalized_desc = normalize_text(desc)
            # Add bullet point with slight indentation
            pdf_obj.cell(8)  # Indentation
            pdf_obj.multi_cell(
                0, 5, f"- {normalized_desc}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )

        pdf_obj.add_line_break(4)

    pdf_obj.add_line_break(2)


def add_list_section(pdf_obj, title, items):
    """
    Add a section with a list of items (for projects, achievements, certifications).
    """
    if not items:
        return

    add_section_title(pdf_obj, title)
    pdf_obj.set_font("Helvetica", size=11)

    for item in items:
        normalized_item = normalize_text(item)
        pdf_obj.multi_cell(
            0, 5, f"- {normalized_item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )

    pdf_obj.add_line_break(5)


def add_about_section(pdf_obj, about_text):
    """
    Add the about/summary section.
    """
    if not about_text:
        return

    add_section_title(pdf_obj, "Summary")
    pdf_obj.set_font("Helvetica", size=11)
    normalized_about = normalize_text(about_text)
    pdf_obj.multi_cell(0, 5, normalized_about, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf_obj.add_line_break(5)


def create_resume_pdf(resume_data, output_filename="resume.pdf", output_buffer=False):
    """
    Generates a Harvard-style resume PDF from a dictionary of data.

    Args:
        resume_data (dict): A dictionary containing all the resume information.
        output_filename (str): The name of the output PDF file.
        output_buffer (bool): If True, return PDF as BytesIO buffer instead of saving to file.
    """
    # Create a new PDF document
    pdf = PDF()
    pdf.add_page()

    # Parse personal information
    personal_info = parse_personal_info(resume_data.get("personal_information", {}))

    # Add header with name and contact info
    add_header(pdf, personal_info)

    # Add about/summary section
    add_about_section(pdf, resume_data.get("about"))

    # Add education section
    add_education_section(pdf, resume_data.get("education", []))

    # Add experience section
    add_experience_section(pdf, resume_data.get("experiences", []))

    # Add skills section
    add_simple_section(pdf, "Skills", resume_data.get("skills", []))

    # Add certifications section
    add_list_section(pdf, "Certifications", resume_data.get("certifications", []))

    # Add projects section
    add_list_section(pdf, "Projects", resume_data.get("projects", []))

    # Add achievements section
    add_list_section(pdf, "Achievements", resume_data.get("achievements", []))

    # Add languages section
    add_simple_section(pdf, "Languages", resume_data.get("languages", []))

    # Add interests section
    add_simple_section(pdf, "Interests", resume_data.get("interests", []))

    # Output the PDF
    if output_buffer:
        # Create an in-memory buffer to store the PDF
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)  # Rewind the buffer to the beginning
        return pdf_buffer
    else:
        pdf.output(output_filename)
        print(f"Resume saved as {output_filename}")
        return None


# --- Sample usage with the provided JSON data ---
if __name__ == "__main__":
    # Sample data matching the JSON structure
    sample_data = {
        "personal_information": 'Natasha "NeNe" Gonzales | 125 Michigan Ave NE, Washington, DC 12984 | (757) 767‑8976 | n.gonzales@email.com',
        "skills": [
            "Fluent Spanish (verbal/written)",
            "Patient mobility assistance",
            "Behavioral intervention",
            "ADLs support",
            "CRM & documentation systems",
        ],
        "languages": ["English (native)", "Spanish (fluent)"],
        "interests": [
            "Psychosocial research",
            "Video game‑based therapy (exploring applications)",
            "Outdoor fitness & strength training",
        ],
        "about": "Empathetic and results‑driven care professional with a BA in Psychology (Anticipated Fall 2025) and extensive experience supporting the elderly, children with developmental disabilities, and individuals with complex needs. Proven ability to design and implement engaging activities, streamline processes, and improve client satisfaction using evidence‑based interventions. Fluent in Spanish and experienced in cross‑functional teamwork, I am eager to contribute to a forward‑thinking healthcare organization.",
        "experiences": [
            {
                "name": "Recreational Aide",
                "position": "Amsterdam Nursing Home",
                "start_date": "May 2017",
                "end_date": "Present",
                "descriptions": [
                    "Developed customized recreational activities for 60+ geriatric residents to combat social isolation.",
                    "Implemented daily cognitive engagement programs and provided mobility assistance.",
                    "Improved resident satisfaction scores by 30%.",
                ],
            },
            {
                "name": "Respite Specialist",
                "position": "National Institute for People with Disabilities",
                "start_date": "June 2015",
                "end_date": "April 2016",
                "descriptions": [
                    "Supervised children with developmental disabilities requiring conflict resolution and safety protocols.",
                    "Applied behavioral management techniques during activities.",
                    "Reduced incident reports by 40% over six months.",
                ],
            },
            {
                "name": "Direct Care Worker",
                "position": "Episcopal Social Services",
                "start_date": "March 2012",
                "end_date": "October 2012 (check – year)",
                "descriptions": [
                    "Managed intake for 50+ daily clients.",
                    "Streamlined documentation system, reducing processing time by 25%.",
                ],
            },
        ],
        "education": [
            "Trinity Washington University – Washington, DC – B.A. in Psychology (Anticipated Fall 2025)",
            "Courses: City Seminar I & II, Ethnographies of Work I & II, Statistics, Arts in New York City, Introduction to Biology, Life in New York City, Composition I",
        ],
        "certifications": [
            "Certified Nursing Assistant (CNA) – 2022 (check raw credential)",
            "First Aid & CPR – 2021 (check license validity)",
        ],
        "projects": [
            "Community Outreach Initiative – Led a volunteer group to provide weekly tech support and social entertainment to nursing home residents (metrics pending)."
        ],
        "achievements": [
            "Resident satisfaction scores at Amsterdam Nursing Home increased by 30% due to tailored activity programming.",
            "Incident reports within the National Institute setting decreased by 40% through proactive behavioral strategies.",
            "Document processing time at Episcopal Social Services reduced by 25% via system improvements.",
        ],
    }

    create_resume_pdf(sample_data)
