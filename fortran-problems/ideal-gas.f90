program ideal_gas

implicit none

!* Variables
integer :: pressure
integer, parameter :: temp = 273
REAL :: volume
REAL, parameter :: n = 6.02e23
REAL, parameter :: r = 8.314

!* Calculates the volume over a range of pressures using the Ideal Gas Law
DO pressure = 1, 1001, 100

    volume = (n * r * temp) / pressure
    print *, 'At a pressure of', pressure, 'kPA, the volume is', volume, 'L'

END DO 

end program ideal_gas