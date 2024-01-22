-- Keep a log of any SQL queries you execute as you solve the mystery.

sqlite3 fiftyville.db
.tables
.schema


-- To start of I want to know what we working with here.
SELECT COUNT(name) FROM people;

-- Okey, 200 people dosent seem to many.
-- Im given a Hint to start with the crime reports. And date + location. Im thinking trying to match that with fligts or bank accounts, lets take a look.

SELECT COUNT(id) FROM crime_scene_reports;

--  301 ids, eh thats alot, so we know "that the theft took place on July 28, 2021 and that it took place on Humphrey Street."
-- lets start by year
 SELECT COUNT(id) FROM crime_scene_reports WHERE year = '2021';
 SELECT year FROM crime_scene_reports WHERE year = '2021';

 -- okey, they all from 2021
SELECT count(id) FROM crime_scene_reports WHERE month = 7;

 -- because the month is a int, I figured it would be stored in 7. Im still not sure and abit exited to se whats in th discription so lets read one.

SELECT description FROM crime_scene_reports WHERE id = 300;

-- so its just a small string of text with the time, not month. Lets se if we can find the right one anyway.

SELECT count(id) FROM crime_scene_reports WHERE month = 7 AND day = 28;
-- we are down to 5 reports, we could just read all five, something else might happend that day that could give us a clue.
-- I will print the street names aswell so we know witch one is the right one.

SELECT id, street, description FROM crime_scene_reports WHERE month = 7 AND day = 28;

-- There it is, lets get rid of the others

SELECT id, street, description FROM crime_scene_reports WHERE AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- okey we know the ID 295 of the report, 3 witnesses and something about the bakery.
-- So the bakery have securitys logs. Lets see what we can find that day.

SELECT * FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28;

-- lets get rid of everything before the robery

SELECT * FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour >= 10;

-- im not tealy sure what to do with the license plats, lets se if any wittneses picked up anything related to the plats or time.


SELECT * FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- so Ruth says the car left the parking lot with in 10 minutes of the thefts, that helps alot.
-- Egene says the robber withdraw money at Leggett Street the same day
-- Raymond says the robber calls someone when leving the robbery
-- Raymond says the robber wants to take the erliest flight, day after the robbery, some one else buys the ticket

-- THere are some alternativ steps to take here.
-- We know the robber left the parkinglot in one of the cars license plates with ID 260-267.
-- Lets match the owner of those with the withdraws erlier that day.

SELECT license_plate FROM bakery_security_logs WHERE id BETWEEN 260 AND 267;

SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE id BETWEEN 260 AND 267);
-- Here is our first list of suspects.

-- Lets try to get the names of the atm withdraws and then compare them with the cars that left the parkinglot.
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

SELECT name
FROM people
        WHERE id IN (
            SELECT person_id
            FROM bank_accounts
            WHERE account_number IN (
                SELECT account_number
                FROM atm_transactions
                WHERE year = 2021
                AND month = 7
                AND day = 28
                AND atm_location = 'Leggett Street'
                AND transaction_type = 'withdraw'));

-- Here is our secound list of suspects
-- lets make the list smaller by comparing the names
SELECT name
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw')
)
    AND license_plate IN (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE id BETWEEN 260 AND 267);
-- Here is my list of 4 suspects. Alltho ive been thinking all along the car could belong to someone else.
-- We can now view calls or flights. Lets start with calls. I can look up calls that day, and look for a matching susspect

SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28;

-- so here are both caller and resiver. My sql line is begining to become long.

SELECT name, phone_number
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw')
)
    AND license_plate IN (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE id BETWEEN 260 AND 267)
    AND phone_number IN (
        SELECT caller
        FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28);


SELECT *
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw')
)
    AND license_plate IN (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE id BETWEEN 260 AND 267)
    AND phone_number IN (
        SELECT caller
        FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28
        UNION ALL
        SELECT receiver
        FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28);

-- There we have Diana, as a caller and Bruce as a reciver. And they both withdraw money and left the parking lot.
-- lets figure out who was on the plane and where they were going.

SELECT * FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY(hour);

-- THis is the erliest fligt the 29th

SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY(hour) LIMIT 1);

-- I cant match any passport nummber with my two susspects, disepointing


SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE id = 4);

-- Just reliesed that they have difrent take of airports :)


SELECT * FROM airports WHERE id IN (SELECT origin_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29) AND city = 'Fiftyville';
SELECT * FROM airports WHERE id IN (SELECT destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY(hour) LIMIT 1);

-- So we know the thef left from FFiftyville going to New York..

SELECT passport_number
FROM passengers
WHERE flight_id IN (
    SELECT id
    FROM flights
    WHERE
        year = 2021
        AND month = 7
        AND day = 28
        AND origin_airport_id = (
            SELECT id
            FROM airports
            WHERE city = 'Fiftyville')ORDER BY(hour) LIMIT 1);

-- Another list but still no of the two suspects on it.
-- jsut relies ive mixed up the days :(
SELECT *
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw')
)
    AND license_plate IN (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE id BETWEEN 260 AND 267)
    AND phone_number IN (
        SELECT caller
        FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60
        UNION ALL
        SELECT receiver
        FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60 );

-- ran this again with correct calling day, now we have 3 suspects instead of two


SELECT passport_number
FROM passengers
WHERE flight_id IN (
    SELECT id
    FROM flights
    WHERE
        year = 2021
        AND month = 7
        AND day = 29
        AND origin_airport_id = (
            SELECT id
            FROM airports
            WHERE city = 'Fiftyville')ORDER BY(hour) LIMIT 1);

-- Both Bruce and Luca where on the plane :S
-- If we assume the winess is correct and the susspect is the caller, I will figure out who is the caller and who is the reciver.

SELECT *
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw')
)
    AND license_plate IN (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE id BETWEEN 260 AND 267)
    AND phone_number IN (
        SELECT caller
        FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60);

-- Bruce is the caller and he is most likely the thef. Diana is the reciver of the call and on the plane with him to new york and there for a accomplice.
-- Ran check cs50 and something is worng. I belive Bruce is the thef but I think I got the part wrong who he called. Luca recives a call and is on the plane. But its not 100% he recives the call from bruce.


SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60 AND caller = '(367) 555-5533';

-- Here is the call.
SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60 AND caller = '(367) 555-5533';
-- reciver is (375) 555-8161
SELECT * FROM people WHERE phone_number = '(375) 555-8161';
-- And its Robin, not a name ive seen before.
