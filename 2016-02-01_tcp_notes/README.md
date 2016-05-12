SIECI I TAKIE TAM

CIDR - Classless Inter-Domain Routing:
Metoda alokacji adresów IP i routowania pakietów IP.
IETF ogłosił to w 1993 żeby zastąpić poprzednią architekturę "klas" (classful) (adresy klasy A, B, C, D, E).
Celem było spowolnienie wzrostu routing tables na routerach w internecie i żeby spowolnić szybkie wyczerpywanie sę adresów IP.
Adresy IP składają się z dwóch części - bardziej znacząca część to nerwork address, a reszta to host identifier.
W IPv6, rozmiar podsieci ma zawsze 64 bity.
CIDR notation to sposób zapisywania adresu IP razem z ich routing prefixem - dopisuje sie po slashu ilość bitów routing prefixu, np. 192.168.2.0/24

ROUTING ALGORITHMS
Routery muszą wiedzieć coś o innych routerach żeby ocenić jaka droga będzie najlepsza.
Istnieją dwa rodzaje algorytmów
    - DV (distance vector) algorithms, czyli decentralized algorithms
        - każdy router zna swoją odległość do wszystkich innych, i wie przez kogo kierować
        - algorytmy - np. bellman ford, albo ford fulkerson
    - LS (link state) algorithms, czyli centralized algorithms
        - każdy router identyfikuje z czym jest fizycznie połączony i pobiera od nich ich adres IP
        - zmierz delay time między sąsiednimi routerami
        - każdy router dzieli sie wiedzą z sąsiadami, którzy to zapisują - ostatecznie każdy router wie wszystko
        - algorytmy - przykładowo dijkstrta
    - hierarchical routing

Większość routingu TCP/IP jest bazowana na dwupoziomowym routingu, gdzie adres IP jest dzielony na część hosta i część sieci.
Bramy używają jedynie części sieci, do momentu kiedy datagram dojdzie do bramy która może dostarczyć go bezpośrednio. Większe poziomy hierarchii są wprowadzane przez dodanie podsieci.

TCP/IP Transport Layer Protocols

TCP "NOTES" - ciekawe funkcje TCP
 - three way handshake - to wiadomo
 - sliding window mechanism - wysyłanie nie jednego pakietu na raz ale całej serii
 - PUSH - wymuszenie wysłania danych od razu, bez buforowania
 - URGENT - wymuszenie wysłania pakietu, niekoniecznie nawet w dobrej kolejności (priorytetowe dane)
 - retransmission timer - po wysłaniu każdego segmentu włączamy timer, i czekamy. Jeśli nie dostaniemy acka odpowiedniego, to przesyłamy jeszcze raz.
 - non contiguous acknowledgment handling and selective acknowledgment (SACK)
    - problem że nie można powiedzieć "nie doszedł pierwszy pakiet, ale doszło następne 19" - w wyniku będzie retransmisja wszystkicj 20
    - można retransmitować tylko timeoutnięte segmenty - niewydajne przy pesymistycznych przypackach - albo wszystkie segmenty - niewydajne przy optymistyczncyh przypadkach.
    - SACK - rozszerzenie do TCP w RFC 1072. Oba urządzenia muszą wspierać TCP i muszą to wynegocjować ustawiając SACK-Permitted w segencie SYN. Pozwala wysłać flagę bitową z ackniętymi pakietami.
 - problemy z wybieraniem długości retransmission timera
    - bardzo ważne jest latency/odległość między serwerami
    - różne losowe fluktacje i wariancje
    - adaptive retransmission bazujące na round trip time calculations - TCP liczy na podstawie round trip time ile może zająć kolejny RTT.
    - problem przy retransmitach, bo nie wiemy czy liczymy RTT retransmitniętego pakietu czy oryginału
    - Karn's algorithm - nie liczymy retransmitniętych pakietów do liczenia RTT. Ale jeśli pakiet nie dojdzie, to mnożymy tymczasowy retransmission timer przez jakiś mnożnik, aż dojdzie pakiet i uda sie zmierzyć bez retransmisji.
 - TCP window size Adjustment and Flow Control
    - potrzebne, bo urządzenie może nie radzić sobie z przetwarzaniem danych tak szybko jak je dostaje.
    - można też zmniejszyć rozmiar bufora w razie potrzeby
 - silly willy syndrome (SWS) - rozmiar bufora się ciągle zmniejsza, i coraz mniejsze pakiety są wysyłane - za małe, nie ma minimal segment size 
   - Silly Window Syndrome Avoidance Algorithms - wymaganie minimalnej wielkości okna przed rozgłoszeniem
   - Receiver SWS Avoidance - odbiorca przyczynia się do SWS przez redukowanie okna swojego receive window do ciągle mniejszych wartości. Prosta zasada rozwiązująca problem - nie rozsyłamy że mamy inną wielkośc okna, jeśli to zostawia nam za mało używalnego okna.
   - Sender SWS Avoidance and Nagle's algorithm - bardzo podobnie, tylko że ze strony sendera. Nie wysyłamy danych od razu, a wtedy kiedy mamy co wysyłać.
     - kiedy nie ma unacknowledged data, wysyłamy dane od razu kiedy sie da
     - kiedy jest unacknowledged data, cała pozostałe dane muszą być trzymane w transmit buffer i nie wysłane zanim unacknowledged data będzie acknowledged, albo zbierzemy wystarczająco dużo danych żeby wysłać cały segment (MSS). Dotyczy to też PUSH requestów
 - TCP congestion handling and congestion avoidance algorithms
   - połączenia TCP stają się mniej 'selfish' - próbują brać pod uwagę istnienie innych użytkowników sieci etc. 
   - Wiemy że jest congestion kiedy urządzenia=routery pośrodku zaczynają sie przeciążać.
   - Slow Start - naiwnie kiedy dwa urządzenia nawiążą TCP to mogą do siebie wysyłać ile wlecie pakietów. Ale Slow Start mówi że powinny poczekać i wysyłać najpierw mniej żeby nie przeciążyć sieci.
   - Congestion Avoidance - kiedy pakiety są dropowane, znowu urządzenia zmniejszają ilość wysyłanych pakietów
   - Fast Retransit - kiedy segmenty są otrzymywane nie w kolejności, odbiorca będzie je i tak ackował w kolejnosci. Ale retransmit timer jest długi, i czasami nadawca może dojść do wniosku że pakiet przepadł nawet jeśli jeszcze nie przedawnił się timer.
   - Fast Recovery - w poprzednim przypadku, nie jest używany Slow Start (bo założenie jest takie, że skoro doszły inne segmenty to coś tam idzie).

TCP/IP Internet Layer (OSI Network Layer) Protocols
 - Internet Protocol (IP/IPv4, IPng/IPv6) and IP-Related Protocols (IP NAT, IPSec, Mobile IP)
   - Concepts and Overview
     - IP Overview and Characteristics
       - IP zajmuje sie dostarczaniem danych nie pomiędzy urządzeniami na tej samej fizycznej sieci, ale urządzeniami które mogą być w różnych sieciach, połączonych w dowolny sposób.
       - czyli zadanie - dostarczenie datagramów z jednego miejsca w drugie
       - urządzenia adresują sie uniwersalnie po adresie IP
       - Underlying protocol independent - IP działa na dowolnej sieci która jest designowana żeby pracować z TCP/IP (huh).
       - Connectionless
       - IP daje możliwość fragmentacji pakietu (bo każde urządzenie może miec inne Maximum Frame Size) a później reassembly
       - Routing / Indirect Delivery
     - Protokoły podobne do IP
       - IP NAT / NAT - Network Adress Translation. pozwala prywatnym sieciom być interfacowanye do publicznych sieci w flexible sposób. Pozwala to na sharowanie publicznych adresów IP.
       - IPSec - zbiór subprotokołów które pozwalają na bezpieczny transfer danych za pomocą IP - coraz popularniejsze dla np. VPNów
       - Mobile IP - upraszcza IP w sytuacjack kiedy kompiter często przechodzi z sieci do innej.
       - 



# 1. Network Funtamentals

## 1.1 OSI Model

OSI model oryginalnie nie miał być stworzony w celach edukacyjnych - a jako podstawa do zaakceptowanego szeroko zbioru protokołów które byłyby używane
między sieciami - czyli dokłądnie tego czym stał się internet.

W praktyce OSI przegrało z modelem TCP/IP (który był prostszy), i teraz jego zastosowanie jest głównie edukacyjne.


# 2. Network Interface Layer

## 2.1 Address Resolution Protocol (ARP)

**Potrzeba ARP**
 - Adresy IP są zbyt wysokopoziomowe dla fizycznych urządzeń
 - Address resolution musi być szybkie, bo zdarza się na każdym kroku w sieci.
 - Address resolution można przeprowadzić na dwa sposoby - albo direct mapping (bierze wysokopoziomowy adres i transformuje na nisko) albo 
     dynamic resolution (specjalny protokół który pozwala urzędzeniu z samym IP dostać adres data link).

**Działanie ARP**
 - Polega na tym, że urządzenie chcące dostać MAC z IP rozsyła pakiet w rodzaju "niech sie zgłosi ten kto ma taki adres IP", i dostaje
     odpowiedź typu "urządzenie z tym adresem IP ma adres MAC równy ..."
 - Jest mocno cachowane - jak urządzenia tylko widzą wymieniane informacje o MAC, updatują swoje cache table.

http://www.tcpipguide.com/free/t_TCPIPAddressResolutionProtocolARP.htm

## 2.2 Reverse Address Resolution Protocol (RARP)

# 3. Internet Layer 

## 3.1 Internet Protocol v4

**IP Overview and Characteristics**
 - IP zajmuje sie dostarczaniem danych nie pomiędzy urządzeniami na tej samej fizycznej sieci, ale urządzeniami które mogą być w różnych sieciach, połączonych w dowolny sposób.
 - czyli zadanie - dostarczenie datagramów z jednego miejsca w drugie
 - urządzenia adresują sie uniwersalnie po adresie IP
 - Underlying protocol independent - IP działa na dowolnej sieci która jest designowana żeby pracować z TCP/IP (huh).
 - Connectionless
 - IP daje możliwość fragmentacji pakietu (bo każde urządzenie może miec inne Maximum Frame Size) a później reassembly
 - Routing / Indirect Delivery

**Protokoły podobne do IP**
 - IP NAT / NAT - Network Adress Translation. pozwala prywatnym sieciom być interfacowanye do publicznych sieci w flexible sposób. Pozwala to na sharowanie publicznych adresów IP.
 - IPSec - zbiór subprotokołów które pozwalają na bezpieczny transfer danych za pomocą IP - coraz popularniejsze dla np. VPNów
 - Mobile IP - upraszcza IP w sytuacjach kiedy kompiter często przechodzi z sieci do innej.

**Adresowanie IP**
 - Adres IP to w pewnym sensie ID komputera w sieci
 - Jeśli komputery nie są w tej samej sieci datagram musi być routowany pośrednio.
 - Notacja adresów IP: 12.34.56.78
 - IP dzielimy na Network Identifier (identifykator sieci) oraz Host Identifier (identyfikator hosta w sieci)
 - Jeśli użyje sie IP z samymi jedynkami w host id, to jest to traktowane jako broadcast do wszystkich urządzeń w sieci.
 - Jeśli użyje się IP z samymi zerami w host id, to jest to traktowane jako pakiet odnoszący się do całej sieci
 - Jeśli użyje sie IP z samymi zerami w network ID, jest to traktowane jako "obecna sieć" albo "domyślna sieć"
 - IP z samymi zerami (0.0.0.0) to konsekwentnie "to urządzenie"/"obecne urządzenie"
 - IP z samymi jedynkami (255.255.255.255) to broadcast to wszystkich hostów osiągalnych w bezpośrednio połączonej sieci
 - Jeśli urządzenie zmienia sieć, musi też zmienić swoje IP (problem przy urządzeniach często zmieniających siec - rozwiązanie to mobile IP)
 - Specjalny zakres adresów IP to 127.0.0.0/8. Normalnie kiedy aplikacja chce wysłać informacje, informacja idzie na sam dół stosu TCP/IP i transmitowana dalej.
     Ale ten zakres jest specjalny (tzw. loopback) - datagramy wysłane przez hosta do niego nie są wysyłane do link layera, ale wracają bezpośrednio do źródłowego
     urządzenia na poziomie IP. Zazwyczaj do tego jest uzywany 127.0.0.1.
 - Zakres 169.254.0.0/16 jest zarezerwowany dla automatic private address allocation (związane z DHCP, todo)
 - Prywatne zakresy IP: 223.255.255.0/24 (reserverd), 192.168.0.0/24, 191.255.0.0/16, 10.0.0.0/8.

**Multiple IP addresses and multihoming**
 - Urządzenie może być podłączone do wielu sieci, siłą rzeczy ma w nich różne ID
 - Urządzenie może być połączone przez wiele interfejsów do sieci, każdy z nich ma inne ID
 - Urządzenie podłączone przez wiele interfejsów do sieci może służyć jako router (software router)

**IP Address Management and Assignment Methods and Authorities**
 - Za zarządzenie adresami IP odpowiadała tylko IANA (Internet Assigned Number Authority)
 - Obecnie powstała (późne lata 90') ICANN (Internet Corporation for Assigned Names and Numbers) które odpowiada za przydzielanie adresów IP oraz za DNS
 - Oryginalnie adresy IP były przydzielane w klasach, teraz tylko CIDR (Classles Inter Domain Routing)

**Classful Addressing**
 - Nieużywany obecnie
 - Pierwszy bit 0? Adres A. Drugi bit 0? Adres B. Trzeci bit 0? Adres C. Czwarty bit 0? Adres D.

**Multicast Addressing**
 - Jeden pakiet może iść do wielu urządzeń dzięki temu
 - Adresy multicast są rozpoznawane po wzorze "1101" w pierwszych czterech bitach (pierwszy oktet 224-239), czyli 224.0.0.0/4
 - Adresy multicast są zawsze docelowe, nigdy źródłem (ofc)
 - Adresy multicast mają 3 typy: 224.0.0.0/8 - "well known" multicast address, 239.0.0.0/8 - lokalne adresy multicast, cała reszta - globalne adresy
 - Well known adresy multicast to lista specjalnych adresów, między innymi:
    - 224.0.0.0 - reserved
    - 224.0.0.1 - wszystkie urządzenia podsieci
    - 224.0.0.2 - wszystkie routery podsieci
    - 224.0.0.3 - reserverd
    - 224.0.0.4 - wszyskie routery używające DVMRP
    - 224.0.0.5 - wszyskie routery używające OSPF
    - 224.0.0.6 - wybrane routery używające DVMRP
    - 224.0.0.9 - wybrane routery używające RPI-2
    - 224.0.0.11 - mobilne urządzenia (dla mobile IP)
    - 224.0.0.12 - DHCP server/relay agent
 - IGMP (Internet Group Management Protocol) to protokół używany do tworzenia i zarządzania grupami urządzeń.

**Subnet Addressing**
 - Możliwość tworzenia podsieci w sieci, ale na zewnątrz dalej wygląda to na jedną fizyczną sieć
 - Wielkość podsieci może sie różnić między organizacjami, więc dochodzi kolejny parametr - subnet mask
 - Implementacja tego wymaga zmian w routerach
 - Podobno można podzielić subnety nie po pierwszych bitach (maska podsieci nieciągła). Brzmi to bardzo dziwnie i pewnie jeszcze dziwniej działa, ale teoretycznie jest możliwe.4
 - VLSM (Variable Length Subnet Masking) - można podzielić podsieci na podsieci etc. Ofc też tylko historyczne bo CIDR.

**CIDR**
 - Stworzony już podczas implementacji IPv6
 - W zasadzie to zastosoawnie konceptów VLSM do całej sieci. W pewnym sensie internet staje sie jedną wielką siecią podzieloną na podsieci jak w VLSM.
 - Potrzebna jest "maska podsieci", ale tutaj wyrażana za pomocą CIDR notation (czyli slash notation) - już bity muszą być ciągłe.
 - Specjalne sieci mają takie same znaczenie jak w zwykłym routingu.

**IP Datagram Encapsulation**
 - Możliwe że wysyłana wiadomośc jest za duża dla pakietu IP i będzie fragmentowana - wtedy odbierające urządzenie musi złożyć ponownie wiadomośc z datagramów
 - Mimo że IP jest dość prostym, bezpołączeniowym protokołem, header Ip przeosi całkiem sporo inforamcji. Ma minimalnie 20 bajtów, a może być dłuższy.
    - Wersja (4 bity) - dla IPv4 zawsze równe 4
    - IHL (Internet Header Length) (4 bity) - długość nagłówka IP w 32bitowych słowach. uwzględnia opcję i padding.
    - TOS (Type Of Service) (1 bajt) - oryginalnie miał mówić o specjalnych ficzerach (typu priorytetowy datagram), ale nigdy tak nie był za dużo używany
        obecnie zredefiniowany i używana jest technika zwana Differentiated Services (DS)
    - TL (Total Length) (2 bajty) - łączna długość datagramu w bajtach
    - Identification (2 bajty) - 16bitowa wartość wspólna dla każdego fragmentu z wiadomości należących do wiadomosci, służy do reasemblacji.\
    - Flags (3 bity) - 1 bity nieużywany, 2 bit to DF (don't fragment, nie fragmentować dalej datagramu) 3 bit to MF (more fragments, jest więcej fragmentów w wiadomości)
    - Fragment Offset (15 bitów) - offset wiadomości gdzie zaczyna się ten fragment (w wielokrotnościach 8 bajtów)
    - TTL (Time To Live) (1 bajt) - jak długo datagram powinien żyć w sieci. Każdy router zmniejsza o 1, jeśli jest równe 0 to router dropuje.
    - Protocol (1 bajt) - jaki wysokopoziomowy protokół jest używany przez datagramy. Troche dziwne ale no. Definiuje np. TCP, ICMP, IGMP, GGP, UDP, etc.
    - Header Checksum (2 bajty) - podzielenie nagłówka na bajty i dodanie ich do siebie.
    - Source Address (4 bajty) - adres z którego idzie pakiet IP
    - Destination Address (4 bajty) - adres docelowego odbiorcy pakietu
 - Datagramy IP mogą mieć dodatkowe opcje. Każda opcja ma swój własny format i jest doklejana po nagłówku IP
    - Copied flag (1 bit) - flaga mówiąca czy opcję należy kopiować do wszystkich fragmentów przy fragmentacji
    - Option class (2 bity) - flaga mówiąca do jakiej kategorii wpada opcja (0 to kontrolna, 2 to debugging)
    - Option number (5 bitów) - ID opcji
    - Option Length (1 bajt) - dla opcji o różnej długości, długość całej opcji łącznie z trzema subfieldami
    - Option Data (różnie) - dane opcji
 - Przykładowe opcje IP to np
    - End of options - opcja zawierająca tylko jeden zerowy bajt, mówi że to koniec listy opcji
    - No Operation - opcja używana jako padding do wyrównania opcji
    - Security - opcja dla armii, mówiąca o klasyfikacji bezpieczeństwa pakietów (WTF).
    - Loose Source Route - pakiet musi iść dokładnie ścieżką opisaną w tej opcji
    - Record Route - każdy router powinien dodać się do tego datagramu jeśli jest ta opcja, a później można na traceroute patrzeć
    - Strict Source Route - pakiet musi iśc ścieżką opisaną w tej opcji, ale mogą być routery pośrednio.
    - Timestamp - każdy router powinien dodać timestem do tego datagramu
    - Traceroute - do lepszej implementacji traceroute

**IP Datagram Size**
 - Żeby można było przesłać datagram z jednego urządzenia do drugiego, musi być nie większy niż wspierany przez urządzenia po drodze
 - Dlatego IP pozwala na fragmentację datagramów
 - Problemem jest dopasowanie wielkośći datagramu do przepustowości data link layer
 - MTU (Maximum Transmission Unit) to limit jak duży pakiet jest w stanie przesłać urządzenie dalej.
 - Minimalne wymagane MTU to 576 bajtów (żaden router nie może wspierać mniej niż tyle)
 - Urządzenia pośrednie mogą fragmentować, ale nigdy nie reasemblują pakietów
 - MTU path discovery (odkrywanie MTU) - można ustalić MT używając flagi DF (Dont Fragment) i robiąc bsearch.
 - Pofragmentowany pakiet IP trzeba złożyć z powrotem, w dobrej kolejnosci

**IP Datagram Delivery and Routing**
 - Można podzielić wszystkie delivery na dwa rodzaje - direct (bezpośrednio w jednej fizycznej sieci) lub indirect (w innej sieci przez jeden lub więcej routerów)
 - Gateway - nazwa na urządzenie łączące dwie sieci (np. router)
 - Hopping - jako że między urządzeniami może być wiele routerów, pakiet często musi iść przez wiele sieci
 - Routing jest robiony jeden hop na raz. Kiedy wysyłamy pakiet nie wiemy jaką ściezką dojdzie do celu. Wysyłamy go tylko do naszego routera który wysyła go dalej.
 - Każdy router kiedy dostaje pakiet decyduje gdzie go wysłać i wysyła dalej (ma on albo zapisane adresy fizyczne routerów do których jest podłączony, albo używa ARP żeby je zdobyć)
 - Hosty nie przejmują się routowaniem, to robota routerów. Każdy router wie tylko gdzie kierować adresy IP z określonego zakresu.

**IP Routes and Routing Tables**
 - Routery mają wewnętrznie strukturę zwaną routing table.
 - Każdy wpis w tej tabeli (zwanej routing entry) to informacja o jednej podsieci - mówi coś w rodzaju "jeśli adres jest w tej sieci, wyślij do tego routera"
 - Wpisy w routing table ma też informacje o wydajności połączenia (jak wydajne jest połączenie), żeby móc jak najlepszą ścieżkę wybrać. Niestety to ciążka robota.

## 3.2 Internet Protocol v6

**Zmiany w stosunku do IPv4**
 - IPv6 ma wypełniać te same funkcje co IPv4
 - Duzo większy address space oczywiście (16 bajtów/128 bitów per adres)
 - Lepsze zarządzanie address space (hierarchiczna przestrzeń adresowa)
 - Eliminacja "Address Kludges" - NAT ma się stać niepotrzebny
 - Prostsza administracja TCP/IP (nie wiem co dokładnie, ale konfiguracja adresów IP ma być prostsza)
 - Lepsze wsparcie dla multicastingu, oraz dodane wsparcie do anycastingu (dostarczenie do najbliższego urządzenia)
 - Wsparcie dla Quality of Service features
 - Lepsze wsparcie dla bezpieczeństwa (IPv4 nie przejmuje sie bezpieczeństwem za bardzo - autentykacja i szyfrowanie)
 - Zmiany we fragmentacji i reassembly - zwiększa wydajność i bardziej przypomina współczesne sieci
 - Lepsze wsparcie dla mobilnych urządzeń (często zmieniających IP)
 - Neighbor Discovery Protocol (ND) - wypełnia funkcje które w IPv4 spełniał ARP i ICMP

**IPv4 to IPv6 transition methods**
 - "Dual Stack" Devices - urządzenia które zostały skonfigurowane jednocześnie z IPv4 oraz IPv6, i mogą się komunikować z dwoma typami hostów
 - IPv4/IPv6 translation - dual stack devices mogą być zaprojektowane tak żeby akceptować requesty z hostów IPv6, konwertować je do IPv4 i wysyłać dalej
 - IPv4 tunneling - enkapsulacja pakietów IPv6 w pakiety IPv4

**Adresowanie IPv6**
 - Podstawowe funkcjonalności są niezmienione - ciągle najważniejsze są identyfikacja interfejsu sieciowego i routing
 - Network Layer Addressing - adresy IPv6 są ciągle w tej samej warstwie TCP/IP (network layer), i różnią sie od adresów fizycznych
 - Ilość adresów IP na urządzenie - adresy ciągle są przypisywane do urządzenia, zazwyczaj jeden PC będzie miał tylko jeden adres unicast.
 - Interpretacja adresów - Adresy IPv6 są bardzo podobne do classless adresów IPv4.
 - Prywatne i publiczne adresy IP - istnieją oba typy, ale są zdefiniowane i używane trochę inaczej.
 - Adresy się inaczej zapisuje - w postaci np. 805B:2D9D:DC28:0000:0000:FC57:D4C8:1FFF
 - Powyższy adres można skrócić w zapisie do 805B:2D9D:DC28::FC57:D4C8:1FFF (skracanie ciągów zer do ::)

**Typy adresów IPv6**
 - Unicast address - zwykły adres, jeden na interfejs
 - Multicast address - adres multicast, powoduje wysłanie pakietu do grupy urządzeń
 - Anycast address - nowy w ipv6, powooduje wysłanie wiadomości do dowolnego członka grupy, tego najprościej dostępnego
 - Adresy anycast są technicznie zaimplementowane tak że wiele urządzeń dostaje ten sam adres IP
 - Nie ma takiego konceptu jak broadcast address w IPv6 - zastępuje go multicast addressing.

**IPv6 Global Unicast Address Format**
 - Aż 1/8 adresów IPv6 jest dedykowana dla unicast adresów (zaczynają się od bitów 001)
 - Designerzy IPv6 chcieli żeby adresy IPv6 pokazywały topologię internetu (żeby adres sam z siebie coś mówił)
 - Podzielili adres an 3 części - Global Routing Prefix (48 bitów), Subnet ID (16 bitów), Interface ID (64 bity)
 - W ten sposób większość end userów będzie dostawać adresy /48
 - Początkowo pierwsze 48 bitów było podzielone na TLA ID oraz NLA ID (top level aggretation i next level aggregation), ale porzucono to
 - Tak czy inaczej, ten format ma znaczenie tylko dla alokacji, routery się tym nie powinny przejmować

**IPv6 Interface Addresses and Physical Address Mapping**
 - Jako że jest bardzo dużo adresów IP przeznaczonych dla hosta, można część hosta wyprowadzać bezpośrednio z fizycznego adresu (MAC)
 - Mapowanie data link adresów do IP opiera się na konkretnej technologii - wszystkie adresy w sieci muszą używać tego samego sposobu mapowania oczywiście
 - IEEE zdefiniowało blok zwany 64bit extended unique identifier, skracany jako EUI-64. Jest podobny do 48bitowego MAC, poza tym że kiedy OUI ma zawsze 24 bity
     to device identifier ma 40 bitów zamiast 24. Daje to 65k razy więcej urządzeń dla każdego OUI
 - Ten format, zwany modified EUI-64 został zaadoptowany dla identyfikatorów IPv6.
 - Żeby skonwertować adres MAC do EUI-64, trzeba zrobić trzy kroki. Najpierw dzielimy adres na OUI i resztę, potem na środku dodajemy wzorzec "FFFE"
     a na koniec zmieniamy 7 bit z 0 na 1.

**Specjalne typy adresów IPv6**
 - Reserverd - adresy zarezerwowane przez IETF do specjalnych celów. Obecnie to adresy zaczynające się od bitów 00000000.
 - Private/Unroutable - blok adresów przeznaczony do zastosowań prywatnych. Zaczynają się od bitów "1111 1110 1", czyli "FE[8-F]"
 - Loopback address - jest tylko jeden adres do tej funkcji w IPv6, ::1.
 - Unspecified address - same zera, czyli ::. Wtedy kiedy np. urządzenie samo nie zna swojego adresu IP.
 - Site local addresses - adresy mające zakres całej organizacji (routery ich nie forwardują poza organizację)
 - Link local addresses - adresy mające zakres tylko konkretnej fizycznej sieci (routery ich nie forwardują)
 - IP address embedding - są IPv4 compatible IPv6 addresses - adres zaczynający się od samych zer i kończący sę adresem IPv4 - dla urządzeń dual stack
 - IP address embedding - są urządzenia IPv4 niekompatybilne z IPv6, które mają format ::FFFF:ipv4

http://www.tcpipguide.com/free/t_IPv6MulticastandAnycastAddressing.htm

**IPv6 Multicast and Anycast Addressing**
 - Adresy multicast zaczynają się od bitów 11111111 (FF). Potem są cztery zarezerwowane bity mówiące o specyficznych cechach adresu.
     obecnie 3 z nich są nieprzydzielone, a czwarty to T (transient) flag - mowi czy adres jest 'well known'.
 - Globally scoped multicast addresses muszą być unikalne na całym świecie (oczywiście), ale locally scoped addresses są unikalne tylko
     w obrębie jednej organizacji (ofc). Scope dzielimy na - 1: node local, 2: link local, 5: site local, 8: oranization local, 14: global
 - Każdy unicast address ma specjalny multicast address zwany solicited node address - ten adres jest tworzony przez specjalny mapping z
     adresu unicast. Te solicited-node addresses są używane prze IPv6 neighbor discovery protocol do wydajniejszej niż ARP rezolucji adresów.
     Wszystkie solicited node addresses maja flagę transient równą 0 i scope id=2, czyli zaczynają sie od FF02
 - Adresy anycast są noawe w IPv6 - mówią one żeby wysłać pakiet do najbliższego członka grupy, a nie do wszystkich. Co ciekawe, adresy 
     anycast to to samo co adresy unicast - po prostu IP nie musi być unikalne.

**IPv6 Autoconfiguration and Renumbering**
 - IPv6 pozwala urządzeniom chodzącym na nim skonfigurować się samodzielnie i niezależnie. W IPv4 urządzenia najpierw były konfigurowane
     manualnie a potem doszły specjalne protokoły (DHCP) które pozwalały serwerom alokować adresy IP dla dołączających urządzeń.
 - IPv6 renumbering i autoconfiguration jest opisane w RFC "IPv6 stateless address autoconfiguration" - dla kontrastu, DHCPv6 jest "stateful".
     jest stateless, bo zaczyna się bez żadnego "stanu", i nie potrzebuje DHCP servera.
 - Wykorzystuje inne ficzery IPv6 jak link-local addressing, multicasting, Neighbor Discovery protocol oraz możliwość wygenerowania interface
     id mając adres z data link layer.
 - Urządzenie ajpierw generuje swój link-local address, potem sprawdza czy jest unikalny (rozgłaszając go przez ND) i przypisuej sobie, wtedy
     kontaktuje sie z routerem który albo przekazuje mu serwer DHCP albo mówi jak ustalić swój globalny adres IP.

**TODO**
 - http://www.tcpipguide.com/free/t_IPv6DatagramEncapsulationandFormatting.htm

## 3.3 IP Network Address Translation (NAT) Protocol

**Cele i korzyści**
 - Oczywiście znacznie, znacznie przedłuża życie IPv4 - można zaadresować dużo więcej hostów niż bez NATu.
 - Trochę zwiększa bezpieczeństwo (nie da się bezpośrednio zaadresować urządzenia).
 - Prostsze jest zmienienie ISP (zmieniają się tylko adresy publicznych usług)
 - W wiekszości transparantne (zmiany których wymaga NAT są tylko w kilku routerach)
 - Prostsze jest dodawanie nowych klientów do lokalnej sieci
 - NAT mapuje wewnętrzne adresy i routuje przychodzące zewnętrzne pakiety (musi do tego modyfikować pakiety)
 - Wady też są - czasami publiczne IP jest potrzebne (brak ip może być niekompatybilny), problem z rzeczami jak IPSec (detekcja modyfikacji)
     no i wydajność

**Główne typy NAT**
 - Unidirectional NAT (outbound NAT albo traditional NAT)
 - Bidirectional NAT ("two way NAT)
 - Port-based NAT ("overloaded nat", albo jako NAPT albo PAT)
 - Overlappint NAT ("twice NAT")

**Działanie**
 - No NAT jest jak każdy widzi. Router zmienia IP dla połączeń wychodzących i transformuje z powrotem dla przychodzących.
 - Bidirectional NAT - rozszerza DNS w taki sposób, że można sie odnieść do NAT-local adresów przez DNS.
 - Port based NAT - używane w praktyce sporo, pozwala mutliplexować po portach
 - Twice NAT/Overlapping NAT - np. kiedy dwie organizacje używające tych samych prywatnych bloków IP sie łączą. Żeby rozwiązać ten problem,
     trzeba użyć NAT dwa razy i zmieniać jednocześnie source IP oraz destination IP. Tak samo jak twice nat opiera sie na użyciu DNS.
 - Podczas NATowania trzeba rekalkulować checksumy TCP/UDP, wchodzi w działanie ICMP, niektóre aplikacje przesyłają IP, no i IPSec

## 3.4 IP Security Protocols (IPSec)
http://www.tcpipguide.com/free/t_InternetProtocolIPIPv4IPngIPv6andIPRelatedProtocol.htm


## 3.5 IP Mobility Support (Mobile IP)
http://www.tcpipguide.com/free/t_InternetProtocolMobilitySupportMobileIP.htm

TODO: 
http://www.tcpipguide.com/free/t_IPDatagramSizeMaximumTransmissionUnitMTUFragmentat.htm

# 4. Transport Layer
