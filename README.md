# sujuda-data

The masjid list used by the **Sujuda** app (Mosques tab). The app downloads
`masjids.json` from this repository once a day, so changes reach users
**without an app update**. The app also ships with a copy built in, used when
the phone is offline or this file can't be read.

## Editing the list

1. Open `masjids.json` and tap the pencil (edit) icon.
2. Make your change, then **Commit changes**.
3. Check the result under **Actions**: a green tick means the list is fine.
   A red X means the app will ignore this version and keep the last good
   one; open the run to see which line is wrong.

Phones pick up the change within about a day (the next time the Mosques tab
opens after their daily check).

## Fields of one masjid

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Unique, lowercase with dashes, e.g. `masjid-al-jannah`. Don't change it later. |
| `name` | yes | Shown in the app. |
| `latitude`, `longitude` | yes | Position, as numbers. |
| `coordinatesApproximate` | no | `true` if the position is only roughly right; directions then use the address. |
| `address`, `city`, `country` | no | Shown under the name. |
| `website` | no | The masjid's website ("Website" button). |
| `prayerTimesUrl` | no | A page that is **only** the prayer-time table (often the widget their site embeds). Shown by the "Prayer times" button. |
| `prayerTimeSourceUrl` + `prayerTimesSelector` | no | Instead of `prayerTimesUrl`: the page with the table, and the CSS selector of the table on it. The app shows only that part. |
| `prayerTimesMustContain` | no | Text the table must contain (e.g. `Fajr`), to pick the right one. |
| `verified` | no | `true` for entries you've checked yourself. |
| `notes` | no | For you; not shown in the app. |

Without `prayerTimesUrl` or `prayerTimesSelector`, a masjid has no "Prayer
times" button.

Links must start with `https://` (or `http://`).
