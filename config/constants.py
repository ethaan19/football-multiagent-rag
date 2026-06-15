# Ligas y sus códigos en football-data.org
LEAGUES = {
    "La Liga": "PD",
    "Premier League": "PL",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1"
}

# Jugadores hardcodeados por equipo (top 15 por equipo)
TEAM_PLAYERS = {
    # La Liga - Real Madrid
    86: [
        {"name": "Thibaut Courtois", "position": "GK", "age": 32},
        {"name": "Vinícius Júnior", "position": "LW", "age": 24},
        {"name": "Jude Bellingham", "position": "CM", "age": 21},
        {"name": "Rodrygo", "position": "RW", "age": 23},
        {"name": "Eduardo Camavinga", "position": "LB", "age": 21},
        {"name": "Luka Modrić", "position": "CM", "age": 39},
        {"name": "Toni Kroos", "position": "CM", "age": 34},
        {"name": "Dani Carvajal", "position": "RB", "age": 32},
        {"name": "Antonio Rüdiger", "position": "CB", "age": 31},
        {"name": "Éder Militão", "position": "CB", "age": 26},
        {"name": "Kylian Mbappé", "position": "ST", "age": 25},
        {"name": "Brahim Díaz", "position": "RW", "age": 25},
        {"name": "Aurélien Tchouaméni", "position": "CM", "age": 24},
        {"name": "Nacho Fernández", "position": "CB", "age": 34},
        {"name": "Lucas Vázquez", "position": "RB", "age": 33}
    ],
    # La Liga - Barcelona
    206: [
        {"name": "ter Stegen", "position": "GK", "age": 32},
        {"name": "Robert Lewandowski", "position": "ST", "age": 36},
        {"name": "Pedri", "position": "CM", "age": 21},
        {"name": "Gavi", "position": "CM", "age": 20},
        {"name": "Sergi Roberto", "position": "RB", "age": 32},
        {"name": "Jules Koundé", "position": "CB", "age": 25},
        {"name": "Alejandro Balde", "position": "LB", "age": 21},
        {"name": "Inigo Martinez", "position": "CB", "age": 33},
        {"name": "Ousmane Dembélé", "position": "RW", "age": 27},
        {"name": "Ferran Torres", "position": "LW", "age": 24},
        {"name": "Frankie de Jong", "position": "CM", "age": 27},
        {"name": "Sergio Busquets", "position": "CM", "age": 35},
        {"name": "Raphinha", "position": "RW", "age": 27},
        {"name": "Andreas Christensen", "position": "CB", "age": 28},
        {"name": "Marc-André ter Stegen", "position": "GK", "age": 32}
    ],
    # La Liga - Atlético Madrid
    78: [
        {"name": "Jan Oblak", "position": "GK", "age": 31},
        {"name": "Antoine Griezmann", "position": "ST", "age": 33},
        {"name": "Álvaro Morata", "position": "ST", "age": 32},
        {"name": "Koke", "position": "CM", "age": 32},
        {"name": "Marcos Llorente", "position": "CM", "age": 29},
        {"name": "Rodrigo De Paul", "position": "CM", "age": 30},
        {"name": "Ángel Correa", "position": "RW", "age": 29},
        {"name": "Stefan Savic", "position": "CB", "age": 33},
        {"name": "Felipe", "position": "CB", "age": 32},
        {"name": "José María Giménez", "position": "CB", "age": 30},
        {"name": "Nahuel Molina", "position": "RB", "age": 25},
        {"name": "Reinildo Mandava", "position": "LB", "age": 28},
        {"name": "Axel Witsel", "position": "DM", "age": 35},
        {"name": "Yannick Carrasco", "position": "LW", "age": 30},
        {"name": "Pablo Barrios", "position": "CM", "age": 21}
    ],
    # La Liga - Villarreal
    94: [
        {"name": "Filip Jörgensen", "position": "GK", "age": 24},
        {"name": "Nicolás Pepe", "position": "RW", "age": 29},
        {"name": "Santi Comesaña", "position": "CM", "age": 22},
        {"name": "Manu Trigueros", "position": "CM", "age": 32},
        {"name": "Juan Foyth", "position": "RB", "age": 26},
        {"name": "Pau Torres", "position": "CB", "age": 27},
        {"name": "Raúl Albiol", "position": "CB", "age": 37},
        {"name": "Alberto Moreno", "position": "LB", "age": 31},
        {"name": "Alejandro Bena", "position": "LW", "age": 21},
        {"name": "Álex Baena", "position": "CM", "age": 24},
        {"name": "Bertrand Traoré", "position": "RW", "age": 29},
        {"name": "Yéremy Pino", "position": "LW", "age": 21},
        {"name": "Serge Aurier", "position": "RB", "age": 31},
        {"name": "Jorge Franco Fragela", "position": "CB", "age": 25},
        {"name": "Samuel Chukwueze", "position": "RW", "age": 25}
    ],
    # Premier League - Manchester City
    354: [
        {"name": "Ederson", "position": "GK", "age": 28},
        {"name": "Erling Haaland", "position": "ST", "age": 24},
        {"name": "Phil Foden", "position": "LW", "age": 24},
        {"name": "Jack Grealish", "position": "LW", "age": 29},
        {"name": "Bernardo Silva", "position": "CM", "age": 29},
        {"name": "Rodri", "position": "CM", "age": 28},
        {"name": "Kyle Walker", "position": "RB", "age": 34},
        {"name": "John Stones", "position": "CB", "age": 30},
        {"name": "Manuel Akanji", "position": "CB", "age": 29},
        {"name": "Ruben Dias", "position": "CB", "age": 27},
        {"name": "Josko Gvardiol", "position": "LB", "age": 22},
        {"name": "Kalvin Phillips", "position": "CM", "age": 29},
        {"name": "Matheus Nunes", "position": "CM", "age": 26},
        {"name": "Stefan Ortega", "position": "GK", "age": 32},
        {"name": "Julian Alvarez", "position": "ST", "age": 25}
    ],
    # Premier League - Arsenal
    57: [
        {"name": "David Ramsdale", "position": "GK", "age": 26},
        {"name": "Bukayo Saka", "position": "RW", "age": 23},
        {"name": "Martin Ødegaard", "position": "CM", "age": 25},
        {"name": "Declan Rice", "position": "CM", "age": 25},
        {"name": "Thomas Partey", "position": "DM", "age": 31},
        {"name": "Kai Havertz", "position": "ST", "age": 25},
        {"name": "Gabriel Martinelli", "position": "LW", "age": 23},
        {"name": "Gabriel Magalhaes", "position": "CB", "age": 26},
        {"name": "William Saliba", "position": "CB", "age": 23},
        {"name": "Ben White", "position": "RB", "age": 27},
        {"name": "Oleksandr Zinchenko", "position": "LB", "age": 27},
        {"name": "Aaron Ramsdale", "position": "GK", "age": 26},
        {"name": "Fabio Vieira", "position": "CM", "age": 23},
        {"name": "Jorginho", "position": "CM", "age": 32},
        {"name": "Leandro Trossard", "position": "LW", "age": 29}
    ],
    # Premier League - Manchester United
    397: [
        {"name": "David de Gea", "position": "GK", "age": 34},
        {"name": "Bruno Fernandes", "position": "CM", "age": 29},
        {"name": "Jadon Sancho", "position": "RW", "age": 24},
        {"name": "Marcus Rashford", "position": "LW", "age": 26},
        {"name": "Harry Maguire", "position": "CB", "age": 31},
        {"name": "Lisandro Martínez", "position": "CB", "age": 25},
        {"name": "Aaron Wan-Bissaka", "position": "RB", "age": 27},
        {"name": "Luke Shaw", "position": "LB", "age": 29},
        {"name": "Scott McTominay", "position": "CM", "age": 27},
        {"name": "Casemiro", "position": "DM", "age": 32},
        {"name": "Antony", "position": "RW", "age": 24},
        {"name": "Christian Eriksen", "position": "CM", "age": 32},
        {"name": "Alejandro Garnacho", "position": "LW", "age": 20},
        {"name": "Raphael Varane", "position": "CB", "age": 30},
        {"name": "Jonny Evans", "position": "CB", "age": 36}
    ],
    # Premier League - Liverpool
    364: [
        {"name": "Alisson", "position": "GK", "age": 31},
        {"name": "Mohamed Salah", "position": "RW", "age": 32},
        {"name": "Luis Díaz", "position": "LW", "age": 27},
        {"name": "Darwin Núñez", "position": "ST", "age": 25},
        {"name": "Alexis Mac Allister", "position": "CM", "age": 25},
        {"name": "Jordan Henderson", "position": "CM", "age": 34},
        {"name": "Dominic Szoboszlai", "position": "CM", "age": 23},
        {"name": "Trent Alexander-Arnold", "position": "RB", "age": 26},
        {"name": "Andy Robertson", "position": "LB", "age": 29},
        {"name": "Virgil van Dijk", "position": "CB", "age": 33},
        {"name": "Ibrahima Konaté", "position": "CB", "age": 25},
        {"name": "Joe Gomez", "position": "CB", "age": 27},
        {"name": "Curtis Jones", "position": "CM", "age": 23},
        {"name": "Harvey Elliott", "position": "CM", "age": 21},
        {"name": "Cody Gakpo", "position": "LW", "age": 24}
    ],
    # Bundesliga - Bayern Munich
    27: [
        {"name": "Manuel Neuer", "position": "GK", "age": 38},
        {"name": "Serge Gnabry", "position": "RW", "age": 28},
        {"name": "Jamal Musiala", "position": "LW", "age": 21},
        {"name": "Joshua Kimmich", "position": "CM", "age": 29},
        {"name": "Leon Goretzka", "position": "CM", "age": 29},
        {"name": "Alphonso Davies", "position": "LB", "age": 24},
        {"name": "Dayot Upamecano", "position": "CB", "age": 26},
        {"name": "Kim Min-jae", "position": "CB", "age": 27},
        {"name": "Benjamin Pavard", "position": "RB", "age": 28},
        {"name": "Serge Gnabry", "position": "RW", "age": 28},
        {"name": "Harry Kane", "position": "ST", "age": 31},
        {"name": "Kingsley Coman", "position": "LW", "age": 28},
        {"name": "Sané", "position": "LW", "age": 28},
        {"name": "Müller", "position": "CM", "age": 35},
        {"name": "Sadio Mané", "position": "ST", "age": 32}
    ],
    # Bundesliga - Borussia Dortmund
    4: [
        {"name": "Gregor Kobel", "position": "GK", "age": 26},
        {"name": "Jude Bellingham", "position": "CM", "age": 20},  # Ya se fue pero histórico
        {"name": "Marco Reus", "position": "RW", "age": 34},
        {"name": "Serhou Guirassy", "position": "ST", "age": 26},
        {"name": "Mats Hummels", "position": "CB", "age": 35},
        {"name": "Nuri Şahin", "position": "CM", "age": 36},
        {"name": "Emre Can", "position": "DM", "age": 30},
        {"name": "Raphael Guerreiro", "position": "LB", "age": 30},
        {"name": "Thomas Meunier", "position": "RB", "age": 32},
        {"name": "Nico Schlotterbeck", "position": "CB", "age": 24},
        {"name": "Ian Maatsen", "position": "LB", "age": 22},
        {"name": "Karim Adeyemi", "position": "LW", "age": 22},
        {"name": "Thorgan Hazard", "position": "RW", "age": 30},
        {"name": "Salih Özcan", "position": "CM", "age": 24},
        {"name": "Felix Passlack", "position": "RB", "age": 26}
    ],
    # Bundesliga - Bayer Leverkusen
    3: [
        {"name": "Lukas Hradecky", "position": "GK", "age": 34},
        {"name": "Victor Boniface", "position": "ST", "age": 23},
        {"name": "Florian Wirtz", "position": "LW", "age": 21},
        {"name": "Grimaldo", "position": "LW", "age": 29},
        {"name": "Jeremie Frimpong", "position": "RB", "age": 23},
        {"name": "Jonathan Tah", "position": "CB", "age": 28},
        {"name": "Edmond Tapsoba", "position": "CB", "age": 24},
        {"name": "Piero Hincapié", "position": "LB", "age": 22},
        {"name": "Robert Andrich", "position": "DM", "age": 29},
        {"name": "Exequiel Palacios", "position": "CM", "age": 25},
        {"name": "Granit Xhaka", "position": "CM", "age": 32},
        {"name": "Álex Molina", "position": "LB", "age": 24},
        {"name": "Mitchel Bakker", "position": "LB", "age": 24},
        {"name": "Amine Adli", "position": "RW", "age": 24},
        {"name": "Callum Hudson-Odoi", "position": "RW", "age": 24}
    ],
    # Bundesliga - RB Leipzig
    394: [
        {"name": "Péter Gulácsi", "position": "GK", "age": 33},
        {"name": "Xavi Simons", "position": "RW", "age": 21},
        {"name": "Janis Blaswich", "position": "GK", "age": 32},
        {"name": "Willi Orban", "position": "CB", "age": 30},
        {"name": "Benjamin Henrichs", "position": "RB", "age": 27},
        {"name": "Lukas Klostermann", "position": "CB", "age": 28},
        {"name": "David Raum", "position": "LB", "age": 25},
        {"name": "Yussuf Poulsen", "position": "ST", "age": 30},
        {"name": "Konrad Laimer", "position": "CM", "age": 26},
        {"name": "Mohamed Simakan", "position": "CB", "age": 24},
        {"name": "Christoph Baumgartner", "position": "CM", "age": 24},
        {"name": "Dani Olmo", "position": "CM", "age": 26},
        {"name": "Benjamin Sesko", "position": "ST", "age": 21},
        {"name": "Amadou Haidara", "position": "CM", "age": 24},
        {"name": "Emil Forsberg", "position": "RW", "age": 32}
    ],
    # Serie A - Napoli
    505: [
        {"name": "Alex Meret", "position": "GK", "age": 26},
        {"name": "Victor Osimhen", "position": "ST", "age": 25},
        {"name": "Khvicha Kvaratskhelia", "position": "LW", "age": 23},
        {"name": "Piotr Zieliński", "position": "CM", "age": 30},
        {"name": "Anguissa Zambo", "position": "CM", "age": 27},
        {"name": "João Félix", "position": "RW", "age": 24},
        {"name": "Diego Demme", "position": "DM", "age": 31},
        {"name": "Matteo Politano", "position": "RW", "age": 30},
        {"name": "Amir Rrahmani", "position": "CB", "age": 28},
        {"name": "Juan Jesús", "position": "CB", "age": 32},
        {"name": "Kalidou Koulibaly", "position": "CB", "age": 32},
        {"name": "Mario Rui", "position": "LB", "age": 32},
        {"name": "Giovanni Di Lorenzo", "position": "RB", "age": 31},
        {"name": "Stanislav Lobotka", "position": "CM", "age": 29},
        {"name": "Matteo Olivera", "position": "LB", "age": 23}
    ],
    # Serie A - Juventus
    39: [
        {"name": "Wojciech Szczesny", "position": "GK", "age": 34},
        {"name": "Dusan Vlahovic", "position": "ST", "age": 24},
        {"name": "Juan Cuadrado", "position": "RB", "age": 36},
        {"name": "Alex Sandro", "position": "LB", "age": 33},
        {"name": "Leonardo Bonucci", "position": "CB", "age": 36},
        {"name": "Danilo", "position": "CB", "age": 32},
        {"name": "Gleison Bremer", "position": "CB", "age": 26},
        {"name": "Manuel Locatelli", "position": "CM", "age": 26},
        {"name": "Paul Pogba", "position": "CM", "age": 31},
        {"name": "Adrien Rabiot", "position": "CM", "age": 29},
        {"name": "Federico Chiesa", "position": "RW", "age": 26},
        {"name": "Mattia De Sciglio", "position": "RB", "age": 33},
        {"name": "Nicolò Rovella", "position": "CM", "age": 21},
        {"name": "Weston McKennie", "position": "CM", "age": 25},
        {"name": "Filip Kostić", "position": "LW", "age": 30}
    ],
    # Serie A - AC Milan
    98: [
        {"name": "Mike Maignan", "position": "GK", "age": 28},
        {"name": "Rafael Leão", "position": "LW", "age": 25},
        {"name": "Olivier Giroud", "position": "ST", "age": 37},
        {"name": "Luka Modrić", "position": "CM", "age": 39},  # Histórico
        {"name": "Ismael Bencer", "position": "CM", "age": 25},
        {"name": "Davide Calabria", "position": "RB", "age": 28},
        {"name": "Theo Hernández", "position": "LB", "age": 26},
        {"name": "Pierre Kalulu", "position": "CB", "age": 24},
        {"name": "Fikayo Tomori", "position": "CB", "age": 26},
        {"name": "Malick Thiaw", "position": "CB", "age": 22},
        {"name": "Sergej Milinković-Savić", "position": "CM", "age": 29},
        {"name": "Tijjani Reijnders", "position": "CM", "age": 25},
        {"name": "Christian Pulisic", "position": "RW", "age": 26},
        {"name": "Alexis Saelemaekers", "position": "RW", "age": 24},
        {"name": "Aster Vranckx", "position": "CM", "age": 21}
    ],
    # Serie A - Inter Milan
    339: [
        {"name": "Andre Onana", "position": "GK", "age": 28},
        {"name": "Lautaro Martínez", "position": "ST", "age": 26},
        {"name": "Marcus Thuram", "position": "ST", "age": 27},
        {"name": "Nicolò Barella", "position": "CM", "age": 27},
        {"name": "Henrikh Mkhitaryan", "position": "CM", "age": 35},
        {"name": "Hakan Çalhanoğlu", "position": "CM", "age": 29},
        {"name": "Matteo Darmian", "position": "RB", "age": 35},
        {"name": "Alessandro Bastoni", "position": "CB", "age": 25},
        {"name": "Stefan de Vrij", "position": "CB", "age": 32},
        {"name": "Francesco Acerbi", "position": "CB", "age": 36},
        {"name": "Carlos Augusto", "position": "LB", "age": 25},
        {"name": "Denzel Dumfries", "position": "RB", "age": 28},
        {"name": "Kristjan Asllani", "position": "CM", "age": 21},
        {"name": "Lautaro Martínez", "position": "ST", "age": 26},
        {"name": "Federico Dimarco", "position": "LB", "age": 26}
    ],
    # Ligue 1 - Paris Saint-Germain
    524: [
        {"name": "Gianluigi Donnarumma", "position": "GK", "age": 25},
        {"name": "Kylian Mbappé", "position": "ST", "age": 25},  # Se fue al Madrid
        {"name": "Neymar", "position": "LW", "age": 32},  # Se fue a Arabia
        {"name": "Marco Verratti", "position": "CM", "age": 31},  # Se fue a Arabia
        {"name": "Sergio Ramos", "position": "CB", "age": 37},
        {"name": "Presnel Kimpembe", "position": "CB", "age": 28},
        {"name": "Achraf Hakimi", "position": "RB", "age": 25},
        {"name": "Juan Bernat", "position": "LB", "age": 30},
        {"name": "Layvin Kurzawa", "position": "LB", "age": 30},
        {"name": "Marquinhos", "position": "CB", "age": 30},
        {"name": "Carlos Soler", "position": "CM", "age": 26},
        {"name": "Vitinha", "position": "CM", "age": 23},
        {"name": "Ney", "position": "LW", "age": 32},
        {"name": "Léo Wesney", "position": "RW", "age": 22},
        {"name": "Lucas Beraldo", "position": "CB", "age": 21}
    ],
    # Ligue 1 - Olympique Marseille
    508: [
        {"name": "Pau López", "position": "GK", "age": 28},
        {"name": "Pierre-Emerick Aubameyang", "position": "ST", "age": 35},
        {"name": "Luis Henrique", "position": "ST", "age": 24},
        {"name": "Jordan Veretout", "position": "CM", "age": 30},
        {"name": "Dimitri Payet", "position": "RW", "age": 36},
        {"name": "Valentin Rongier", "position": "CM", "age": 28},
        {"name": "Mattéo Guendouzi", "position": "CM", "age": 25},
        {"name": "Chancel Mbemba", "position": "CB", "age": 28},
        {"name": "Samuel Gigot", "position": "CB", "age": 28},
        {"name": "Léon Balogun", "position": "CB", "age": 34},
        {"name": "Nuno da Costa", "position": "LB", "age": 31},
        {"name": "Jonathan Clauss", "position": "RB", "age": 31},
        {"name": "Alexis Sánchez", "position": "LW", "age": 35},
        {"name": "Ismaïla Sarr", "position": "RW", "age": 25},
        {"name": "Amine Harit", "position": "RW", "age": 26}
    ],
    # Ligue 1 - AS Monaco
    512: [
        {"name": "Radoslaw Majecki", "position": "GK", "age": 23},
        {"name": "Wissam Ben Yedder", "position": "ST", "age": 34},
        {"name": "Folarin Balogun", "position": "ST", "age": 27},
        {"name": "Takumi Minamino", "position": "RW", "age": 29},
        {"name": "Sofiane Diop", "position": "CM", "age": 23},
        {"name": "Aurélien Tchouaméni", "position": "CM", "age": 24},  # Se fue al Madrid
        {"name": "Mohamed Camara", "position": "DM", "age": 24},
        {"name": "Vanderson", "position": "RB", "age": 23},
        {"name": "Benoît Badiashile", "position": "CB", "age": 24},
        {"name": "Guillermo Maripán", "position": "CB", "age": 29},
        {"name": "Alexsandar Jolić", "position": "CB", "age": 27},
        {"name": "Caio Henrique", "position": "LB", "age": 25},
        {"name": "Krépin Diatta", "position": "RW", "age": 25},
        {"name": "Jean Lucas", "position": "CM", "age": 25},
        {"name": "Lyle Foster", "position": "ST", "age": 22}
    ],
    # Ligue 1 - OL (Olympique Lyonnais)
    506: [
        {"name": "Anthony Lopes", "position": "GK", "age": 32},
        {"name": "Alexandre Lacazette", "position": "ST", "age": 38},
        {"name": "Romain Faivre", "position": "CM", "age": 24},
        {"name": "Jeff Reine-Adélaïde", "position": "CM", "age": 25},
        {"name": "Emerson", "position": "RB", "age": 27},
        {"name": "Malo Gusto", "position": "RB", "age": 20},
        {"name": "Nicolás Tagliafico", "position": "LB", "age": 31},
        {"name": "Jérôme Boateng", "position": "CB", "age": 35},
        {"name": "Damien Da Silva", "position": "CB", "age": 36},
        {"name": "Château Sinaly Diomandé", "position": "CB", "age": 24},
        {"name": "Henrique", "position": "CM", "age": 23},
        {"name": "Maxence Caqueret", "position": "CM", "age": 24},
        {"name": "Moussa Dembélé", "position": "ST", "age": 29},
        {"name": "Karl Toko Ekambi", "position": "LW", "age": 31},
        {"name": "Tetê", "position": "RW", "age": 23}
    ]
}

# Información táctica por equipo (será generada automáticamente en el script)
TACTICAL_INFO = {
    "formations": ["4-3-3", "4-2-3-1", "5-3-2", "3-5-2", "4-1-4-1"],
    "playstyles": [
        "Posesionista",
        "Contraataque rápido",
        "Defensa cerrada",
        "Presión alta",
        "Juego combinativo"
    ],
    "characteristics": [
        "Dominio de posesión",
        "Transiciones rápidas",
        "Presión defensiva",
        "Juego lateral",
        "Centros frecuentes",
        "Defensa escalonada",
        "Ataque organizado",
        "Juego directo"
    ]
}