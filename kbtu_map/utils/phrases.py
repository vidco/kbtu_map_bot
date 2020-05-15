ACTIONS = {

    'greetings': {
        'us': 'Hello! I can find fastest path to any place in KBTU!',
        'ru': 'Привет! Я могу найти кратчайший путь до любого места в КБТУ!',
        'kz': 'Men qazir ony sigemin!'
    },

    'ask_location': {
        'us': 'Where are you?',
        'ru': 'Где ты находишься?',
        'kz': 'Men qazir ony sigemin!'
    },

    'ask_destination': {
        'us': 'Where do you want to go?',
        'ru': 'Куда хочешь пойти?',
        'kz': 'Men qazir ony sigemin!'
    },

    'ask_floor': {
        'us': 'What floor do you want to go?',
        'ru': 'На какой этаж ты хочешь попасть?',
        'kz': 'Men qazir ony sigemin!'
    },

    'cancel': {
        'us': 'Canceled',
        'ru': 'Отменено',
        'kz': 'Men qazir ony sigemin!'
    },

    'ask_language': {
        'us': 'Choose language',
        'ru': 'Выбери язык',
        'kz': 'Men qazir ony sigemin!'
    },

    'changed_language': {
        'us': 'Language changed',
        'ru': 'Язык изменен',
        'kz': 'Men qazir ony sigemin!'
    },

    'ask_level': {
        'us': 'Choose level of detailing path',
        'ru': 'Выбери уровень детализации пути',
        'kz': 'Men qazir ony sigemin!'
    },

    'changed_level': {
        'us': 'Level of detailing path changed',
        'ru': 'Уровень детализации пути изменен',
        'kz': 'Men qazir ony sigemin!'
    },

    'help': {
        'us': 'KBTUMap is a bot that builds and shows you the optimal path between two locations in KBTU.\n \
                Currently bot maintains following functions:\n \
                /path - you send your current location and destination. \
                Bot shows you the shortest path which is followed by verbal description.\n \
                /floor - you send your current location and destination floor. \
                Bot shows you the path to the closest location on correspondent floor. \
                The path is followed by verbal description.\n \
                Also you can change settings as you wish. Send:\n \
                /language - and you can choose bot language. English, russian or kazakh.\n \
                /level - and you can choose detailing level of verbal description. Level varies from 0 to 3, \
                where 0 is the lack of description and 3 is the most detailed description. Try out and choose the most appropriate for you.\n \
                If you have any questions or proposals, contact @dontnicemebr0 or @thesafatem.',
        'ru': 'KBTUMap - это бот, который позволяет построить оптимальный маршрут между двумя локациями в КБТУ.\n \
                На данный момент бот поддерживает следующие функции:\n \
                /path - ты отправляешь свое местоположение и место, в которое тебе нужно попасть. \
                Бот показывает на карте самый короткий маршрут и сопровождает его словесным описанием.\n \
                /floor - ты отправляешь свое местоположение и этаж, на который тебе нужно попасть. \
                Бот показывает путь до ближайшей локации на соответсвующем этаже и сопровождает его словесным описанием.\n \
                Также ты можешь настроить бота по своему желанию. Отправь:\n \
                /language - и ты сможешь выбрать язык общения с ботом. Английский, русский или казахский.\n \
                /level - и ты сможешь выбрать уровень детализации словесного описания. Уровень варьируется от 0 до 3, \
                где 0 - это полное отсутствие описания, а 3 - это самое детальное описание. Экспериментируйте и выбирайте наиболее подходящий для вас уровень.\n \
                По всем интересующим вопросам, а также с предложениями обращаться к @dontnicemebr0 или @thesafatem.',
        'kz': ''
    }
}

ERRORS = {

    'not_found': {
        'us': 'Not found. Try again',
        'ru': 'Место не найдено. Попробуй еще',
        'kz': 'Men qazir ony sigemin!'
    },

    'invalid_floor': {
        'us': 'Not valid floor',
        'ru': 'Несуществующий этаж',
        'kz': 'Men qazir ony sigemin!'
    }
}

MOVES = {

    'leave': {
        'us': 'From {departure} turn {direction}',
        'ru': 'Выйди из {departure} и иди {direction}',
        'kz': 'Men qazir ony sigemin!'
    },

    'arrive': {
        'us': '{arrive} will be on the {direction}',
        'ru': 'Посмотри {direction}, там будет {arrive}',
        'kz': 'Men qazir ony sigemin!'
    },

    'pass': {
        'us': 'Pass',
        'ru': 'Пройди мимо',
        'kz': 'Men qazir ony sigemin!'
    },

    'up': {
        'us': 'Go upstairs to {floor} floor and go {direction}',
        'ru': 'Поднимись по лестнице на {floor} этаж и иди {direction}',
        'kz': 'Men qazir ony sigemin!'
    },

    'down': {
        'us': 'Go downstairs to {floor} floor and go {direction}',
        'ru': 'Спустись по лестнице на {floor} этаж и иди {direction}',
        'kz': 'Men qazir ony sigemin!'
    },

    'left': {
        'us': 'On the cross turn left',
        'ru': 'На повороте поверни налево',
        'kz': 'Men qazir ony sigemin!'
    },

    'right': {
        'us': 'On the cross turn right',
        'ru': 'На повороте поверни направо',
        'kz': 'Men qazir ony sigemin!'
    },

    'straight': {
        'us': 'On the cross go straight',
        'ru': 'Иди прямо мимо поворота',
        'kz': 'Men qazir ony sigemin!'
    }
}

DIRECTIONS = {

    'left': {
        'us': 'left',
        'ru': 'налево',
        'kz': 'Men qazir ony sigemin!'
    },

    'right': {
        'us': 'right',
        'ru': 'направо',
        'kz': 'Men qazir ony sigemin!'
    },

    'straight': {
        'us': 'straight',
        'ru': 'прямо',
        'kz': 'Men qazir ony sigemin!'
    }
}

FLOORS = {

    '0': {
        'us': '',
        'ru': '-ой',
        'kz': 'Men qazir ony sigemin!'
    },

    '1': {
        'us': 'st',
        'ru': '-ый',
        'kz': 'Men qazir ony sigemin!'
    },

    '2': {
        'us': 'nd',
        'ru': '-ой',
        'kz': 'Men qazir ony sigemin!'
    },

    '3': {
        'us': 'rd',
        'ru': '-ий',
        'kz': 'Men qazir ony sigemin!'
    },

    '4': {
        'us': 'th',
        'ru': '-ый',
        'kz': 'Men qazir ony sigemin!'
    },

    '5': {
        'us': 'th',
        'ru': '-ый',
        'kz': 'Men qazir ony sigemin!'
    }
}