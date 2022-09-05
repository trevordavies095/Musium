# Musium

Musium is an attempt to track album scores based on your track ratings.

## The Forumla

$\lfloor \left (\left (\frac{Sum of track ratings}{Total Number of Tracks} \cdot 10  \right ) + .15  \right ) \cdot 10 \rfloor$

## Commands

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