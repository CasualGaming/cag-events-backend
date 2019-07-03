from bs4 import BeautifulSoup


SEAT_BORDER_WIDTH = 0.05


def generate_area_layout(area_layout):
    doc = BeautifulSoup("<svg>", "html.parser")
    svg_element = doc.svg
    svg_element["viewBox"] = "0 0 {0} {1}".format(area_layout.width, area_layout.height)
    svg_element["xmlns"] = "http://www.w3.org/2000/svg"

    for row_layout in area_layout.row_layouts.all():
        row_rotation = "translate({0} {1})".format(row_layout.offset_horizontal, row_layout.offset_vertical)
        row_translation = "rotate(-{0})".format(row_layout.rotation)
        row_element = doc.new_tag("g")
        row_element["id"] = "row-{0}".format(row_layout.row_number)
        row_element["class"] = "row"
        row_element["transform"] = "{0} {1}".format(row_rotation, row_translation)
        for seat_num_vertical in range(1, row_layout.seat_count_vertical + 1):
            for seat_num_horizontal in range(1, row_layout.seat_count_horizontal + 1):
                seat_element = _generate_area_layout_seat(doc, row_layout, seat_num_vertical, seat_num_horizontal)
                row_element.append(seat_element)
        svg_element.append(row_element)

    return doc.prettify("utf-8")


def _generate_area_layout_seat(doc, row_layout, seat_num_vertical, seat_num_horizontal):
    seat_num = (seat_num_vertical - 1) * row_layout.seat_count_horizontal + seat_num_horizontal
    seat_element = doc.new_tag("a")
    seat_element["class"] = "seat"
    seat_element["href"] = "#"
    seat_element["data-row-num"] = row_layout.row_number
    seat_element["data-seat-num"] = seat_num
    content_element = doc.new_tag("rect")
    content_element["width"] = row_layout.seat_width - 2 * SEAT_BORDER_WIDTH
    content_element["height"] = row_layout.seat_height - 2 * SEAT_BORDER_WIDTH
    content_element["x"] = (seat_num_horizontal - 1) * (row_layout.seat_width + row_layout.seat_spacing_horizontal) + SEAT_BORDER_WIDTH
    content_element["y"] = (seat_num_vertical - 1) * (row_layout.seat_height + row_layout.seat_spacing_vertical) + SEAT_BORDER_WIDTH
    seat_element.append(content_element)
    return seat_element
