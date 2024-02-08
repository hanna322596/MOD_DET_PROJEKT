Projekt Modelowanie Deterministyczne

Projektując mieszkanie należy nie skupiać się tylko na rozkładzie pomieszczeń, ale także na odpowiedniej cyrkulacji powietrza.

Projekt uwzględnia oczywiście nie tylko poszczególne pomieszczenia, ale również okna, drzwi oraz grzejniki. 
Mieszkanie składa się z 3 głównych pomieszczeń sypialni, łazienki oraz pokoju dziennego, a także małego korytarza. 
W każdym pokoju znajduje się grzejnik i okna (z wyjątkiem pokoju dziennego, gdzie zostały umieszczone dwa okna). 

Celem projektu jest zminimalizowanie kosztów związanych z ogrzewaniem mieszkania. Jest to problem większości Polaków w okresie grzewczym.
Nieodpowiednio dobrana moc grzejników czy zły przepływ powietrza może znacząco wpłynąć na wysokość otrzymanego rachunku.

W właśnie tym celu zostało zaimplementowane w języku Python mieszkanie wraz z odpowiednimi do każdego pomieszczenia temperaturami. 
Został napisany opowiedni schemat numeryczny, który odpowiada za proces dyfuzji ciepła a tym samym za zmiany temperatury w mieszkaniu. 
Przewadzono eksperyment jak zmienia się rozkład temperatur w poszczególnych pomieszczeniach wraz z upływającym czasem. 
Aby dokładnie przyjrzeć się problemowi zużytej energii potrzebnej na ogrzewanie domu, wykonano symulacje dla różnych ustawień mocy grzejników.

W ten sposób można uzyskać odpowiedź, jak uniknąć kosmicznych rachunków i nie zamarznąć?

Projekt zawiera:
- RYSUNEKDOMU.py kod implementujący klasę HeatingModel oraz mieszkanie jako macierz 100x100, który rysuje projekt
- PROJEKTMOD.py kod odpowiadający za symulację i wykorzystujący schematy numeryczne
- Projekt_domu.png rysunek projektu mieszkania
- Temperatura_domu.png wykres rozkładu temperatury początkowej
- pomiarenergi.png wykres porownujacy końcowe wyniki symulacji
- heatingmodel.pdf szczegółowy opis projektu 
