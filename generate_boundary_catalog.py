#!/usr/bin/env python3
"""
Generate boundary catalog JSON from the output folder structure.

Scans the misc folder and generates a JSON catalog with download links,
metadata, and OSM relation information for each boundary.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional


def parse_folder_name(folder_name: str) -> Optional[Dict[str, str]]:
    """
    Parse folder name to extract relation ID and name.

    Expected format: relation_<id>_<name>
    Example: relation_50046_denmark

    Returns dict with 'relation_id' and 'name' or None if parse fails
    """
    match = re.match(r"relation_(\d+)_(.+)", folder_name)
    if match:
        return {"relation_id": match.group(1), "name": match.group(2).replace("_", " ").title()}
    return None


def get_country_name_from_iso(iso_code: str) -> str:
    """
    Map ISO codes to country names.
    This is a basic mapping - extend as needed.
    """
    country_map = {
        "AF": "Afghanistan",
        "AX": "Åland Islands",
        "AL": "Albania",
        "DZ": "Algeria",
        "AS": "American Samoa",
        "AD": "Andorra",
        "AO": "Angola",
        "AI": "Anguilla",
        "AQ": "Antarctica",
        "AG": "Antigua and Barbuda",
        "AR": "Argentina",
        "AM": "Armenia",
        "AW": "Aruba",
        "AU": "Australia",
        "AT": "Austria",
        "AZ": "Azerbaijan",
        "BS": "Bahamas",
        "BH": "Bahrain",
        "BD": "Bangladesh",
        "BB": "Barbados",
        "BY": "Belarus",
        "BE": "Belgium",
        "BZ": "Belize",
        "BJ": "Benin",
        "BM": "Bermuda",
        "BT": "Bhutan",
        "BO": "Bolivia (Plurinational State of)",
        "BQ": "Bonaire, Sint Eustatius and Saba",
        "BA": "Bosnia and Herzegovina",
        "BW": "Botswana",
        "BV": "Bouvet Island",
        "BR": "Brazil",
        "IO": "British Indian Ocean Territory",
        "BN": "Brunei Darussalam",
        "BG": "Bulgaria",
        "BF": "Burkina Faso",
        "BI": "Burundi",
        "CV": "Cabo Verde",
        "KH": "Cambodia",
        "CM": "Cameroon",
        "CA": "Canada",
        "KY": "Cayman Islands",
        "CF": "Central African Republic",
        "TD": "Chad",
        "CL": "Chile",
        "CN": "China",
        "CX": "Christmas Island",
        "CC": "Cocos (Keeling) Islands",
        "CO": "Colombia",
        "KM": "Comoros",
        "CG": "Congo",
        "CD": "Congo, Democratic Republic of the",
        "CK": "Cook Islands",
        "CR": "Costa Rica",
        "CI": "Côte d'Ivoire",
        "HR": "Croatia",
        "CU": "Cuba",
        "CW": "Curaçao",
        "CY": "Cyprus",
        "CZ": "Czechia",
        "DK": "Denmark",
        "DJ": "Djibouti",
        "DM": "Dominica",
        "DO": "Dominican Republic",
        "EC": "Ecuador",
        "EG": "Egypt",
        "SV": "El Salvador",
        "GQ": "Equatorial Guinea",
        "ER": "Eritrea",
        "EE": "Estonia",
        "SZ": "Eswatini",
        "ET": "Ethiopia",
        "FK": "Falkland Islands (Malvinas)",
        "FO": "Faroe Islands",
        "FJ": "Fiji",
        "FI": "Finland",
        "FR": "France",
        "GF": "French Guiana",
        "PF": "French Polynesia",
        "TF": "French Southern Territories",
        "GA": "Gabon",
        "GM": "Gambia",
        "GE": "Georgia",
        "DE": "Germany",
        "GH": "Ghana",
        "GI": "Gibraltar",
        "GR": "Greece",
        "GL": "Greenland",
        "GD": "Grenada",
        "GP": "Guadeloupe",
        "GU": "Guam",
        "GT": "Guatemala",
        "GG": "Guernsey",
        "GN": "Guinea",
        "GW": "Guinea-Bissau",
        "GY": "Guyana",
        "HT": "Haiti",
        "HM": "Heard Island and McDonald Islands",
        "VA": "Holy See",
        "HN": "Honduras",
        "HK": "Hong Kong",
        "HU": "Hungary",
        "IS": "Iceland",
        "IN": "India",
        "ID": "Indonesia",
        "IR": "Iran (Islamic Republic of)",
        "IQ": "Iraq",
        "IE": "Ireland",
        "IM": "Isle of Man",
        "IL": "Israel",
        "IT": "Italy",
        "JM": "Jamaica",
        "JP": "Japan",
        "JE": "Jersey",
        "JO": "Jordan",
        "KZ": "Kazakhstan",
        "KE": "Kenya",
        "KI": "Kiribati",
        "KP": "Korea (Democratic People's Republic of)",
        "KR": "Korea, Republic of",
        "KW": "Kuwait",
        "KG": "Kyrgyzstan",
        "LA": "Lao People's Democratic Republic",
        "LV": "Latvia",
        "LB": "Lebanon",
        "LS": "Lesotho",
        "LR": "Liberia",
        "LY": "Libya",
        "LI": "Liechtenstein",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "MO": "Macao",
        "MG": "Madagascar",
        "MW": "Malawi",
        "MY": "Malaysia",
        "MV": "Maldives",
        "ML": "Mali",
        "MT": "Malta",
        "MH": "Marshall Islands",
        "MQ": "Martinique",
        "MR": "Mauritania",
        "MU": "Mauritius",
        "YT": "Mayotte",
        "MX": "Mexico",
        "FM": "Micronesia (Federated States of)",
        "MD": "Moldova, Republic of",
        "MC": "Monaco",
        "MN": "Mongolia",
        "ME": "Montenegro",
        "MS": "Montserrat",
        "MA": "Morocco",
        "MZ": "Mozambique",
        "MM": "Myanmar",
        "NA": "Namibia",
        "NR": "Nauru",
        "NP": "Nepal",
        "NL": "Netherlands",
        "NC": "New Caledonia",
        "NZ": "New Zealand",
        "NI": "Nicaragua",
        "NE": "Niger",
        "NG": "Nigeria",
        "NU": "Niue",
        "NF": "Norfolk Island",
        "MK": "North Macedonia",
        "MP": "Northern Mariana Islands",
        "NO": "Norway",
        "OM": "Oman",
        "PK": "Pakistan",
        "PW": "Palau",
        "PS": "Palestine, State of",
        "PA": "Panama",
        "PG": "Papua New Guinea",
        "PY": "Paraguay",
        "PE": "Peru",
        "PH": "Philippines",
        "PN": "Pitcairn",
        "PL": "Poland",
        "PT": "Portugal",
        "PR": "Puerto Rico",
        "QA": "Qatar",
        "RE": "Réunion",
        "RO": "Romania",
        "RU": "Russian Federation",
        "RW": "Rwanda",
        "BL": "Saint Barthélemy",
        "SH": "Saint Helena, Ascension and Tristan da Cunha",
        "KN": "Saint Kitts and Nevis",
        "LC": "Saint Lucia",
        "MF": "Saint Martin (French part)",
        "PM": "Saint Pierre and Miquelon",
        "VC": "Saint Vincent and the Grenadines",
        "WS": "Samoa",
        "SM": "San Marino",
        "ST": "Sao Tome and Principe",
        "SA": "Saudi Arabia",
        "SN": "Senegal",
        "RS": "Serbia",
        "SC": "Seychelles",
        "SL": "Sierra Leone",
        "SG": "Singapore",
        "SX": "Sint Maarten (Dutch part)",
        "SK": "Slovakia",
        "SI": "Slovenia",
        "SB": "Solomon Islands",
        "SO": "Somalia",
        "ZA": "South Africa",
        "GS": "South Georgia and the South Sandwich Islands",
        "SS": "South Sudan",
        "ES": "Spain",
        "LK": "Sri Lanka",
        "SD": "Sudan",
        "SR": "Suriname",
        "SJ": "Svalbard and Jan Mayen",
        "SE": "Sweden",
        "CH": "Switzerland",
        "SY": "Syrian Arab Republic",
        "TW": "Taiwan, Province of China",
        "TJ": "Tajikistan",
        "TZ": "Tanzania, United Republic of",
        "TH": "Thailand",
        "TL": "Timor-Leste",
        "TG": "Togo",
        "TK": "Tokelau",
        "TO": "Tonga",
        "TT": "Trinidad and Tobago",
        "TN": "Tunisia",
        "TR": "Turkey",
        "TM": "Turkmenistan",
        "TC": "Turks and Caicos Islands",
        "TV": "Tuvalu",
        "UG": "Uganda",
        "UA": "Ukraine",
        "AE": "United Arab Emirates",
        "GB": "United Kingdom of Great Britain and Northern Ireland",
        "US": "United States of America",
        "UM": "United States Minor Outlying Islands",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VU": "Vanuatu",
        "VE": "Venezuela (Bolivarian Republic of)",
        "VN": "Viet Nam",
        "VG": "Virgin Islands (British)",
        "VI": "Virgin Islands (U.S.)",
        "WF": "Wallis and Futuna",
        "EH": "Western Sahara",
        "YE": "Yemen",
        "ZM": "Zambia",
        "ZW": "Zimbabwe",
    }
    return country_map.get(iso_code, iso_code)


def scan_output_folder(base_path: str = "misc") -> List[Dict]:
    """
    Scan the output folder and generate boundary catalog entries.

    Folder structure expected:
    misc/
      <ISO_CODE>/
        <admin_level>/
          relation_<id>_<name>/
            relation_<id>_<name>.geojson.zip
            relation_<id>_<name>.shp.zip
            relation_<id>_<name>.gpkg.zip
            relation_<id>_<name>.mapinfo.zip
            relation_<id>_<name>_land.geojson.zip  (optional)
            relation_<id>_<name>_land.shp.zip      (optional)
            relation_<id>_<name>_land.gpkg.zip     (optional)
            relation_<id>_<name>_land.mapinfo.zip  (optional)
    """
    catalog = []
    base_path = Path(base_path)

    if not base_path.exists():
        print(f"Warning: {base_path} does not exist")
        return catalog

    # Iterate through ISO code folders
    for iso_folder in sorted(base_path.iterdir()):
        if not iso_folder.is_dir():
            continue

        iso_code = iso_folder.name
        parent_country = get_country_name_from_iso(iso_code)

        # Iterate through admin level folders
        for admin_level_folder in sorted(iso_folder.iterdir()):
            if not admin_level_folder.is_dir():
                continue

            try:
                admin_level = int(admin_level_folder.name)
            except ValueError:
                continue

            # Iterate through relation folders
            for relation_folder in sorted(admin_level_folder.iterdir()):
                if not relation_folder.is_dir():
                    continue

                parsed = parse_folder_name(relation_folder.name)
                if not parsed:
                    continue

                relation_id = parsed["relation_id"]
                name = parsed["name"]

                # Check for maritime and land variants
                base_name = relation_folder.name
                has_geojson = (relation_folder / f"{base_name}.geojson.zip").exists()
                has_shp = (relation_folder / f"{base_name}.shp.zip").exists()
                has_gpkg = (relation_folder / f"{base_name}.gpkg.zip").exists()
                has_mapinfo = (relation_folder / f"{base_name}.mapinfo.zip").exists()
                has_land_geojson = (relation_folder / f"{base_name}_land.geojson.zip").exists()
                has_land_shp = (relation_folder / f"{base_name}_land.shp.zip").exists()
                has_land_gpkg = (relation_folder / f"{base_name}_land.gpkg.zip").exists()
                has_land_mapinfo = (relation_folder / f"{base_name}_land.mapinfo.zip").exists()

                # URLs mirror the exact directory structure
                # e.g., LU/6/relation_123_folder/relation_123_folder.geojson.zip

                # Generate maritime entry if files exist
                # Use 'm' for maritime, 'l' for land to save space
                if has_geojson or has_shp or has_gpkg or has_mapinfo:
                    catalog.append(
                        {
                            "parent": parent_country,
                            "iso_code": iso_code,
                            "admin_level": admin_level,
                            "name": name,
                            "relation_id": relation_id,
                            "slug": base_name.replace(f"relation_{relation_id}_", ""),
                            "type": "m",
                        }
                    )

                # Generate land entry if land files exist
                if has_land_geojson or has_land_shp or has_land_gpkg or has_land_mapinfo:
                    catalog.append(
                        {
                            "parent": parent_country,
                            "iso_code": iso_code,
                            "admin_level": admin_level,
                            "name": name,
                            "relation_id": relation_id,
                            "slug": base_name.replace(f"relation_{relation_id}_", ""),
                            "type": "l",
                        }
                    )

    return catalog


def main():
    """Main function to generate and save the catalog."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate boundary catalog JSON from output folder structure")
    parser.add_argument("scan_folder", nargs="?", default="misc", help="Path to the folder to scan (default: misc)")
    args = parser.parse_args()

    # Generate catalog
    catalog = scan_output_folder(args.scan_folder)

    # Save to JSON file in the src directory (optimized for production)
    script_dir = Path(__file__).parent
    src_dir = script_dir / "src"
    output_file = src_dir / "boundary_catalog.json"

    # Save minimized version (no whitespace) to reduce file size
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(catalog, f, separators=(",", ":"), ensure_ascii=False)

    import os

    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"Generated catalog with {len(catalog)} entries")
    print(f"Saved to {output_file} ({file_size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
