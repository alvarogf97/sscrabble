# Sscrabble in a nutshell

Sscrabble allows you to hide secret messages in spotify playlist with 0 effort. Giving a playlist and the message it will gives you the tracks order or the missing letters you have to add in order to complete the message.

# Retrieving spotify access token

1. Open spotify web and logs in.
2. Open the development console and clicks on `Network`.
3. Search the request wss://gew1-dealer.spotify.com/?access_token={access_token}.
4. Copy access token value.

# Usage

Just invoke **process** command and let sscrabble resolve it for you

```cmd
 Usage: sscrabble.py process [OPTIONS] PLAYLIST_URL MESSAGE

╭─ Arguments ───────────────────────────────────────────────────╮
│ *    playlist_url      TEXT  [default: None] [required]       │
│ *    message           TEXT  [default: None] [required]       │
╰───────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────╮
│ --strategy                   TEXT  [default: inline]          │
│ --commit      --no-commit          [default: no-commit]       │
│ --help                             Show this message and exit.│
╰───────────────────────────────────────────────────────────────╯
```

If there's not enough letters you will receive the missings ones

```cmd
❌ Missing letters
┏━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Letter ┃ Missings ┃ Positions ┃
┡━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
│ a      │ 1        │ 1         │
│ e      │ 4        │ 1         │
│ n      │ 3        │ 1         │
│ r      │ 1        │ 1         │
└────────┴──────────┴───────────┘
```

Otherwise full order tracklist will be displayed (for message `wait`)

```cmd
✅ Resolution
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Position ┃ Track name                                           ┃ Track artist                ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 0        │ War Of Hearts - Acoustic Version                     │ Ruelle                      │
│ 1        │ Already Gone                                         │ Sleeping At Last            │
│ 2        │ If I Could Fly                                       │ One Direction               │
│ 3        │ Truce                                                │ Twenty One Pilots           │
│ 4        │ Must Have Been The Wind                              │ Alec Benjamin               │
│ 5        │ Sorry                                                │ Halsey                      │
│ 6        │ Shattered                                            │ Trading Yesterday           │
│ 7        │ You Said You'd Grow Old With Me                      │ Michael Schulte             │
│ 8        │ One More Light                                       │ Linkin Park                 │
│ 9        │ undressed                                            │ sombr                       │
│ 10       │ Last to Know                                         │ Three Days Grace            │
│ 11       │ Let Me Down Slowly                                   │ Alec Benjamin               │
│ 12       │ Kitchen Sink                                         │ Isabelle Hyde               │
│ 13       │ Glimpse of Us                                        │ Joji                        │
│ 14       │ Leave the City                                       │ Twenty One Pilots           │
│ 15       │ listen before i go                                   │ Billie Eilish               │
│ 16       │ IDK You Yet                                          │ Alexander 23                │
│ 17       │ Die A Little                                         │ YUNGBLUD                    │
│ 18       │ I Can't Make You Love Me                             │ Dave Thomas Junior          │
│ 19       │ Take on the World                                    │ You Me At Six               │
│ 20       │ Flares                                               │ The Script                  │
│ 21       │ Crash                                                │ Sum 41                      │
│ 22       │ Colors - Stripped                                    │ Halsey                      │
│ 23       │ From The Start                                       │ Laufey                      │
│ 24       │ the broken hearts club                               │ gnash                       │
│ 25       │ Touch                                                │ Sleeping At Last            │
│ 26       │ You're Somebody Else                                 │ flora cash                  │
│ 27       │ Moral of the Story (feat. Niall Horan) - Bonus Track │ Ashe, Niall Horan           │
│ 28       │ Oblivion                                             │ Bastille                    │
│ 29       │ Little Do You Know                                   │ Alex & Sierra               │
│ 30       │ Please Notice                                        │ Christian Leave             │
│ 31       │ White Blood                                          │ Oh Wonder                   │
│ 32       │ One Day                                              │ Tate McRae                  │
│ 33       │ That's Us                                            │ Anson Seabra                │
│ 34       │ Saturn                                               │ Sleeping At Last            │
│ 35       │ hate u love u                                        │ Olivia O'Brien              │
│ 36       │ What A Time (feat. Niall Horan)                      │ Julia Michaels, Niall Horan │
│ 37       │ Deep End                                             │ Birdy                       │
│ 38       │ Brother - Acoustic                                   │ Kodaline                    │
└──────────┴──────────────────────────────────────────────────────┴─────────────────────────────┘
```