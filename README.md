# Musium

Musium is an attempt to track album scores based on your track ratings.

## The Forumla

$\lfloor \left (\left (\frac{Sum of track ratings}{Total Number of Tracks} \cdot 10  \right ) + .15  \right ) \cdot 10 \rfloor$

### Track Ratings
* 1   - A track that comes to mind when you think of the album, you love this track.
* .75 - A good track from the album, you like this track.
* .5  - A track that you would only listen to when listening to the album, you may consider this track "filler"
* 0 - A track you would never want to listen to again.

## Commands
Example of rating an album:
```
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
Stars: 4.0```

### Basic album search and rating
```console
python3 Musium.py
```

#### You are able to bypass searching by passing in a MusicBrainz Release ID
```console
python3 Musium.py --mb "8d44b76f-a05b-434b-9781-79b60b0d5253"
```

### Basic reporting
```console
python3 Musium.py -ar "Simon & Garfunkel"
python3 Musium.py -ar "Simon & Garfunkel" -al "Bridge Over Troubled Water"
python3 Musium.py -y 2022
python3 Musium.py -d 2010s
```