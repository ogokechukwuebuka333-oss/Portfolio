from playwright.sync_api import expect

from conftest import view_box


def test_city_renders_all_projects(home):
    for pid in ("betalmighty", "dnt", "hassanah", "soundyaad", "hq"):
        expect(home.locator(f'#scene g.pin[data-id="{pid}"]')).to_have_count(1)
    expect(home.locator("#panel h2")).to_have_text("BetAlmighty")


def test_click_building_updates_panel(home):
    home.locator("#plan").scroll_into_view_if_needed()
    home.locator('#scene g.pin[data-id="hassanah"]').click()
    expect(home.locator("#panel h2")).to_have_text("Hassanah Shonibare")
    expect(home.locator("#panel .soon")).to_have_text("Case study in progress")

    home.locator('#scene g.pin[data-id="hq"]').click()
    expect(home.locator("#panel h2")).to_have_text("Chukwuebuka Ogoke")
    expect(home.locator("#panel [data-mail]")).to_be_visible()


def test_zoom_and_reset(home):
    start = view_box(home)
    home.click("#zin")
    assert view_box(home)[2] < start[2]
    home.click("#zout")
    home.click("#zout")
    assert view_box(home)[2] > start[2]
    home.click("#zre")
    assert view_box(home) == start


def test_drag_pans_the_map(home):
    home.locator("#plan").scroll_into_view_if_needed()
    box = home.locator("#scene").bounding_box()
    x, y = box["x"] + box["width"] * 0.15, box["y"] + box["height"] * 0.15
    before = view_box(home)
    home.mouse.move(x, y)
    home.mouse.down()
    home.mouse.move(x + 120, y + 60, steps=8)
    home.mouse.up()
    after = view_box(home)
    assert after[0] < before[0] and after[1] < before[1], (before, after)
    assert after[2] == before[2]  # panning doesn't zoom


def test_full_screen_pan_zoom_and_exit(home):
    plan = home.locator(".plan")
    home.click("#zfull")
    expect(plan).to_have_class("plan full")
    expect(home.locator("#zfull")).to_have_attribute("aria-pressed", "true")
    assert home.evaluate("getComputedStyle(document.body).overflow") == "hidden"
    box = home.locator("#scene").bounding_box()
    vp = home.viewport_size
    assert box["width"] > vp["width"] * 0.5 and box["height"] > vp["height"] * 0.6

    before = view_box(home)
    home.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    home.mouse.wheel(0, -400)
    home.wait_for_timeout(100)
    assert view_box(home)[2] < before[2], "wheel should zoom in while full screen"

    home.keyboard.press("Escape")
    expect(plan).to_have_class("plan")
    expect(home.locator("#zfull")).to_have_attribute("aria-pressed", "false")
    assert home.evaluate("getComputedStyle(document.body).overflow") != "hidden"


def test_wheel_does_not_hijack_page_scroll(home):
    home.locator("#plan").scroll_into_view_if_needed()
    box = home.locator("#scene").bounding_box()
    before_vb = view_box(home)
    before_y = home.evaluate("scrollY")
    home.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    home.mouse.wheel(0, 300)
    home.wait_for_timeout(200)
    assert view_box(home) == before_vb
    assert home.evaluate("scrollY") > before_y


def test_full_screen_button_toggles_back(home):
    home.click("#zfull")
    expect(home.locator(".plan")).to_have_class("plan full")
    home.click("#zfull")
    expect(home.locator(".plan")).to_have_class("plan")
