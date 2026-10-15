"""The city explorer: a full-screen map opened from the hero, the explore buttons and the in-progress cards."""
from playwright.sync_api import expect

from conftest import view_box


def open_explorer(page, via=".hexplore"):
    page.click(via)
    expect(page.locator("#explorer")).to_have_class("plan full")


def test_explorer_is_hidden_until_opened(home):
    expect(home.locator("#explorer")).to_be_hidden()
    open_explorer(home)
    expect(home.locator("#explorer")).to_be_visible()
    expect(home.locator("#xclose")).to_be_focused()
    for pid in ("betalmighty", "dnt", "hassanah", "soundyaad", "hq"):
        expect(home.locator(f'#scene g.pin[data-id="{pid}"]')).to_have_count(1)


def test_close_returns_focus_to_the_opener(home):
    btn = home.locator(".hexplore")
    btn.click()
    home.click("#xclose")
    expect(home.locator("#explorer")).to_be_hidden()
    expect(btn).to_be_focused()
    assert home.evaluate("getComputedStyle(document.body).overflow") != "hidden"


def test_label_click_updates_the_floating_card(home):
    open_explorer(home)
    home.locator('#plabels .plabel[data-id="hassanah"]').click()
    expect(home.locator("#panel h2")).to_have_text("Hassanah Shonibare")
    expect(home.locator("#panel .soon")).to_have_text("Case study in progress")
    home.locator('#plabels .plabel[data-id="hq"]').click()
    expect(home.locator("#panel h2")).to_have_text("Chukwuebuka Ogoke")
    expect(home.locator("#panel [data-mail]")).to_be_visible()


def test_selected_building_is_not_hidden_behind_the_card(home):
    home.locator('.draft[data-q="dnt"]').click()
    expect(home.locator("#panel h2")).to_have_text("Dataset Nexus Tech")
    home.wait_for_timeout(700)  # camera glide
    label = home.locator('#plabels .plabel[data-id="dnt"]').bounding_box()
    card = home.locator("#panel").bounding_box()
    assert label["x"] > card["x"] + card["width"], "the building should land to the right of the card"


def test_zoom_and_reset(home):
    open_explorer(home)
    start = view_box(home)
    home.click("#zin")
    assert view_box(home)[2] < start[2]
    home.click("#zout")
    home.click("#zout")
    assert view_box(home)[2] > start[2]
    home.click("#zre")
    assert view_box(home)[2] == start[2]


def test_drag_pans_the_map(home):
    open_explorer(home)
    box = home.locator("#scene").bounding_box()
    x, y = box["x"] + box["width"] * 0.6, box["y"] + box["height"] * 0.85
    before = view_box(home)
    home.mouse.move(x, y)
    home.mouse.down()
    home.mouse.move(x + 120, y - 60, steps=8)
    home.mouse.up()
    after = view_box(home)
    assert after[0] < before[0] and after[1] > before[1], (before, after)
    assert after[2] == before[2]


def test_wheel_zooms_even_over_a_label(home):
    open_explorer(home)
    label = home.locator('#plabels .plabel[data-id="betalmighty"]').bounding_box()
    before = view_box(home)
    home.mouse.move(label["x"] + label["width"] / 2, label["y"] + label["height"] / 2)
    home.mouse.wheel(0, -400)
    home.wait_for_timeout(100)
    assert view_box(home)[2] < before[2]


def test_escape_and_exit_button_close(home):
    open_explorer(home)
    home.keyboard.press("Escape")
    expect(home.locator("#explorer")).to_be_hidden()
    open_explorer(home)
    home.click("#zfull")
    expect(home.locator("#explorer")).to_be_hidden()


def test_labels_are_keyboard_controls(home):
    open_explorer(home)
    home.locator("#plabels .plabel", has_text="Soundyaad").focus()
    home.keyboard.press("Enter")
    expect(home.locator("#panel h2")).to_have_text("Soundyaad")
    expect(home.locator('#plabels .plabel[data-id="soundyaad"]')).to_have_attribute("aria-pressed", "true")
    expect(home.locator('#plabels .plabel[data-id="betalmighty"]')).to_have_attribute("aria-pressed", "false")


def test_labels_follow_the_map_and_keep_their_size(home):
    open_explorer(home)
    label = home.locator('#plabels .plabel[data-id="dnt"]')
    before = label.bounding_box()
    home.click("#zin")
    after = label.bounding_box()
    assert (before["x"], before["y"]) != (after["x"], after["y"])
    assert abs(after["height"] - before["height"]) < 1


def test_case_study_link_in_the_card(home, base_url):
    open_explorer(home)
    home.locator('#plabels .plabel[data-id="betalmighty"]').click()
    home.locator("#panel a", has_text="Read the case study").click()
    expect(home).to_have_url(base_url + "/betalmighty")
    expect(home.locator("#case")).to_be_visible()
