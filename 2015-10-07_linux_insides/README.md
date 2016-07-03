# Linux Internals Notes

[Source](https://github.com/0xAX/linux-insides/blob/master/SUMMARY.md)

# 1. Booting

## 1.1 From the bootloader to kernel

**Power Button, What Happens Next**
 - Najpierw użytkownik naciska przycisk `Power` (albo w jakikolwiek inny sposób rozpoczyna się proces bootowania)
 - Następnie płyta główna wysyła sygnał do zasilacza, który robi to co do niego należy.
 - Płyta główna dostaje `power good signal` (sygnał, który powstrzymuje komputer przed działaniem przy złym napięciu etc). Ten sygnał jest
     zdefiniowany w standardzie ATX (stworzonym przez intela w 1995, będącym ulepszeniem AT) jako +5V, zazwyczaj po 0.1s do 0.5s po rozpoczęciu.
 - Wtedy płyta główna próbuje zastartować CPU. CPU resetuje wszystkie dane które zostały w jego rejestrach i ustawia w nich domyślne wartości.
 - 80386 i późniejsze procesory definiują takie defaulty: IP=0xfff0, CS (selector)=0xf000, CS (base)=0xffff0000.
 - Procesor rozpoczyna w `Real Mode`. `Real Mode` jest wspierane przez wszystkie CPU kompatybilne z x86, od 8086 do najnowszych procesorów 64bit.
 - Procesor 8086 ma 20-bitowy bus adresowy, czyli mógł pracować z przestrzenią adresową 0-0x100000 (1mb). Ale miał tylko 16bitowe rejestry. W celu
     użycia całej dostępnej pamięci, trzeba było używać odpowiednio rejestrów segmentowych (ostateczny adres to `segment<<4 + offset`).
 - Jest z tym związany śmieszny bug (albo ficzer) - może nastąpić overflow przy dużym segmencie, jeśli jest wyłączona linia `A20`.
 - Tak czy inaczej, biorąc pod uwagę defaulty, początkowy adres to 0xfffffff0. Ten punkt nazywa się `Reset Vector`. Jest to lokacja w której procesor
     spodziewa się znaleźc pierwszą operację którą ma wykonać. Zawiera ona prawie zawsze skok, który zazwyczaj wskazuje na entrypoint BIOSa.
 - Teraz rozpoczyna się działanie BIOSa. Inicjalizuje on i sprawdza hardware, a następnie szuka bootowalnego urządzenia. Kolejność bootowania jest
     zapisana w konfiguracji BIOSa.
 - Jeśli BIOS próbuje bootować z dysku twardego, musi znaleźć bootsector. Na dyskach partycjonowanych z MBR, boot sector jest przechowywany w pierwszych
     446 bajtach pierwszego sektora. Ostatnie dwa bajty pierwszego sektora to powinny być `0x55, 0xaa`, co sygnalizuje że urządzenie jest bootowalne.
 - BIOS wczytuje pierwszy sektor kodu bootloadera do pamięci, pod adres 0x7c00, i przekazuje wykonywanie do niego.
 
**Bootloader**
 - Jest wiele bootloaderów które mogą bootować linuxa (np. GRUB2 albo syslinux) - w ogólności muszą interpretować tzw. `boot protocol`.
 - W przypadku GRUB - wykonywanie zaczyna się od boot.img. Kod jest bardzo prosty, i zawiera wskaźnik który skacze pod GRUB core image.
 - Core image zawiera diskboot.img, które czyta resztę bootloadera do pamięci (zawiera kernel GRUB2 i kod od filesystemów) i wykonuje grub_main
 - Bootloader musi wypełnić sporo pól w kernel setup headerze (zgodnie z boot protokołem).
 - Obecnie kernel nie ma swojego bootloadera, więc jeśli sie bezpośrednio spróbuje go uruchomić to nie zadziała.  