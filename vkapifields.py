# -*- coding :  utf-8 -*-

class VKFIELDS: 
    def __init__(self): 
        self.REQ_LIST = ['id', 'first_name', 'last_name', 'about', 'activities', 'bdate', 'books', 'career', 'city', 
                         'country', 'followers_count', 'games', 'home_town', 'interests', 'movies','music',
                         'occupation', 'personal', 'quotes', 'relation', 'schools', 'sex', 'tv', 'universities']
        
        self.AUDIO_LIST = ['id', 'artist', 'title', 'duration']


        self.USERS = {'personal' : {'political' : {
                                    1 : 'коммунистические',
                                    2 : 'социалистические',
                                    3 : 'умеренные',
                                    4 : 'либеральные',
                                    5 : 'консервативные',
                                    6 : 'монархические',
                                    7 : 'ультраконсервативные',
                                    8 : 'индифферентные',
                                    9 : 'либертарианские'
                                    },
                                    'people_main' : {
                                    1 : 'ум и креативность',
                                    2 : 'доброта и честность',
                                    3 : 'красота и здоровье',
                                    4 : 'власть и богатство',
                                    5 : 'смелость и упорство',
                                    6 : 'юмор и жизнелюбие'
                                    },
                                    'life_main ' : {                    
                                    1 : 'семья и дети',
                                    2 : 'карьера и деньги',
                                    3 : 'развлечения и отдых',
                                    4 : 'наука и исследования',
                                    5 : 'совершенствование мира',
                                    6 : 'саморазвитие',
                                    7 : 'красота и искусство',
                                    8 : 'слава и влияние'
                                    },
                                    'smoking' : {    
                                    1 : 'резко негативное',
                                    2 : 'негативное',
                                    3 : 'компромиссное',
                                    4 : 'нейтральное',
                                    5 : 'положительное'
                                    },
                                    'alcohol' : {
                                    1 : 'резко негативное',
                                    2 : 'негативное',
                                    3 : 'компромиссное',
                                    4 : 'нейтральное',
                                    5 : 'положительное'
                                    }},
                    'relation' : {
                    1 : 'не женат/не замужем',
                    2 : 'есть друг/есть подруга',
                    3 : 'помолвлен/помолвлена',
                    4 : 'женат/замужем',
                    5 : 'всё сложно',
                    6 : 'в активном поиске',
                    7 : 'влюблён/влюблена',
                    8 : 'в гражданском браке',
                    0 : 'не указано'
                    },
                    'sex' : {
                    1 : 'женский',
                    2 : 'мужской',
                    0 : 'пол не указан'
                    }}

        self.AUDIO_GENRE = {
                1 : 'Rock',
                2 : 'Pop',
                3 : 'Rap & Hip-Hop',
                4 : 'Easy Listening',
                5 : 'House & Dance',
                6 : 'Instrumental',
                7 : 'Metal',
                21 : 'Alternative',
                8 : 'Dubstep',
                1001 : 'Jazz & Blues',
                10 : 'Drum & Bass',
                11 : 'Trance',
                12 : 'Chanson',
                13 : 'Ethnic',
                14 : 'Acoustic & Vocal',
                15 : 'Reggae',
                16 : 'Classical',
                17 : 'Indie Pop',
                19 : 'Speech',
                22 : 'Electropop & Disco',
                18 : 'Other'
                }