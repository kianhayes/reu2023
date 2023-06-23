PROGRAM current_calculation

IMPLICIT NONE

INTEGER :: T, vd
REAL :: current
REAL, PARAMETER :: q = 1.602e-19, k = 1.38e-23, io = 2e-6

DO T = 75, 126, 25
    DO vd = -1, 1

        current = io*(exp(q*vd / k*T) - 1)
        PRINT *, 'The diode current at voltage', vd, 'volts and a temperature of', T, 'K is', current, 'A'

    END DO
END DO

END PROGRAM current_calculation