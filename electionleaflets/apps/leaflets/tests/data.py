MAPIT_POSTCODE_RETURN = """
{"wgs84_lat": 51.4599323104553, "coordsyst": "G", "shortcuts": {"WMC": 65913, "ward": 8323, "council": 2491}, "wgs84_lon": -0.0824797738988752, "postcode": "SE22 8DJ", "easting": 533310, "areas": {"900000": {"parent_area": null, "generation_high": 19, "all_names": {}, "id": 900000, "codes": {}, "name": "House of Commons", "country": "", "type_name": "UK Parliament", "generation_low": 1, "country_name": "-", "type": "WMP"}, "900001": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 900001, "codes": {}, "name": "European Parliament", "country": "", "type_name": "European Parliament", "generation_low": 1, "country_name": "-", "type": "EUP"}, "900002": {"parent_area": 900006, "generation_high": 23, "all_names": {}, "id": 900002, "codes": {}, "name": "London Assembly", "country": "E", "type_name": "London Assembly area (shared)", "generation_low": 1, "country_name": "England", "type": "LAE"}, "8323": {"parent_area": 2491, "generation_high": 23, "all_names": {}, "id": 8323, "codes": {"ons": "00BEGW", "gss": "E05000551", "unit_id": "11015"}, "name": "South Camberwell", "country": "E", "type_name": "London borough ward", "generation_low": 1, "country_name": "England", "type": "LBW"}, "900006": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 900006, "codes": {}, "name": "London Assembly", "country": "E", "type_name": "London Assembly area", "generation_low": 1, "country_name": "England", "type": "LAS"}, "2247": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 2247, "codes": {"unit_id": "41441"}, "name": "Greater London Authority", "country": "E", "type_name": "Greater London Authority", "generation_low": 1, "country_name": "England", "type": "GLA"}, "70189": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 70189, "codes": {"ons": "E01004048"}, "name": "Southwark 027C", "country": "E", "type_name": "Lower Layer Super Output Area (Full)", "generation_low": 13, "country_name": "England", "type": "OLF"}, "11822": {"parent_area": 2247, "generation_high": 23, "all_names": {}, "id": 11822, "codes": {"gss": "E32000010", "unit_id": "41446"}, "name": "Lambeth and Southwark", "country": "E", "type_name": "London Assembly constituency", "generation_low": 1, "country_name": "England", "type": "LAC"}, "41906": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 41906, "codes": {"ons": "E02000833"}, "name": "Southwark 027", "country": "E", "type_name": "Middle Layer Super Output Area (Generalised)", "generation_low": 13, "country_name": "England", "type": "OMG"}, "104567": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 104567, "codes": {"ons": "E01004048"}, "name": "Southwark 027C", "country": "E", "type_name": "Lower Layer Super Output Area (Generalised)", "generation_low": 13, "country_name": "England", "type": "OLG"}, "34712": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 34712, "codes": {"ons": "E02000833"}, "name": "Southwark 027", "country": "E", "type_name": "Middle Layer Super Output Area (Full)", "generation_low": 13, "country_name": "England", "type": "OMF"}, "65913": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 65913, "codes": {"gss": "E14000615", "unit_id": "25066"}, "name": "Camberwell and Peckham", "country": "E", "type_name": "UK Parliament constituency", "generation_low": 13, "country_name": "England", "type": "WMC"}, "2491": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 2491, "codes": {"ons": "00BE", "gss": "E09000028", "unit_id": "11013"}, "name": "Southwark Borough Council", "country": "E", "type_name": "London borough", "generation_low": 1, "country_name": "England", "type": "LBO"}, "11806": {"parent_area": null, "generation_high": 23, "all_names": {}, "id": 11806, "codes": {"ons": "07", "gss": "E15000007", "unit_id": "41428"}, "name": "London", "country": "E", "type_name": "European region", "generation_low": 1, "country_name": "England", "type": "EUR"}}, "northing": 175189}"""

LOCAL_BALLOT_WITH_CANDIDATES = {
        "url": "https://candidates.democracyclub.org.uk/api/next/ballots/local.westminster.st-jamess.2022-05-05/",
        "history_url": "https://candidates.democracyclub.org.uk/api/next/ballots/local.westminster.st-jamess.2022-05-05/history/",
        "results_url": "https://candidates.democracyclub.org.uk/api/next/results/local.westminster.st-jamess.2022-05-05/",
        "election": {
        "election_id": "local.westminster.2022-05-05",
        "url": "https://candidates.democracyclub.org.uk/api/next/elections/local.westminster.2022-05-05/",
        "name": "Westminster local election",
        "election_date": "2022-05-05",
        "current": False,
        "party_lists_in_use": False,
        "created": "2022-01-05T11:15:54.488413Z",
        "last_updated": "2024-01-16T18:09:16.371357Z"
        },
        "post": {
        "id": "gss:E05013806",
        "label": "St James's",
        "slug": "st-jamess",
        "created": "2022-01-05T11:15:54.795194Z",
        "last_updated": "2023-07-11T15:31:13.176989+01:00"
        },
        "winner_count": 3,
        "ballot_paper_id": "local.westminster.st-jamess.2022-05-05",
        "cancelled": False,
        "sopn": {
        "uploaded_file": "https://s3.eu-west-2.amazonaws.com/static-candidates.democracyclub.org.uk/media/official_documents/local.westminster.st-jamess.2022-05-05/statement-of-persons-nominated.pdf",
        "source_url": "https://www.westminster.gov.uk/media/document/st-jamess-ward-statement-of-persons-nominated"
        },
        "candidates_locked": True,
        "candidacies": [
        {
          "elected": True,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP52/",
            "ec_id": "PP52",
            "name": "Conservative and Unionist Party",
            "legacy_slug": "party:52",
            "created": "2018-09-17T15:01:08.048032+01:00",
            "modified": "2024-11-19T02:06:24.008964Z"
          },
          "party_name": "Conservative and Unionist Party",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-06T15:06:56.273587+01:00",
          "modified": "2022-05-06T04:12:08.754253+01:00",
          "person": {
            "id": 41112,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/41112/",
            "name": "Louise Hyams"
          },
          "result": {
            "elected": True,
            "num_ballots": 979
          }
        },
        {
          "elected": True,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP52/",
            "ec_id": "PP52",
            "name": "Conservative and Unionist Party",
            "legacy_slug": "party:52",
            "created": "2018-09-17T15:01:08.048032+01:00",
            "modified": "2024-11-19T02:06:24.008964Z"
          },
          "party_name": "Conservative and Unionist Party",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-06T15:06:56.327388+01:00",
          "modified": "2022-05-06T04:12:08.836342+01:00",
          "person": {
            "id": 41114,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/41114/",
            "name": "Tim Mitchell"
          },
          "result": {
            "elected": True,
            "num_ballots": 965
          }
        },
        {
          "elected": True,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP52/",
            "ec_id": "PP52",
            "name": "Conservative and Unionist Party",
            "legacy_slug": "party:52",
            "created": "2018-09-17T15:01:08.048032+01:00",
            "modified": "2024-11-19T02:06:24.008964Z"
          },
          "party_name": "Conservative and Unionist Party",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-06T15:06:56.389619+01:00",
          "modified": "2022-05-06T04:12:08.912046+01:00",
          "person": {
            "id": 41117,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/41117/",
            "name": "Mark Shearer"
          },
          "result": {
            "elected": True,
            "num_ballots": 954
          }
        },
        {
          "elected": False,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP53/",
            "ec_id": "PP53",
            "name": "Labour Party",
            "legacy_slug": "party:53",
            "created": "2018-09-17T15:01:09.580623+01:00",
            "modified": "2024-11-15T02:06:31.822331Z"
          },
          "party_name": "Labour Party",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-07T16:50:03.294367+01:00",
          "modified": "2022-04-07T16:50:03.296651+01:00",
          "person": {
            "id": 92971,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/92971/",
            "name": "Karina Darbin"
          },
          "result": {
            "elected": False,
            "num_ballots": 789
          }
        },
        {
          "elected": False,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP53/",
            "ec_id": "PP53",
            "name": "Labour Party",
            "legacy_slug": "party:53",
            "created": "2018-09-17T15:01:09.580623+01:00",
            "modified": "2024-11-15T02:06:31.822331Z"
          },
          "party_name": "Labour Party",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-07T16:50:03.479288+01:00",
          "modified": "2022-04-07T16:50:03.481537+01:00",
          "person": {
            "id": 92973,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/92973/",
            "name": "Paul Raphael James Spence"
          },
          "result": {
            "elected": False,
            "num_ballots": 701
          }
        },
        {
          "elected": False,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP53/",
            "ec_id": "PP53",
            "name": "Labour Party",
            "legacy_slug": "party:53",
            "created": "2018-09-17T15:01:09.580623+01:00",
            "modified": "2024-11-15T02:06:31.822331Z"
          },
          "party_name": "Labour Party",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-07T16:50:03.416071+01:00",
          "modified": "2022-04-07T16:50:03.418536+01:00",
          "person": {
            "id": 92972,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/92972/",
            "name": "Nigel Stephen Medforth"
          },
          "result": {
            "elected": False,
            "num_ballots": 700
          }
        },
        {
          "elected": False,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP90/",
            "ec_id": "PP90",
            "name": "Liberal Democrats",
            "legacy_slug": "party:90",
            "created": "2018-09-17T15:01:08.091504+01:00",
            "modified": "2024-11-19T02:06:24.311670Z"
          },
          "party_name": "Liberal Democrats",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-07T16:50:03.221833+01:00",
          "modified": "2022-04-07T16:50:03.224684+01:00",
          "person": {
            "id": 92970,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/92970/",
            "name": "Michael Anthony Ahearne"
          },
          "result": {
            "elected": False,
            "num_ballots": 295
          }
        },
        {
          "elected": False,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP90/",
            "ec_id": "PP90",
            "name": "Liberal Democrats",
            "legacy_slug": "party:90",
            "created": "2018-09-17T15:01:08.091504+01:00",
            "modified": "2024-11-19T02:06:24.311670Z"
          },
          "party_name": "Liberal Democrats",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-07T16:50:03.341602+01:00",
          "modified": "2022-04-07T16:50:03.343789+01:00",
          "person": {
            "id": 41110,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/41110/",
            "name": "Paul Diggory"
          },
          "result": {
            "elected": False,
            "num_ballots": 281
          }
        },
        {
          "elected": False,
          "party_list_position": None,
          "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP90/",
            "ec_id": "PP90",
            "name": "Liberal Democrats",
            "legacy_slug": "party:90",
            "created": "2018-09-17T15:01:08.091504+01:00",
            "modified": "2024-11-19T02:06:24.311670Z"
          },
          "party_name": "Liberal Democrats",
          "party_description_text": "",
          "deselected": False,
          "deselected_source": "",
          "created": "2022-04-07T16:50:03.544670+01:00",
          "modified": "2022-04-07T16:50:03.546973+01:00",
          "person": {
            "id": 92974,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/92974/",
            "name": "Alice Anne Wells"
          },
          "result": {
            "elected": False,
            "num_ballots": 249
          }
        }
        ],
        "created": "2022-01-05T11:15:54.801506Z",
        "last_updated": "2024-01-16T18:09:16.478549Z",
        "replaces": None,
        "replaced_by": None,
        "uncontested": False,
        "results": {
        "num_turnout_reported": 2057,
        "turnout_percentage": 30,
        "num_spoilt_ballots": None,
        "source": "https://www.westminster.gov.uk/about-council/democracy/elections-referendums-and-how-vote/local-elections-5-may-2022/st-jamess",
        "total_electorate": 6943
        },
        "voting_system": "FPTP"
        }
