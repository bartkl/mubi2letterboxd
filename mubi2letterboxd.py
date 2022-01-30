import os
import csv
import json
import urllib.request
from datetime import datetime
from operator import itemgetter


BASE_URL = "https://mubi.com/services/api/ratings"
USER_ID = "6341306"


def mubi_reader(base_url, user_id, items_per_page=100):
    url = f"{base_url}?user_id={user_id}&per_page={items_per_page}"
    page = 1

    while True:
        with urllib.request.urlopen(f"{url}&page={page}") as conn:
            data = json.loads(conn.read())

            if data == []:
                return

            yield data
            page += 1


# TODO: Locally, to reduce load on MUBI during development.
def mubi_reader(base_url, user_id, items_per_page=100):
    for nr in range(0, 8):
        with open(f"data/out_{nr}.txt") as f:
            yield json.loads(f.read())


def letterboxd_writer(csv_file):
    result = []

    with open(csv_file, "w", newline=os.linesep) as f:
        field_names = ["Title", "Year", "Directors", "Rating", "WatchedDate", "Review"]
        writer = csv.DictWriter(f, fieldnames=field_names)

        writer.writeheader()

        while True:
            mubi_data = yield
            for mubi_item in mubi_data:
                item = create_letterboxd_item(mubi_item)
                writer.writerow(item)


def create_letterboxd_item(mubi_item):
    return {
        "Title": mubi_item["film"]["title"],
        "Year": mubi_item["film"]["year"],
        "Directors": ",".join(map(itemgetter("name"), mubi_item["film"]["directors"])),
        "Rating": float(mubi_item["overall"]),
        "WatchedDate": datetime.fromtimestamp(mubi_item["updated_at"]).strftime("%Y-%m-%d"),
        "Review": mubi_item["body"],
    }


def main():
    read_mubi = mubi_reader(BASE_URL, USER_ID)
    write_letterboxd = letterboxd_writer("out.txt")
    next(write_letterboxd)  # Priming.

    for nr, page in enumerate(read_mubi):
        with open(f"out_{nr}.txt", mode="w") as f:
            write_letterboxd.send(page)
            # f.write(json.dumps(page))



if __name__ == "__main__":
    main()
