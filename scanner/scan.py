#!/usr/bin/python3

from PIL import Image
import gi
gi.require_version('Libinsane', '1.0')
from gi.repository import Libinsane


def raw_to_img(params, img_bytes):
    fmt = params.get_format()
    assert(fmt == Libinsane.ImgFormat.RAW_RGB_24)
    (w, h) = (
        params.get_width(),
        int(len(img_bytes) / 3 / params.get_width())
    )
    print("Mode: RGB : Size: {}x{}".format(w, h))
    return Image.frombuffer("RGB", (w, h), img_bytes, "raw", "RGB", 0, 1)



api = Libinsane.Api.new_safebet()

device = None

devs = api.list_devices(Libinsane.DeviceLocations.ANY)
for d in devs:
    print(d.get_dev_id(), d.to_string())
    if "M281fdw" in d.to_string() :
        device = api.get_device(d.get_dev_id())
    #if "airscan" in d.to_string() and "7520" in d.to_string():
    #    device = api.get_device(d.get_dev_id())

if device is not None:
    print("using", device.get_name())
else:
    print("Can't find suitable scanner")
    exit()

source = None
sources = device.get_children()
print("Available scan sources:")
for src in sources:
    if "flatbed" == src.get_name():
        source = src
        print("Using", source.get_name())


session = source.scan_start()
out = "scanned.png"
try:
    page_nb = 0
    while not session.end_of_feed() and page_nb < 20:
        # Do not assume that all the pages will have the same size !
        scan_params = session.get_scan_parameters()
        total = scan_params.get_image_size()
        if scan_params.get_height() < 0:
            total = "unknown"
        else:
            total = f"{total} B"
        print(
            "Expected scan parameters:"
            f" {scan_params.get_format()} ;"
            f" {scan_params.get_width()}x{scan_params.get_height()}"
            f" = {total}"
        )

        img = []
        r = 0

        print("Scanning page {} --> {}".format(page_nb, out))
        while not session.end_of_page():
            data = session.read_bytes(128 * 1024)
            data = data.get_data()
            img.append(data)
            r += len(data)
            print(f"Got {len(data)} bytes => {r} B / {total}")

        
        img = b"".join(img)
        print("Got {} bytes".format(len(img)))
        if out is not None:
            print("Saving page as {} ...".format(out))
            if scan_params.get_format() == Libinsane.ImgFormat.RAW_RGB_24:
                img = raw_to_img(scan_params, img)
                img.save(out, format="PNG")
            else:
                print("Warning: output format is {}".format(
                    scan_params.get_format()
                ))
                with open(out, 'wb') as fd:
                    fd.write(img)
        page_nb += 1
        print("Page {} scanned".format(page_nb))
    if page_nb == 0:
        print("No page in feeder ?")
finally:
    session.cancel()
    


