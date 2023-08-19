## urlFollow

Receives URLs as stdin or input file. Follows any potential redirects and print back the end base URL.

Examples:
```
$ cat urls.txt | ./urlFollow.py

$ cat urls.txt | urlFollow.py -o end-urls.txt -t 10 -r redirects.txt
```

Help:
```
$ urlFollow.py -h
usage: urlFollow.py [-h] [-i INFILE] [-o OUTFILE] [-t THREADS] [-r REDIRECTSFILE]

endUrl.py find final url after redirection for a list of urls read from stdin

options:
  -h, --help            show this help message and exit
  -i INFILE, --input INFILE
                        input file [if none, stdin]
  -o OUTFILE, --outfile OUTFILE
                        Output file to write urls [if none, only stdout]
  -t THREADS, --threads THREADS
                        Number of parallel threads [default 4]
  -r REDIRECTSFILE, --redirectsfile REDIRECTSFILE
                        File location to write redirections, "|" separated
```