

def county_namer(block, encoding='latin1'):
    # {'INTPTLAT': '32.536382', 'NAME': 'Autauga County', 'INTPTLONG': '-86.644490', 'USPS': 'AL', 'AWATER_SQMI': '9.952', 'AWATER': '25775735', 'ANSICODE': '00161526', 'HU10': '22135', 'POP10': '54571', 'ALAND_SQMI': '594.436', 'GEOID': '01001', 'ALAND': '1539582278'}
    name = block['NAME'].lower().replace(" ", "-").decode(encoding)
    state_name = block['USPS'].lower()
    return "ocd-division/country:us/state:%s/county:%s" % (state_name, name)


def place_namer(block, encoding='latin1'):
    name = block['NAME'].lower().replace(" ", "-").decode(encoding)
    state_name = block['USPS'].lower()
    return "ocd-division/country:us/state:%s/place:%s" % (state_name, name)



PLACES = {
    "Gaz_counties_national.txt": {
        "namer": county_namer
    },
    "Gaz_places_national.txt": {
        "namer": place_namer
    }
}
