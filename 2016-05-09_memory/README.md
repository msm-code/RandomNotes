# WHAT EVERY PROGRAMMER SHOULD KNOW ABOUT MEMORY

## 1. Introduction

## 2. Commodity Hardware Today

**CPU architecture**
 - Obecnie wygląda to tak, że wszystkie CPU łączą się z northbridge przez FSB (Front Side Bus)
 - Northbridge zawiera, między innymi, memory controller. Różne typy RAM (DRAM, Rambus, SDRAM) wymagają róznych memory controllerów.
 - Northbridge komunikuje się z southbridge. Southbrudge komunikuje się z wszystkimi innymi urządzeniami.
 - Kiedyś każdy dostęp do RAMu musiał iść przez CPU, ale teraz wszystkie urządzenia wspierają DMA (direct memory access)
 - Wyraźny bottleneck to bus z northbridge do RAMu - kiedyś był tylko jeden, od DDR2 są dwa (co podwaja bandwidth). Przez to trzeba schedulować dostępy do pamięci.
 - Z poprzedniego wynika też, że kiedy wiele hyperthreadów, wątków albo procesorów próbuje sie dostać do pamięci jednocześnie, to czas czekanai jest jeszcze dłuższy
 
**NUMA**
 - Northbridge może być podłączone do kilku zewnętrznych memory controllerów - pozwala to zwiększyć bandwidth i ilość dostępnej pamięci
 - Ale to nie jedyne podejście - można też zintegrować MC z procesorami, i podłączyć RAM do każdego CPU
 - Zaleta to olbrzymi bandwidth
 - Wada to np. niejednorodny dostęp do pamięci (tytułowe Non Uniform Memory Architecture) - kiedy procesor chce coś czytac z nieswojego RAMu, są problemy

**RAM Types**
 - mamy SRAM (static RAM) i DRAM (dynamic RAM).
 - static jest dużo szybsze, i dostarcza tej samej funkcjonalności - ale jest dużo bardziej skomplikowany (i drogi)
 - SRAM składa się z 6 tranzystorów, połączonych w skomplikowany sposób. Mają dwa stany stabilne (1 i 0). Stan jest stabilny kiedy napięcie jest dostarczane.
 - DRAM składa się z jednego tranzystora i kondensatora. Niestety, wymaga refresh cycli, oraz czas dostępu jest dużo gorszy. Refresh cycle jest co około 64ms.
 - Dodatkowy problem jest taki, że dostęp do DRAMu nie jest natychmiastowy (w przeciwieństwie do SRAM)
 - Tak czy inaczej, różnica w koszcie wygrywa i prawie wszędzie DRAM jest używany do głównej pamięci

**DRAM Access**
 - Zapytania odczytu i zapisu są multiplexowane i demultiplexowane (trudno by było mieć 2^32 address lines)
 - Konkretnie, adres jest przekazywany jako liczba binarna, i N wejść starcza do adresowania 2^N komórek)
 - Przy jeszcze większej ilości linii, multiplexing działa na dwóch etapach - row address selection oraz column address selection
 - Z powodu DRAM rechargingu, jeśli procesor chce się dostać do wiersza który jest obecnie refreshowany, może mu to zająć całkiem sporo czasu.
 
**Synchronous DRAM**
 - każdy transfer danych dzisiaj składa się z 8 bajtów.
 - przekazanie adresu kolumny i wiersza, z powodu protokołu, zajmuje 4 cykle. Później co cykl można odczytać jeden pakiet danych (8 bajtów)
 - trzymanie otwartego wiersza to coś co kontroler musi zadecydować spekulatywnie.
 - moduły DDR są często opisywaner za pomocą notacji w-x-y-z-T, np. 2-3-2-8-T1.
   - w to CAS latency
   - x to RAS-to-CAS latency
   - y to RAS precharge
   - z to Active to Precharge delay
   - T to command ratge
 - sporo z tych parametrów można zmienić z poziomu BIOSu. SDRAM ma programowalne rejestry, gdzie można zmienić te wartości.

**Memory Types**
 - Przy SDR SDRAM (single data rate) wielkości komórek i prędkość transferu były identyczne
 - Przy DDR SDRAM (double data rate) dane są transportowane przy rising i falling edge. Jest to możliwe dzięki buforowi.
 - Przy DDR2 SDRAM, jest kolejna innowacja - frequency na busie jest zwiększone 2x.
 - Przy DDR3 SDRAM, frequency na busie jest zwiększone 4x
 
**Fully Buffered DRAM**
 - Rozwiązanie Intela na problem tego, że przy dużych maszynach nie wiadomo gdzie podłączyć więcej ramu (poza NUMA)
 - Różni się od DDR2 tym, że zamiast równoległego databusa FBDRAM używa serial busa (który może być na znacznie wyższej częstotliwości)
 - Ma tylko 69 pinów, zamiast 240 pinów dla DDR2.

## 3. CPU Caches

**Cache CPU**
 - Dawno temu, dostęp do RAMu był prawie równie szybki jak dostęp do rejestru
 - Ale to się bardzo zmieniło, bo okazało się w pewnym momencie że dostępu do RAMu już nie można przyśpieszyć (jak wspomniano w powyższych punktach)
 - Rozwiązanie: mała ilość SRAMu + duża ilość DRAMu
 - Procesor "komunikuje" się bezpośrednio z cache, a dostęp do main memory (przez bus) jest wykonywany tylko jeśli nastąpi cache miss
 - Intel (i pewnie inni) stosuje oddzielne cache dla kodu i dla danych
 - Później doszło second level cache (które jest większe niż first level cache, ale mniejsze niż główna pamieć)
 - No i jest TLB (translation lookaside buffer) - cache przechowujące translacje z pamięci wirtualnej do fizycznej.

**Strategie Cachowania**
 - Kiedy coś trzeba jakieś dane wczytać do cache, zawsze jest to czytane do L1d.
 - Prawie zawsze to oznacza że trzeba coś wyrzucić z L1d - ląduje to w L2, z L2 coś ląduje do L3, a z L3 do głównej pamięci.
 - Taka strategia nazywa się Exclusive Cache (robi to np. AMD i VIA).
 - Intel implementuje Inclusive Caches - gdzie każda linia cache z L1d jest jednocześnie w L2. Dzięki temu evicting z L1d jest dużo szybsze.
 - CPU mogą dowolnie implementować caching, tak długo jak nie naruszają abstrakcji dostarczanej przez architekturę procesora.
 - Wszystkie procesory w Symmetric Multi-Processor (SMP) muszą widzieć jednocześnie te same dane (cache coherency).
 - Jest to rozwiązane ta, że kiedy jakiś inny procesor pisze jakieś dane to jest to wykrywane, i ta linia w cache jest oznaczana jako invalid.
 - Przykładowe czasy dostępu do cache (w cyklach): 1 do rejestru, 3 do L1d, 14 do L2, 240 do głównej pamięci.
 
**CPU Cache Implementation Details**
 - Fully Associative Cache - każda linia cache może potencjalnie trzymać każdą linię z głównej pamięci. Niestety, niepraktyczne prawie zawsze.
 - Direct-Mapped Cache - ekstremalna odwrotność poprzedniego - każda linia z głównej pamięci może trafić tylko w jedno miejsce.
 - Wadą poprzedniego jest to, że działa dobrze tylko jeśli używana pamięc jest mniej więcej równo rozłożona. Jesli nie, to będzie duzo konfliktów.
 - Set-Associative Cache - Połączenie FAC i DMC. Dzieli się cache na zbiory, a w zbiorach używamy DMC.
 - w SAC obecne procesory używają około 24 poziomów dla L2, i około 8 poziomów dla L1.

**Performance Details**
 - Ciekawy detal implementacyjny procesora - kiedy procesor wykrywa sekwencyjny dostęp do pamięci, potrafi prefetchować kolejną linię (prefetching).
 - Dzięki prefetchingowi dostęp do cache L2 i głównej pamięci potrafi być dużo szybszy, niż gdyby go nie było - np. zamiast 200 cykli wyjdzie 9.
 - Ograniczenie prefetchingu jest takie, że nie może przekraczać granic stron.
 - A nie może przekraczać granic stron, bo w przeciwnym wypadku program doświadczałby pagefaulta (potencjalnie) którego sam nie wywołał.
 - Dodatkowo problemem są TLB cache misses. Kiedy dużo stron jest dotykanych, TLB szybko się kończy i trzeba obliczać adresy stron co jest wolne.

**Write Behavior**
 - Kiedy zapisuje się coś do pamięci, trzeba coś zrobić z faktem ze cache mają być coherent.
 - Write-Though - kiedy cokolwiek jest pisane do cache, to od razu idzie to przez FSB do głównej pamięci.
 - Problem z write through jest taki, ze np. pisanie w kółko do lokalnej zmiennej spowoduje masę ruchu na FSB.
 - Write-Back - linie w cache są tylko markowane jako dirty. Kiedy linia z cache będzie dropowana kiedyś, dirty bit mówi że trzeba ją zapisać do RAMu.
 - Problem z write back jest taki, ze jeśli drugi procesor chce przeczytac coś z cache, a jakiś procesor ma tą linię jako dirty, to jest kłopot.
 - Są jeszcze dwie strategie zapisywania - Write Combining i Uncacheable. Ale są one używane dla fragmentów przestrzeni adresowej które nie odpowiadają RAMowi.
 - Write Combining - działa tak, że czeka z zapisaniem linii, bo liczy że będzie kilka writów pod rząd w podobne miejsce.
 - Uncacheable - jak nazwa wskazuje, obszar pamięci który nie jest cachowany wcale (może np. odpowiadać on fizycznym urządzeniom).

**Multi-Processor Support**
 - Problem kiedy wiele procesorów próbuje czytać i zapisywać te same dane.
 - Dawanie procesorom dostępu bezpośrednio do innych cache jest kompletnie niepraktyczne.
 - Rozwiązanie to czytanie z cache innego procesora, jeśli linia jest dirty. Tylko skąd procesor może wiedzieć że jakaś linia jest dirty?
 - Standard MESI (Modified, Exclusive, Shared, Invalid).
   - Stan Modified mówi, że linia jest zmieniona w lokalnym cache (oraz że to jest jedyna kopia w jakimkolwiek cache)
   - Stan Exclusive mówi, że linia jest wyłączna (nie ma jej w żadnym innym cache)
   - Stan Shared mówi, że linia nie jest modyfikowana, ale może być w cache innego procesora
   - Stan Invalid mówi, że linia jest nieużywana. 
 - Operacja RFO (Request For Ownership) - kiedy procesor chce zapisać do jakiejś linii cache która jest shared.
 - RFO będzie wołane w dwóch przypadkch zazwyczaj - wątek zmigrował między procesorami, oraz linia cache jest naprawdę potrzenba w dwóch procesorach.
 
**Instruction Cache**
 - Nie tylko dane są cachowane, również instrukcje wykonywane przez procesor są cachowane.
 - Dużo mniej problematyczne niż data cache, bo dane są znacznie lokalniejsze, oraz kod jest generowane przez kompilator a nie człowieka.
 - Instrukcje często są cachowane już po zdekodowaniu, nazywa się to Trace Cache.
 - Z powodu tego cachowania, Self Modifying Code jest bardzo niemiłe dla cache.
 
**Critical Word Load**
 - Ficzer pozwalający na to, że procesor mówi które słowo go najbardziej interesuje podczas czytania z RAMu.
 - Dzięki temu, mimo że będzie czytana cała linia z RAMu do cache, to to najważniejsze słowo dostanie od razu.
 - Przy prefetchingu nie wiadomo oczywiście które słowo sie przyda. 
 
## 4. Virtual Memory

**Virtual Memory**
 - Subsystem pamięci wirtualnej w procesorze implementuje wirtualna przestrzeń adresową dostarczaną dla każdego procesu osobno.
 - Dzięki temu każdy proces może udawać że jest sam w systemie.
 - Virtual Address Space jest implementowane w MMU (Memory Management Unit) na CPU.
 
**Simplest Address Translation**
 - Adres wirtualny dzielimy na dwie części - directory i offset.
 - Directory to liczba wskazująca na offset w page directory, a directory entry wskazuje na słownik stron.
 - Przykładowo, przy 4MB stronach jest używany taki layout na x86 - offset ma 22 bity, a address ma 10
 - Problem z tym, że marnowałoby to dużo pamięci (duże strony)
 
**Multi-Level Page Tables**
 - Jako że 4MB strony są duże, przydatny jest kolejny poziom
 - Dzięki temu można mieć best of both worlds - page table nie marnują za dużo pamięci, a jednocześnie strony są małe
 - W praktyce obecnie największy poziom page tabli to 4 stopień zagnieżdżenia (4 słowniki i offset)
 - Level 4 directory jest adresowane przez specjalny rejestr w CPU, a indeksy w tym są adresowane przez części adresu wirtualnego.
 
**Optimizing Page Table Access**
 - Jeden resolving adresu wirtualnego to aż cztery odwołania do pamięci (patrz: punkt poprzedni). To dużo za wolno.
 - Można traktować słowniki page tabli jak normalne dane i trzymać je w L1d, ale to ciągle będize za wolne.
 - Dlatego wprowadzono TLB (Translation Lookaside Buffer). Jest to dość małe cache, bo musi być ekstremalnie szybkie.
 - Współczesne CPU mają kilka poziomów TLB cache (tak jak z danymi). Mała wielkość L1TLB często jest nadrabiana tym, że jest fully associative.
 - TLB nie może być prefetchowane, bo mogłoby spowodować pagefaulty których proces nie spowodował (a na to nie można pozwolić).
 - Tak samo TLB jest dzielony na ITLB i DTLB (instruction i data TLB), i tak samo jest wyższy poziom jak L2TLB.
 
**Caveats of using TLB**
 - Problem z TLB jest taki, że to processor-wide resource. Więc jak zmienia się pagetable, trzeba coś z cache zrobić
 - Rozwiązanie pierwsze - całe cache jest flushowane kiedy context switch jest robiony.
 - To dobre rozwiązanie, ale drogie - czasami np. przy syscallu kod kernela może tylko kilka tysięcy opcodów wykonać.
 - Rozwiązanie drugie - invalidowanie wpisów w TLB indywidualnie. W tym celu taguje się indywidualnie różne address spaces.
 
**Impact of Virtualization**
 - Wirtualizacja jest coraz bardziej popularna.
 - (dużo czytania/pisania).
 - TL;DR - z wirtualizacją, koszt dostępów do pamięci jest jeszcze bardziej kosztowny.
 
## 5. NUMA Support

**NUMA Hardware**
 - Northbridge jest dużym bottleneckiem, bo cały ruch pamięci przez niego przechodzi.
 - Alternatywa to model którego używa AMD (HyperTransport) - procesory są łaczone w hipersześcian (tzn. odcinek/kwadrat/sześcian/etc).
 - Następny krok, to łączenie grup procesorów i implementacja współdzielonej pamięci dla nich - to dość specjalizowane hardware już.
 - Niektóre procesory są projektowane bezpośrednio pod NUMA

**OS Support for NUMA**
 - Żeby wspierać NUMA, procesor musi brać rozproszony charamter pamięci pod uwagę.
 - Przykładowo, jeśli procesor wykonuje się na procesorze X, powinien dosta pamięć podłączoną bezpośrednio do tego procesora.
 - OS powinien też unikać migrowania procesora z jednego cora na drugi.
 - Pliki/foldery z informacjami o procesorze: `/sys/devices/system/cpu/cpu*/cache/`, `/sys/devices/system/cpu/cpu*/topology/`.
 - Bardziej specyficzne dla NUMA są dane w `/sys/devices/system/node/node*` - każdy folder to jeden node w NUMA. 

**Remote Access Costs**
 - W przykładzie, 1 hop spowalnia wszystko o około 17%, a 2 hop spowalnia wszystko o około 30%
 - W /proc/pid/numa_maps są informacje o rozkładzie pamięci procesu miedzy nodami
 
## 6. What Programmers Can Do