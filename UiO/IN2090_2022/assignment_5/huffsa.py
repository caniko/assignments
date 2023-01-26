import psycopg2

# MERK: Må kjøres med Python 3

user = 'canht' # Sett inn ditt UiO-brukernavn ("_priv" blir lagt til under)
pwd = 'random123' # Sett inn passordet for _priv-brukeren du fikk i en mail

connection = \
    "dbname='" + user + "' " +  \
    "user='" + user + "_priv' " + \
    "port='5432' " +  \
    "host='dbpg-ifi-kurs03.uio.no' " + \
    "password='" + pwd + "'"

def huffsa():
    conn = psycopg2.connect(connection)
    
    ch = 0
    while (ch != 3):
        print("--[ HUFFSA ]--")
        print("Vennligst velg et alternativ:\n 1. Søk etter planet\n 2. Legg inn forsøksresultat\n 3. Avslutt")
        ch = int(input("Valg: "))

        if (ch == 1):
            planet_sok(conn)
        elif (ch == 2):
            legg_inn_resultat(conn)
    
def planet_sok(conn):
    # Oppg 1
    print("--[ PLANET-SØK ]--")
    m1 = input("Molekyl 1: ")
    if not m1:
        msg = "Molekyl 1 must be defined!"
        raise ValueError(msg)

    m2 = input("Molekyl 2: ") or ""

    molecule_query_text = (
        f"WHERE molekyl IN ('{m1}', '{m2}') "
        f"GROUP BY planet "
        f"HAVING COUNT(distinct molekyl) = 2"
    ) if m2 else f"WHERE molekyl = '{m1}'"

    cursor = conn.cursor()
    cursor.execute(f"""
WITH
    filtered_molecule AS (
        SELECT planet FROM materie AS m
        {molecule_query_text}
    )
SELECT p.navn, p.masse, s.masse, s.avstand, p.liv
FROM filtered_molecule AS m
INNER JOIN planet AS p
    ON m.planet = p.navn
INNER JOIN stjerne AS s
    ON p.stjerne = s.navn;
""")

    for planet_name, planet_mass, star_mass, star_distance, has_life in cursor.fetchall():
        print((
            f"--Planet--\n"
            f"Navn: {planet_name}\n"
            f"Planet-masse: {planet_mass}\n"
            f"Stjerne-masse: {star_mass}\n"
            f"Stjerne-distance: {star_distance}\n"
            f"Bekreftet liv: {'Ja' if has_life else 'Nei'}\n"
        ))

    cursor.close()


def legg_inn_resultat(conn):
    # Oppg 2
    def sql_bool(norweigan_bool: bool):
        return 'true' if norweigan_bool.lower() == 'j' else 'false'

    planet_name = input("Planet: ")
    scary = sql_bool(input("Skummel: "))
    intelligent = sql_bool(input("Intelligent: "))
    description = input("Beskrivelse: ")

    print((
        f"--[ LEGG INN RESULTAT ]--"
        f"Planet: {planet_name}\n"
f"Skummel: {scary}\n"
f"Intelligent: {intelligent}\n"
f"Beskrivelse: {description}\n"
    ))

    cursor = conn.cursor()
    cursor.execute(f"""
UPDATE planet
SET
    skummel = {scary},
    intelligent = {intelligent},
    beskrivelse = '{description}'
WHERE
    navn = '{planet_name}';
""")

    conn.commit()
    cursor.close()

    print("Resultat lagt inn.")


if __name__ == "__main__":
    huffsa()
