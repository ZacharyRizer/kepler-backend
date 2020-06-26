from astropy.time import Time
from astropy import units as u
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric, get_body, get_moon


def calculate_trip(depart, arrive, date):

    t = Time(date)
    solar_system_ephemeris.set('builtin')
    start = get_body_barycentric(depart, t)
    end = get_body_barycentric(arrive, t)

    distance = ((start.x - end.x)**2 + (start.y - end.y)**2 + (start.z - end.z)**2)**(1/2)
    return distance.to(u.km)

