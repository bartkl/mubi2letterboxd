# `mubi2letterboxd`

If you want to import your MUBI ratings and reviews into your Letterboxd account, this script is for you.

It is a command-line tool written in Python that imports your MUBI data, extracts the relevant data for Letterboxd and transforms it appropriately, and finally writes a [Letterboxd input format CSV](https://letterboxd.com/about/importing-data/) that you can import [in the browser](https://letterboxd.com/import/).

## Installation and configuration
None, really!

All you need is a working Python installation (version ≥ 3.6). There are no dependencies outside of the standard library, no config files and no setup or installation scripts.
Then, you can simply clone this repository or download the `mubi2letterboxd.py` script directly. That file is all you'll need.

## Usage
To use this script, simply invoke Python on it:

```console
$ python mubi2letterboxd.py
Error: please supply parameters to fetch MUBI data, either from a local file, or from the MUBI API.
```

As you can see, you need to pass in some arguments in order for it to get to work. We'll get to those in a bit. First, let's invoke the help option.


### Help
```console
$ python mubi2letterboxd.py -h

usage: mubi2letterboxd [-h] [--output_path output-path] {file,api} ...

positional arguments:
  {file,api}
    file                import data from a pre-downloaded text file containing the raw JSON data from the MUBI API
                        call
    api                 import data from MUBI by calling the API

optional arguments:
  -h, --help            show this help message and exit
  --output_path output-path, -o output-path
                        path to output Letterboxd CSV file to
```

### Importing from MUBI API
This use case is almost certainly the one you want. It connects to the MUBI API and retrieves your ratings/reviews data.

You'll need to pass in your user ID, which you can find in the URL to your profile.  For example, my profile page URL is:

> https://mubi.com/users/6341306

So, my user ID is `6341306`.

To run the script and fetch the data from the MUBI API, I would enter:

```console
$ python mubi2letterboxd.py api 6341306
Reading data from MUBI API at URL: `https://mubi.com/services/api/ratings` using user ID `6341306` and 100 items per call.

Writing MUBI site data page 1 to the Letterbox'd CSV...   done.
Writing MUBI site data page 2 to the Letterbox'd CSV...   done.
Writing MUBI site data page 3 to the Letterbox'd CSV...   done.
Writing MUBI site data page 4 to the Letterbox'd CSV...   done.
Writing MUBI site data page 5 to the Letterbox'd CSV...   done.
Writing MUBI site data page 6 to the Letterbox'd CSV...   done.
Writing MUBI site data page 7 to the Letterbox'd CSV...   done.
Writing MUBI site data page 8 to the Letterbox'd CSV...   done.

Successfully wrote the Letterboxd import CSV file to `letterboxd.csv`.
```

As you can see, since it defaults to the retrieval of 100 items per call, it had to do 8 calls total to fetch all my data.
The Letterboxd CSV file was then written to `letterboxd.csv` in the current directory, which is default.
This can be changed with the `--output_path` or `-o` option (see _Help_ above).

#### Help
For a full list of supported options, ask for help this way:
```console
$ python mubi2letterboxd.py api -h
usage: mubi2letterboxd api [-h] [--items-per-page ITEMS_PER_PAGE] [--base-url BASE_URL] user-id

positional arguments:
  user-id               your user ID as it appears in the URL of your profile page

optional arguments:
  -h, --help            show this help message and exit
  --items-per-page ITEMS_PER_PAGE
                        items to fetch per call to MUBI
  --base-url BASE_URL   MUBI service API URL to perform requests to
```

### Importing from MUBI data file
If for some reason you already have downloaded the MUBI data in the literal JSON form it is outputted by the API, and have that stored in a file, you can avoid having to connect to MUBI's API and read from that file directly. I won't be detailing this scenario and refer you to the help screen:

```console
$ python mubi2letterboxd.py file -h
usage: mubi2letterboxd file [-h] path

positional arguments:
  path        path to the file to read the data from

optional arguments:
  -h, --help  show this help message and exit
```

## Inspiration
I was inspired by [Igor Rudenko's script](https://github.com/hextriclosan/mubi2letterboxd), but hesitated to use it since it requires installing the Go compiler. Then I figured: "How hard can it be?", and wrote my own version in Python.  Note that this implementation does not mirror that one, but is written from scratch.

## Contact
If you have questions, don't hesitate to ask. It will vary how much time I have to spend on maintaining this though.

