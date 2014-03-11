dns_brute.rb
============

A threaded ruby script to bruteforce DNS entries that supports custom character sets and generated host filters.

Installation:
-------------
> Ruby 1.9.3

Usage: dns_brute [options]
--------------------------
>-t, --threads THEADS             Number of threads to use. (Default: 30)
>-d, --domain DOMAINS             The target domain to scan.
> -D, --depth DEPTH                The number of characters deep to go. (Default: 3)
> -w, --wordlist WORDLIST          Optional dictionary list to test.
> -n, --nameserver NAMESERVER      DNS server to use for lookups. You can specify this multiple times. (Default: 8.8.8.8)
> -c, --charset CHARSET            The character set use to generate the names using PCRE character classes. (Default: [a-z0-9])
> -p, --pattern PATTERN            Only send requests for generated hosts matching this pattern. (Default: .*)

Examples:
---------
* Test only single character hostnames for google.com
> ruby dns_brute.rb -d google.com -D 1
> d.google.com 21599 IN CNAME www3.l.google.com
> m.google.com 21599 IN CNAME mobile.l.google.com
> w.google.com 21599 IN CNAME www3.l.google.com

* Test four character hostnames using only w's and numbers and only test hosts matching www\d with 100 threads
> ruby dns_brute.rb -t 100 -n 207.46.75.254 -d microsoft.com -D 4 -c '[w\d]' -p 'www\d' 
> www4.microsoft.com 3600 IN A 65.55.39.12
> www4.microsoft.com 3600 IN A 207.46.31.61
> www6.microsoft.com 3600 IN A 65.55.39.12
> www6.microsoft.com 3600 IN A 207.46.31.61
> www9.microsoft.com 3600 IN A 65.55.39.12
> www9.microsoft.com 3600 IN A 207.46.31.61
> www2.microsoft.com 3600 IN A 65.55.39.12
> www2.microsoft.com 3600 IN A 207.46.31.61
> www7.microsoft.com 3600 IN A 65.55.39.12
> www7.microsoft.com 3600 IN A 207.46.31.61
> www3.microsoft.com 3600 IN A 65.55.39.12
> www3.microsoft.com 3600 IN A 207.46.31.61
> www1.microsoft.com 3600 IN A 65.55.39.12
> www1.microsoft.com 3600 IN A 207.46.31.61
> www8.microsoft.com 3600 IN A 65.55.39.12
> www8.microsoft.com 3600 IN A 207.46.31.61
> www5.microsoft.com 3600 IN A 207.46.31.61
> www5.microsoft.com 3600 IN A 65.55.39.12
> www0.microsoft.com 3600 IN A 65.55.39.12
> www0.microsoft.com 3600 IN A 207.46.31.61
