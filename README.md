2016 "Breaking Binaries" Fuzzer
============

This repository hosts the code that we "objEEdump" used to try and render a [segfault] with multiple binaries during the [Cyberstakes] 2016 "Breaking Binaries" exercise.

At this point, the code is a disgusting nightmare and is daunting to look through and review, but it should documented and stored nonetheless.

__It managed to break over 200 binaries during the exercise, which on average 50-70 more than the other competing teams!__

File & Directory Information
--------


* [`original_smart.py`](original_smart.py)

	This is the main code, the powerhouse [Python] script that does everything for the [fuzzer]. __This is what the interested onlooker should look at and play with.__ It was named "`smart`" because that rendition keeps track of the binaries it has already cracked, and it does not loop through them when it moves onto a new attack. The attacks we tried to implement were a [standard input] overflow, [command-line arguments] up to eight repeating, [integer bounds], and a theoretical command-line "options" attack, that would try combinations of command-line arguments like `-x` or `-a` (etc.) to try and guess at program interaction. This ended up being too time-consuming, so I didn't use it for the actual competition (but I _think_ the functionality is still there). 

	The code tests for a [segfault] by looking for changes in [`dmesg`][dmesg] output. Cheap, I know, but it works.


* [`this_is_the_old_one.py`](this_is_the_old_one.py)

	This old rendition of the script did not compartmentalize the attacks into different functions, so it generated the "fuzz" for the [fuzzing] in a much more dirty way (on top of all the code already being pretty overbloated).

* [`segfaults`](segfaults)

	This directory hosts experimental code that was never actually implemented; the hope was try and _automate a [buffer overflow] attack_ and actually attempt to gain a [shell]. I ended up testing this with the [Behemoth] challenge of the [Over the Wire]  wargames, but this made for a "one-trick pony" kind of solution (it was not readily replicable with other vulnerable [buffer overflows]). __An automated [buffer overflow] would be a worth while thing to implement, if at any point someone wants to try again.__

* [`clean.sh`](clean.sh)

	This was a dirty [`bash`][bash] script to kill any leftover processes and binaries that still happened to be running after execution.



[segfault]: https://en.wikipedia.org/wiki/Segmentation_fault
[Cyberstakes]: https://www.cyberstakesonline.com/
[buffer overflow]: https://en.wikipedia.org/wiki/Buffer_overflow
[buffer overflows]: https://en.wikipedia.org/wiki/Buffer_overflow
[shell]: https://en.wikipedia.org/wiki/Bash_%28Unix_shell%29
[bash]: https://en.wikipedia.org/wiki/Bash_%28Unix_shell%29
[Over the Wire]: http://overthewire.org/wargames/
[Behemoth]: http://overthewire.org/wargames/behemoth/
[Python]: https://www.python.org/
[fuzzer]: https://en.wikipedia.org/wiki/Fuzz_testing
[stdin]:https://en.wikipedia.org/wiki/Standard_streams#Standard_input_.28stdin.29
[standard input]: https://en.wikipedia.org/wiki/Standard_streams#Standard_input_.28stdin.29
[command-line arguments]: https://www.cs.bu.edu/teaching/c/program-args/
[integer bounds]: https://en.wikipedia.org/wiki/2147483647_%28number%29
[dmesg]: https://en.wikipedia.org/wiki/Dmesg