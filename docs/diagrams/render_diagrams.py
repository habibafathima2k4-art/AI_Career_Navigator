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


if __name__ == "__main__":
    render_dfd()
    render_flow()
