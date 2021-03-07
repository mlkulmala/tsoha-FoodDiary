# Käyttöohje

## Kirjautuminen ja rekisteröityminen

Sovellus avautuu näkymään, jossa sen toiminta esitellään lyhyesti ja käyttäjä ohjataan kirjautumaan tai 
rekisteröitymään käyttäjäksi.

Sovellus ilmoittaa, jos käyttäjänimi on liian lyhyt tai jo käytössä, tai jos salasana ei täytä kriteerejä 
tai salasanan vahvistus ei täsmää.

<img src="https://github.com/mlkulmala/tsoha-FoodDiary/blob/master/documentation/images/login.png" width="300">


## Omien tietojen täyttäminen

Uuden käyttäjät ohjataan heti kirjautumisen jälkeen Omiin tietoihin, missä käyttäjä voi kirjata tietoja itsestään 
(sukupuoli, ikä, pituus, paino sekä arvio aktiivisuustasosta), joiden perusteella sovellus laskee arvion 
päivittäisestä kalorintarpeesta. 

Vaihtoehtoisesti käyttäjä voi itse määrittää arvon päivittäin tavoiteltavalle kalorimäärälle. 

Valintoja voi käydä muuttamassa Omista tiedoista. Kunkin päivän kohdalle jää talteen viimeksi valittu laskutapa ja 
kalorimäärä. Painon tai oman aktiivisuuden muuttuessa voi kalorintarve vaihdella.

<img src="https://github.com/mlkulmala/tsoha-FoodDiary/blob/master/documentation/images/set_goal.png" width="600">


## Ruokapäiväkirja

Sisäänkirjautumisen jälkeen käyttäjä ohjataan suoraan ruokapäiväkirjan täyttöön. 

Jos käyttäjällä on ruokapäiväkirjassa merkintöjä, ne näkyvät näkymässä taulukkona aterian mukaan ryhmiteltynä. Kullakin 
rivillä näkyy syödyn ruoan nimi, määrä sekä annoskohtaiset ravintoaineiden määrät.

Oikealla näkyy yhteenveto, joka päivittyy jokaisen ruokapäiväkirjamerkinnän lisäyksen jälkeen. Yhteenvedossa on nähtävissä 
tähän asti saadun energian määrä, päiväkohtainen tavoite sekä paljonko tavoitteesta vielä puuttuu. Lisäksi 
yhteenvedossa on eri ravintoaineiden osuudet päivän energiansaannista sekä näiden osuuksien suositusarvot. 

<img src="https://github.com/mlkulmala/tsoha-FoodDiary/blob/master/documentation/images/food_search.png" width="600">


## Omien ruokien lisääminen

Jos käyttäjä ei löydä hakemaansa ruoka-ainetta, hän voi lisätä myös omia ruokiaan tai suosikkituotteitaan. Käyttäjän
lisäämät ruoka-aineet näkyvät vain hänelle itselleen, jolloin hän vastaa vain itselleen tietojen oikeellisuudesta.


## Arkisto

Vanhat ruokapäiväkirjat ovat katseltavissa arkistossa. Näkymä on samantyyppinen kuin ruokapäiväkirjan täytössäkin: syötyjen 
ruokien lisäksi yhteenvedosta näkee, miten sille päivälle asetettu tavoite on täyttynyt ja miten ravintoaineet ovat
jakautuneet.


## Kehitettävää

Arkistoon jäi lisäämättä ominaisuus, jossa ruokapäiväkirjamerkintöjä voi muuttaa. Tällä hetkellä poistomahdollisuus on olemassa
vain kuluvan päivän ruokapäiväkirjamerkinnöissä.

Omien ruokien lisääminen onnistuu nyt vain ruoka-ainehaun kautta. Sillekin voisi lisätä oman linkin vaikka navigaatiopalkkiin.

