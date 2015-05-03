import json
import re


почеток = re.compile(r".*Разговор помеѓу ([\w-]+\s[\w-]+) и ([\w-]+\s[\w-]+).*",
                     flags=re.UNICODE&re.IGNORECASE)


class Пуч:
    def __repr__(пуч):
        return пуч.__unicode__()

    def __iter__(пуч):
        return iter(пуч.__dict__.items())


class Личност(Пуч):
    def __init__(личност, име_презиме):
        личност.име, личност.презиме = име_презиме.split()
        личност.иницијали = "".join([a for a in име_презиме if a.isupper()])

    def __unicode__(личност):
        return "{} {}".format(личност.име, личност.презиме)


class Разговор(Пуч):
    def __init__(разговор, наслов, текст):
        имиња = почеток.search(наслов).groups()
        assert len(имиња) == 2
        разговор.соговорници = [Личност(име_презиме) for име_презиме in имиња]
        разговор.содржина = [линија.strip() for линија in текст if
                             линија.strip() != ""]

    def __unicode__(разговор):
        return "Разговор помеѓу {} и {}".format(*разговор.соговорници)

    def __iter__(разговор):
        d = разговор.__dict__
        d['соговорници'] = [dict(с) for с in разговор.соговорници]
        return iter(d.items())


def креирај_транскрипт(име_на_датотека):
    with open(име_на_датотека, 'r') as датотека:
        разговори = []

        линија = next(датотека).strip()
        while not почеток.match(линија):
            линија = next(датотека).strip()

        наслов = линија
        текст = []
        for линија in датотека:
            if почеток.match(линија):
                разговори.append(Разговор(наслов, текст))
                наслов = линија
                текст = []
            elif линија.strip() != '':
                текст += [линија]

        разговори.append(Разговор(наслов, текст))
        наслов = линија
        return разговори


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print("ГРЕШКА: Фали бројот на бомбата.")
        print("python bomba.py 10")
        exit(-1)

    бомба = sys.argv[1]
    print("Разговори од {}-та бомба:".format(бомба))
    разговори = креирај_транскрипт('транскрипти/{}.txt'.format(бомба))

    for разговор in разговори:
        print(разговор)

    транскрипт = {'бомба': бомба, 'разговори': [dict(р) for р in разговори]}
    with open('транскрипти/{}.json'.format(бомба), 'w+') as jsonf:
        json.dump(транскрипт, jsonf)
