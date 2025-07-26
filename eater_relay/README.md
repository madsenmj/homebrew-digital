# Ben Eater 8-bit Computer Using Relays

This project is a mash-up of [Ben Eater's tutorial](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU), the [Relay Computer](https://www.relaycomputer.co.uk/), [Harry Porter's Relay Computer](https://web.cecs.pdx.edu/~harry/Relay/index.html), and the [DiPDoT Relay Computer](https://www.youtube.com/playlist?list=PL9PsHGpOhJ-vR_PPiXtn8wHm9GdPqBY8A), all implemented using Digital components. See the [Harry Porter paper](https://web.cecs.pdx.edu/~harry/Relay/RelayPaper.pdf) as well.

Although this does not implement all of the ALU functionality, the sample program demonstrates the capabilities, utilizing the Add, Not and Increment functionality to subtract numbers. A third register "A" was added to avoid oscillations at the end of an ALU operation (not necessary in the Eater computer). The ALU dumps its result into the A register and the result is then moved into the B register.
