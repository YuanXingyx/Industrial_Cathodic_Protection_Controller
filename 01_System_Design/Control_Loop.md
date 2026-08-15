# Control Loop

The controlled variable is simulated pipe-to-reference potential. The manipulated variable will be a bounded low-voltage output command. Sign convention, plant gain and sample time are `TBD` and must be measured before enabling a controller.

Development order: open-loop acquisition → PWM characterization → RC plant characterization → bounded P → bounded PI. The PI code present in this repository is an inactive interface skeleton, not a validated control algorithm.
