dns_brute.rb
============

A threaded ruby script to bruteforce DNS entries that supports custom character sets and generated host filters.

Installation:
-------------
> Ruby 1.9.3

Usage: dns_brute [options]
--------------------------
> -t, --threads THEADS             Number of threads to use. (Default: 30)<br />
> -d, --domain DOMAINS             The target domain to scan.<br />
> -D, --depth DEPTH                The number of characters deep to go. (Default: 3)<br />
> -w, --wordlist WORDLIST          Optional dictionary list to test.<br />
> -n, --nameserver NAMESERVER      DNS server to use for lookups. You can specify this multiple times. (Default: 8.8.8.8)<br />
> -c, --charset CHARSET            The character set use to generate the names using PCRE character classes. (Default: [a-z0-9])<br />
> -p, --pattern PATTERN            Only send requests for generated hosts matching this pattern. (Default: .*)

Examples:
---------
* Test only single character hostnames for google.com<br />
> ruby dns_brute.rb -d google.com -D 1<br />
> d.google.com 21599 IN CNAME www3.l.google.com<br />
> m.google.com 21599 IN CNAME mobile.l.google.com<br />
> w.google.com 21599 IN CNAME www3.l.google.com<br />

* Test four character hostnames using only w's and numbers and only test hosts matching www\d with 100 threads<br />
> ruby dns_brute.rb -t 100 -n 207.46.75.254 -d microsoft.com -D 4 -c '[w\d]' -p 'www\d'<br />
> www4.microsoft.com 3600 IN A 65.55.39.12<br />
> www4.microsoft.com 3600 IN A 207.46.31.61<br />
> www6.microsoft.com 3600 IN A 65.55.39.12<br />
> www6.microsoft.com 3600 IN A 207.46.31.61<br />
> www9.microsoft.com 3600 IN A 65.55.39.12<br />
> www9.microsoft.com 3600 IN A 207.46.31.61<br />
> www2.microsoft.com 3600 IN A 65.55.39.12<br />
> www2.microsoft.com 3600 IN A 207.46.31.61<br />
> www7.microsoft.com 3600 IN A 65.55.39.12<br />
> www7.microsoft.com 3600 IN A 207.46.31.61<br />
> www3.microsoft.com 3600 IN A 65.55.39.12<br />
> www3.microsoft.com 3600 IN A 207.46.31.61<br />
> www1.microsoft.com 3600 IN A 65.55.39.12<br />
> www1.microsoft.com 3600 IN A 207.46.31.61<br />
> www8.microsoft.com 3600 IN A 65.55.39.12<br />
> www8.microsoft.com 3600 IN A 207.46.31.61<br />
> www5.microsoft.com 3600 IN A 207.46.31.61<br />
> www5.microsoft.com 3600 IN A 65.55.39.12<br />
> www0.microsoft.com 3600 IN A 65.55.39.12<br />
> www0.microsoft.com 3600 IN A 207.46.31.61<br />
