# Musium

Musium is an attempt to track album scores based on your track ratings.

This is the article that inspired me to create this: https://isthishowyoupop.com/album-scores-and-how-they-work/

## The Forumla

$\lfloor \left (\left (\frac{Sum of track ratings}{Total Number of Tracks} \cdot 10  \right ) + Album Bonus  \right ) \cdot 10 \rfloor$

### Track Ratings
* 1   - A track that comes to mind when you think of the album, you love this track.
* .75 - A good track from the album, you like this track.
* .5  - A track that you would only listen to when listening to the album, you may consider this track "filler"
* 0 - A track you would never want to listen to again.

## Setup
```console
pip install -r requirements.txt
```

## Config
* dbpath (Required) - The directory your Musium.db is stored. If one doesn't exist in this path it will be created.
* bonus (Required) - Extra points added to an album with the logic that if every track on an album was a track you liked, it would be ~80. Default is .5, I have my changed to .15

## Commands
Example of rating an album:
```console
$ python3 musium.py
Artist > Simon & Garfunkel
Album > Bookends
Year > 1968

Artist: Simon & Garfunkel
Album: Bookends (1968)
-------------------------------------------
A1. Bookends Theme
A2. Save the Life of My Child
A3. America
A4. Overs
A5. Voices of Old People
A6. Old Friends
A7. Bookends Theme
B1. Fakin’ It
B2. Punky’s Dilemma
B3. Mrs. Robinson
B4. A Hazy Shade of Winter
B5. At the Zoo

[C]orrect? c
A1. Bookends Theme score: .5
A2. Save the Life of My Child score: 1
A3. America score: 1
A4. Overs score: .75
A5. Voices of Old People score: .5
A6. Old Friends score: 1
A7. Bookends Theme score: .5
B1. Fakin’ It score: 1
B2. Punky’s Dilemma score: 1
B3. Mrs. Robinson score: 1
B4. A Hazy Shade of Winter score: .75
B5. At the Zoo score: 1
-------------------------------------------
Score: 84
Stars: 4.0
```

### Basic album search and rating
```console
python3 musium.py
```

#### You are able to bypass searching by passing in a MusicBrainz Release ID
```console
python3 musium.py --mb "8d44b76f-a05b-434b-9781-79b60b0d5253"
```

### Basic reporting
```console
python3 musium.py -ar "Simon & Garfunkel"
python3 musium.py -ar "Simon & Garfunkel" -al "Bridge Over Troubled Water"
python3 musium.py -y 2022
python3 musium.py -d 2010s
python3 musium.py -at
```