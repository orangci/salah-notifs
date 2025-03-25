# notify-salawāt
Bismillah.
Notify-salawāt is an 80 line Python CLI program for Linux which does only one thing; sends a notification at the adhān and iqāma of each prayer. This project utilizes the [aladhan](https://aladhan.com/prayer-times-api) API. It uses ~25MiB of memory.

## Dependancies
- python
- notify-send

That's it. I tried to ensure it had as little dependencies as possible.

## Installation
Clone this repository. Assuming you placed the repository in `~/code` (place it anywhere you want, this is just an example), set this command to auto-start when you launch your computer: `python3 ~/code/notify-salawat/main.py --city "your city" --country "your country"`.

A Nix flake for NixOS and home-manager is coming soon.

## Configuration
- `--country "your country"`: Required so that the prayer times can be fetched.
- `--city "your city"`: Required so that the prayer times can be fetched.
- `-i`, `--iqama`: Toggle iqāma notifications. Enabled by default.
- `-g`, `--gap`: Gap in minutes between the adhān and iqāma notifications. Default is 15.

## License
[GNU GPL v3](./LICENSE).