from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent

BG_TOP = "#F7F9FC"
BG_BOTTOM = "#EEF3F8"
WHITE = "#FFFFFF"
TEXT = "#20314A"
TEXT_SOFT = "#5B708D"
TEXT_LIGHT = "#D7E4F5"
STROKE = "#D8E1EC"
ACCENT = "#55749E"
NODE_DARK_1 = "#20314A"
NODE_DARK_2 = "#36547C"
USER_FILL = "#FFF7EF"
USER_STROKE = "#F2CC8F"
ADMIN_FILL = "#EEF8F6"
ADMIN_STROKE = "#8CD5BF"

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)


def vertical_gradient(draw, size, top, bottom):
    width, height = size
    top_rgb = tuple(int(top[i : i + 2], 16) for i in (1, 3, 5))
    bottom_rgb = tuple(int(bottom[i : i + 2], 16) for i in (1, 3, 5))
    for y in range(height):
        t = y / max(height - 1, 1)
        color = tuple(int(top_rgb[i] * (1 - t) + bottom_rgb[i] * t) for i in range(3))
        draw.line((0, y, width, y), fill=color)


def rounded_box(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def gradient_box(img, box, radius, c1, c2, outline=None, width=1):
    x1, y1, x2, y2 = map(int, box)
    w, h = x2 - x1, y2 - y1
    layer = Image.new("RGBA", (w, h))
    layer_draw = ImageDraw.Draw(layer)
    c1_rgb = tuple(int(c1[i : i + 2], 16) for i in (1, 3, 5))
    c2_rgb = tuple(int(c2[i : i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        t = y / max(h - 1, 1)
        color = tuple(int(c1_rgb[i] * (1 - t) + c2_rgb[i] * t) for i in range(3)) + (255,)
        layer_draw.line((0, y, w, y), fill=color)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    img.paste(layer, (x1, y1), mask)
    if outline:
        ImageDraw.Draw(img).rounded_rectangle(box, radius=radius, outline=outline, width=width)


def centered_text(draw, x, y, text_value, font_obj, fill):
    bbox = draw.textbbox((0, 0), text_value, font=font_obj)
    w = bbox[2] - bbox[0]
    draw.text((x - w / 2, y), text_value, font=font_obj, fill=fill)


def arrow(draw, start, end, color=ACCENT, width=3):
    draw.line((start, end), fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    tip = (x2, y2)
    base = (x2 - ux * 16, y2 - uy * 16)
    p1 = (base[0] + px * 7, base[1] + py * 7)
    p2 = (base[0] - px * 7, base[1] - py * 7)
    draw.polygon([tip, p1, p2], fill=color)


def dashed_line(draw, start, end, color="#B1C2D8", width=2, dash=12, gap=8):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / length, dy / length
    pos = 0
    while pos < length:
        seg = min(dash, length - pos)
        sx = x1 + ux * pos
        sy = y1 + uy * pos
        ex = x1 + ux * (pos + seg)
        ey = y1 + uy * (pos + seg)
        draw.line((sx, sy, ex, ey), fill=color, width=width)
        pos += dash + gap


def render_dfd():
    img = Image.new("RGB", (1600, 980), BG_TOP)
    draw = ImageDraw.Draw(img)
    vertical_gradient(draw, img.size, BG_TOP, BG_BOTTOM)

    title_font = font(42, True)
    subtitle_font = font(18)
    node_title = font(24, True)
    node_text = font(18)
    header_font = font(16, True)
    flow_font = font(16, True)

    centered_text(draw, 800, 32, "Data Flow Diagram - AI Career Navigator", title_font, TEXT)
    centered_text(draw, 800, 86, "Level 1 overview of user, admin, core modules, and stored data", subtitle_font, TEXT_SOFT)

    rounded_box(draw, (95, 220, 315, 330), 28, USER_FILL, USER_STROKE, 2)
    centered_text(draw, 205, 248, "User", node_title, TEXT)
    centered_text(draw, 205, 286, "Assessment input", node_text, TEXT_SOFT)

    rounded_box(draw, (1285, 220, 1505, 330), 28, ADMIN_FILL, ADMIN_STROKE, 2)
    centered_text(draw, 1395, 248, "Admin", node_title, TEXT)
    centered_text(draw, 1395, 286, "Content management", node_text, TEXT_SOFT)

    rounded_box(draw, (520, 170, 1080, 340), 36, WHITE, STROKE, 2)
    gradient_box(img, (520, 170, 1080, 228), 36, NODE_DARK_1, "#38527A")
    centered_text(draw, 800, 186, "AI CAREER NAVIGATOR SYSTEM", header_font, WHITE)
    draw.text((570, 248), "Core Processes", font=font(24, True), fill=TEXT)
    draw.text((570, 288), "1. Authentication", font=node_text, fill=TEXT_SOFT)
    draw.text((840, 288), "2. Assessment", font=node_text, fill=TEXT_SOFT)
    draw.text((570, 320), "3. Recommendation Engine", font=node_text, fill=TEXT_SOFT)
    draw.text((840, 320), "4. Roadmap & Progress", font=node_text, fill=TEXT_SOFT)

    stores = [
        ((190, 505, 460, 625), "Users", "accounts, roles, profiles"),
        ((505, 505, 775, 625), "Assessments", "inputs, preferences, history"),
        ((820, 505, 1090, 625), "Careers & Skills", "career catalog, skill map"),
        ((1135, 505, 1405, 625), "Resources & Progress", "roadmap items, completion state"),
    ]
    for box, title, desc in stores:
        rounded_box(draw, box, 28, WHITE, STROKE, 2)
        cx = (box[0] + box[2]) / 2
        centered_text(draw, cx, box[1] + 30, title, node_title, TEXT)
        centered_text(draw, cx, box[1] + 66, desc, node_text, TEXT_SOFT)

    arrow(draw, (315, 275), (520, 255))
    centered_text(draw, 420, 226, "register, login, assessment", flow_font, ACCENT)
    arrow(draw, (1080, 255), (1285, 275))
    centered_text(draw, 1185, 226, "analytics, CRUD actions", flow_font, ACCENT)
    arrow(draw, (520, 315), (315, 315))
    centered_text(draw, 418, 338, "results, history, roadmap", flow_font, ACCENT)
    arrow(draw, (1285, 315), (1080, 315))
    centered_text(draw, 1182, 338, "resource updates, reports", flow_font, ACCENT)

    arrow(draw, (650, 340), (390, 505))
    draw.text((468, 430), "auth data", font=flow_font, fill=ACCENT)
    arrow(draw, (740, 340), (665, 505))
    draw.text((678, 430), "assessment data", font=flow_font, fill=ACCENT)
    arrow(draw, (860, 340), (910, 505))
    draw.text((892, 430), "matching rules", font=flow_font, fill=ACCENT)
    arrow(draw, (970, 340), (1215, 505))
    draw.text((1088, 445), "resources, progress", font=flow_font, fill=ACCENT)

    dashed_line(draw, (325, 505), (640, 625))
    draw.text((390, 598), "user linked to assessments", font=flow_font, fill="#7E93AE")
    dashed_line(draw, (955, 625), (1270, 625))
    draw.text((1028, 598), "careers mapped to resources", font=flow_font, fill="#7E93AE")
    dashed_line(draw, (640, 625), (955, 625))
    centered_text(draw, 798, 642, "recommendations generated from assessments + skills", flow_font, "#7E93AE")

    rounded_box(draw, (430, 760, 1170, 880), 28, WHITE, STROKE, 2)
    centered_text(draw, 800, 786, "System Outputs", node_title, TEXT)
    centered_text(draw, 800, 830, "ranked careers, explainable fit score, roadmap resources, saved progress, admin insights", node_text, TEXT_SOFT)

    img.save(BASE / "dfd-diagram.png")


def render_flow():
    img = Image.new("RGB", (1600, 1180), BG_TOP)
    draw = ImageDraw.Draw(img)
    vertical_gradient(draw, img.size, BG_TOP, BG_BOTTOM)

    title_font = font(42, True)
    subtitle_font = font(18)
    step_font = font(22, True)
    copy_font = font(18)
    small_font = font(16, True)

    centered_text(draw, 800, 32, "System Flow - AI Career Navigator", title_font, TEXT)
    centered_text(draw, 800, 86, "End-to-end user and admin interaction flow", subtitle_font, TEXT_SOFT)

    steps = [
        (170, 170, "1. User opens platform and signs in", "Register or log in to unlock private history, progress tracking, and personalized recommendations."),
        (170, 340, "2. User completes the live assessment", "The system captures interest area, education, experience level, preferred domain, work style, salary goal, and selected skills."),
        (170, 510, "3. Recommendation engine evaluates fit", "Assessment data is compared with stored careers, required skills, and weighting rules to rank the strongest career matches."),
        (170, 680, "4. User views results and opens a career path", "Top recommendations, fit scores, confidence, comparison insights, and explainable reasoning are displayed."),
        (170, 850, "5. User follows roadmap resources and tracks progress", "Courses, projects, videos, articles, certifications, and documentation can be filtered and marked as saved, in progress, or completed."),
    ]

    for x, y, title, desc in steps:
        gradient_box(img, (x, y, x + 1260, y + 120), 34, NODE_DARK_1, NODE_DARK_2)
        draw.text((250, y + 28), title, font=step_font, fill=WHITE)
        draw.text((250, y + 64), desc, font=copy_font, fill=TEXT_LIGHT)

    for y1, y2 in [(290, 340), (460, 510), (630, 680), (800, 850)]:
        arrow(draw, (800, y1), (800, y2), color=ACCENT, width=4)

    rounded_box(draw, (200, 1015, 760, 1125), 30, WHITE, STROKE, 2)
    centered_text(draw, 480, 1038, "6. History Dashboard", font(24, True), TEXT)
    centered_text(draw, 480, 1074, "Past assessments, progress totals, and continue-roadmap access", small_font, TEXT_SOFT)

    rounded_box(draw, (840, 1015, 1400, 1125), 30, WHITE, STROKE, 2)
    centered_text(draw, 1120, 1038, "7. Admin Management", font(24, True), TEXT)
    centered_text(draw, 1120, 1074, "Admin updates careers, skills, and resources that power future recommendations", small_font, TEXT_SOFT)

    arrow(draw, (600, 970), (520, 1015), color=ACCENT)
    arrow(draw, (1000, 970), (1080, 1015), color=ACCENT)

    img.save(BASE / "system-flow-diagram.png")


def entity_box(draw, box, title, fields, fill=WHITE, outline=STROKE):
    rounded_box(draw, box, 24, fill, outline, 2)
    x1, y1, x2, _ = box
    gradient_box(
        img_ref,
        (x1, y1, x2, y1 + 48),
        24,
        NODE_DARK_1,
        "#38527A",
    )
    centered_text(draw, (x1 + x2) / 2, y1 + 11, title, font(18, True), WHITE)
    y = y1 + 62
    field_font = font(15)
    for field in fields:
        draw.text((x1 + 18, y), field, font=field_font, fill=TEXT_SOFT)
        y += 22


def plain_entity_box(draw, box, title, fill="#B8E986", outline="#597D3C"):
    x1, y1, x2, y2 = map(int, box)
    draw.rectangle(box, fill=fill, outline=outline, width=2)
    centered_text(draw, (x1 + x2) / 2, y1 + (y2 - y1) / 2 - 14, title, font(20, True), "#203014")


def attribute_oval(draw, center, text_value, fill="#BFEFEA", outline="#3B6F7C"):
    cx, cy = center
    text_font = font(15)
    bbox = draw.textbbox((0, 0), text_value, font=text_font)
    w = bbox[2] - bbox[0] + 34
    h = 40
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    draw.ellipse(box, fill=fill, outline=outline, width=2)
    centered_text(draw, cx, cy - 10, text_value, text_font, TEXT)
    return box


def diamond(draw, center, text_value, fill="#F6B450", outline="#A96B12"):
    cx, cy = center
    text_font = font(14, True)
    bbox = draw.textbbox((0, 0), text_value, font=text_font)
    w = bbox[2] - bbox[0] + 48
    h = 54
    pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
    draw.polygon(pts, fill=fill, outline=outline)
    centered_text(draw, cx, cy - 10, text_value, text_font, TEXT)
    return pts


def line(draw, start, end, color="#111111", width=2):
    draw.line((start, end), fill=color, width=width)


def render_er():
    img = Image.new("RGB", (1900, 1240), "white")
    draw = ImageDraw.Draw(img)
    title_font = font(44, True)
    note_font = font(18)
    small_font = font(16, True)

    centered_text(draw, 950, 26, "AI CAREER NAVIGATOR - ER DIAGRAM", title_font, "#143B73")

    boxes = {
        "users": (110, 180, 290, 260),
        "assessments": (720, 170, 930, 255),
        "recommendations": (1450, 170, 1700, 255),
        "careers": (930, 520, 1130, 600),
        "career_skills": (290, 640, 530, 725),
        "skills": (120, 930, 300, 1010),
        "learning_resources": (900, 910, 1180, 995),
        "recommendation_skill_gaps": (1420, 620, 1710, 710),
        "user_progress": (1440, 930, 1670, 1015),
    }

    for key, title in [
        ("users", "USERS"),
        ("assessments", "ASSESSMENTS"),
        ("recommendations", "RECOMMENDATIONS"),
        ("careers", "CAREERS"),
        ("career_skills", "CAREER_SKILLS"),
        ("skills", "SKILLS"),
        ("learning_resources", "LEARNING_RESOURCES"),
        ("recommendation_skill_gaps", "RECOMMENDATION_SKILL_GAPS"),
        ("user_progress", "USER_PROGRESS"),
    ]:
        plain_entity_box(draw, boxes[key], title)

    attributes = {
        "users": [("id (PK)", (110, 90)), ("full_name", (50, 140)), ("email", (45, 195)), ("password_hash", (75, 250)), ("role", (80, 305)), ("education_level", (95, 360)), ("experience_level", (165, 415))],
        "assessments": [("id (PK)", (700, 80)), ("user_id (FK)", (620, 150)), ("interest_area", (610, 220)), ("education_level", (610, 280)), ("experience_level", (1010, 95)), ("preferred_domain", (1055, 155)), ("work_style", (1080, 215)), ("goal_salary", (1040, 275)), ("created_at", (995, 335))],
        "recommendations": [("id (PK)", (1715, 85)), ("assessment_id (FK)", (1795, 145)), ("career_id (FK)", (1780, 200)), ("fit_score", (1790, 255)), ("confidence_score", (1810, 315)), ("rank", (1770, 375)), ("reason_summary", (1750, 435))],
        "careers": [("id (PK)", (860, 430)), ("title", (760, 500)), ("slug", (770, 560)), ("description", (785, 620)), ("industry", (800, 680)), ("growth_outlook", (1170, 450)), ("salary_min", (1190, 510)), ("salary_max", (1185, 570)), ("is_active", (1165, 630))],
        "career_skills": [("id (PK)", (210, 545)), ("career_id (FK)", (155, 610)), ("skill_id (FK)", (155, 670)), ("importance_level", (170, 735)), ("is_required", (190, 795)), ("weight", (245, 855))],
        "skills": [("id (PK)", (75, 865)), ("name", (55, 935)), ("category", (60, 990)), ("description", (85, 1045))],
        "learning_resources": [("id (PK)", (780, 1070)), ("career_id (FK)", (790, 1140)), ("skill_id (FK)", (860, 1185)), ("title", (985, 1085)), ("resource_type", (1085, 1085)), ("url", (1165, 1085)), ("provider", (1240, 1035)), ("difficulty_level", (1310, 980)), ("is_active", (1270, 1125))],
        "recommendation_skill_gaps": [("id (PK)", (1815, 585)), ("recommendation_id (FK)", (1885, 645)), ("skill_id (FK)", (1850, 705)), ("gap_type", (1825, 765)), ("suggestion", (1800, 825))],
        "user_progress": [("id (PK)", (1775, 905)), ("user_id (FK)", (1805, 965)), ("resource_id (FK)", (1840, 1020)), ("status", (1805, 1080)), ("created_at", (1760, 1140)), ("updated_at", (1710, 1190))],
    }

    entity_centers = {k: ((v[0] + v[2]) / 2, (v[1] + v[3]) / 2) for k, v in boxes.items()}

    for key, items in attributes.items():
        ex, ey = entity_centers[key]
        for label, center in items:
            oval = attribute_oval(draw, center, label)
            ox = (oval[0] + oval[2]) / 2
            oy = (oval[1] + oval[3]) / 2
            line(draw, (ox, oy), (ex, ey))

    relationships = {
        "users_assessments": ((420, 220), "has"),
        "users_progress": ((200, 560), "tracks"),
        "assessments_recommendations": ((1160, 215), "generates"),
        "careers_recommendations": ((1275, 390), "appears in"),
        "careers_career_skills": ((720, 600), "requires"),
        "skills_career_skills": ((385, 835), "maps to"),
        "careers_learning_resources": ((1035, 760), "has"),
        "skills_learning_resources": ((580, 975), "linked to"),
        "recommendations_gaps": ((1575, 435), "has"),
        "skills_gaps": ((1020, 760), "identifies"),
        "resources_progress": ((1310, 955), "tracked in"),
    }

    for _, (center, label) in relationships.items():
        diamond(draw, center, label)

    def rect_mid(box, side):
        x1, y1, x2, y2 = box
        if side == "left":
            return (x1, (y1 + y2) / 2)
        if side == "right":
            return (x2, (y1 + y2) / 2)
        if side == "top":
            return ((x1 + x2) / 2, y1)
        return ((x1 + x2) / 2, y2)

    rel_connections = [
        ("users", "right", "users_assessments", "left", "1", "M"),
        ("users", "bottom", "users_progress", "top", "1", "M"),
        ("assessments", "right", "assessments_recommendations", "left", "1", "M"),
        ("careers", "top", "careers_recommendations", "bottom", "1", "M"),
        ("recommendations", "left", "careers_recommendations", "right", "M", "1"),
        ("careers", "left", "careers_career_skills", "right", "1", "M"),
        ("career_skills", "top", "careers_career_skills", "left", "M", "1"),
        ("skills", "top", "skills_career_skills", "left", "1", "M"),
        ("career_skills", "bottom", "skills_career_skills", "right", "M", "1"),
        ("careers", "bottom", "careers_learning_resources", "top", "1", "M"),
        ("learning_resources", "top", "careers_learning_resources", "bottom", "M", "1"),
        ("skills", "right", "skills_learning_resources", "left", "1", "M"),
        ("learning_resources", "left", "skills_learning_resources", "right", "M", "1"),
        ("recommendations", "bottom", "recommendations_gaps", "top", "1", "M"),
        ("recommendation_skill_gaps", "top", "recommendations_gaps", "bottom", "M", "1"),
        ("skills", "right", "skills_gaps", "left", "1", "M"),
        ("recommendation_skill_gaps", "left", "skills_gaps", "right", "M", "1"),
        ("learning_resources", "right", "resources_progress", "left", "1", "M"),
        ("user_progress", "left", "resources_progress", "right", "M", "1"),
    ]

    # Build relationship boxes for connector points after drawing them.
    rel_boxes = {}
    for key, (center, label) in relationships.items():
        cx, cy = center
        text_font = font(14, True)
        bbox = draw.textbbox((0, 0), label, font=text_font)
        w = bbox[2] - bbox[0] + 48
        h = 54
        rel_boxes[key] = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

    def diamond_mid(box, side):
        x1, y1, x2, y2 = box
        if side == "left":
            return (x1, (y1 + y2) / 2)
        if side == "right":
            return (x2, (y1 + y2) / 2)
        if side == "top":
            return ((x1 + x2) / 2, y1)
        return ((x1 + x2) / 2, y2)

    for entity, e_side, rel_key, rel_side, near_card, far_card in rel_connections:
        start = rect_mid(boxes[entity], e_side)
        end = diamond_mid(rel_boxes[rel_key], rel_side)
        line(draw, start, end)
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        centered_text(draw, mx - 16, my - 12, near_card, small_font, "#111111")

    note_box = (180, 1160, 1720, 1215)
    draw.rectangle(note_box, outline="#8C9AA8", width=2)
    draw.text((210, 1175), "NOTE:", font=font(20, True), fill="#143B73")
    draw.text((350, 1178), "Many-to-many relationship between Careers and Skills is implemented using CAREER_SKILLS.", font=note_font, fill=TEXT)
    draw.text((1150, 1178), "User roadmap tracking is stored in USER_PROGRESS.", font=note_font, fill=TEXT)
    img.save(BASE / "er-diagram.png")


if __name__ == "__main__":
    render_dfd()
    render_flow()
    render_er()
