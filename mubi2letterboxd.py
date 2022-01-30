import argparse
import sys
import os
import csv
import json
import urllib.request
import urllib.error
from datetime import datetime
from operator import itemgetter


BASE_URL = "https://mubi.com/services/api/ratings"
ITEMS_PER_PAGE = 100


def log(msg, ret_code=None):
    print(msg, end="")

    if ret_code is not None:
        sys.exit(ret_code)


def mubi_api_reader(base_url, user_id, items_per_page=100):
    url = f"{base_url}?user_id={user_id}&per_page={items_per_page}"
    page = 1

    while True:
        try:
            with urllib.request.urlopen(f"{url}&page={page}") as conn:
                data = json.loads(conn.read())

                if data == []:
                    return

                yield data
                page += 1
        except urllib.error.HTTPError as e:
            log("The MUBI server gave an error response:\n")
            log(f"Status code: {e.code}\n")
            log(f"Message: {e.read()}\n", -1)
        except urllib.error.URLError as e:
            log("The provided URL is invalid.", -1)


def mubi_file_reader(path):
    with open(path) as f:
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
    parser = argparse.ArgumentParser(prog="mubi2letterboxd")
    parser.add_argument("--output_path", "-o", metavar="output-path", default="letterboxd.csv", help="path to output Letterboxd CSV file to")
    subparsers = parser.add_subparsers()

    parser_file = subparsers.add_parser("file", help="import data from a pre-downloaded text file containing the raw JSON data from the MUBI API call")
    parser_api = subparsers.add_parser("api", help="import data from MUBI by calling the API")

    parser_file.add_argument("path", help="path to the file to read the data from")

    parser_api.add_argument("user_id", metavar="user-id", help="your user ID as it appears in the URL of your profile page")
    parser_api.add_argument("--items-per-page", default=ITEMS_PER_PAGE, help="items to fetch per call to MUBI")
    parser_api.add_argument("--base-url", default=BASE_URL, help="MUBI service API URL to perform requests to")

    args = parser.parse_args()

    write_letterboxd = letterboxd_writer(args.output_path)
    next(write_letterboxd)  # Priming the coroutine.

    if "path" in args:
        log(f"Reading data from MUBI file `{args.path}`.\n")
        read_mubi = mubi_file_reader(args.path)

        log("Writing data to the Letterbox'd CSV...")
        write_letterboxd.send(next(read_mubi))
        log("  done.\n")
    elif "user_id" in args:
        log(f"Reading data from MUBI API at URL: `{args.base_url}` using user ID `{args.user_id}` and {args.items_per_page} items per call.\n")
        read_mubi = mubi_api_reader(args.base_url, args.user_id, args.items_per_page)

        for nr, page in enumerate(read_mubi, 1):
            log(f"Writing MUBI site data page {nr} to the Letterbox'd CSV...")
            write_letterboxd.send(page)
            log("  done.\n")
    else:
        log("Error: please supply parameters to fetch MUBI data, either from a local file, or from the MUBI API.\n", -1)

    log(f"\nSuccessfully wrote the Letterboxd import CSV file to `{args.output_path}`.\n")


if __name__ == "__main__":
    main()
