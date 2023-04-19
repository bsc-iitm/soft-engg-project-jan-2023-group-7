import requests
from web.models import Similar__Drug__Search
from web.app import app, db


def searchSimilarDrug(input):
    sol = []
    get_request_count = 0
    for target_chembl_id, smile in input.items():
        if get_request_count == 25:
            # time.sleep(15)
            get_request_count = 0
        try:
            res = requests.get(
                f"https://www.ebi.ac.uk/chembl/api/data/similarity/"
                + smile
                + "/50?limit=1000&offset=0&format=json",
                timeout=60,
            )
            get_request_count += 1
            if res.status_code == 200:
                data = res.json()
                if len(data.get("molecules", "")) > 0:
                    for i in range(0, len(data["molecules"])):
                        if get_request_count == 25:
                            # time.sleep(15)
                            get_request_count = 0
                        tmp_list = []
                        tmp_list.append(target_chembl_id)
                        mcid = data["molecules"][i]["molecule_chembl_id"]
                        tmp_list.append(mcid)
                        mcid_res = requests.get(
                            "https://www.ebi.ac.uk/chembl/api/data/activity/search?q="
                            + mcid
                            + "&limit=1000&offset=0&format=json",
                            timeout=60,
                        )
                        get_request_count += 1
                        if mcid_res.status_code == 200:
                            mcid_data = mcid_res.json()
                            if len(mcid_data.get("activities")) > 0:
                                if (
                                    mcid_data["activities"][0]["standard_type"] is None
                                    or target_chembl_id is None
                                    or mcid_data["activities"][0]["standard_type"]
                                    in {"Activity", "Potency", "Imax", "Ki"}
                                    or mcid is None
                                    or mcid_data["activities"][0]["standard_value"]
                                    is None
                                    or mcid_data["activities"][0]["standard_units"]
                                    is None
                                    or mcid_data["activities"][0]["canonical_smiles"]
                                    is None
                                ):
                                    continue
                                tmp_list.append(
                                    mcid_data["activities"][0]["standard_type"]
                                )
                                tmp_list.append(
                                    mcid_data["activities"][0]["standard_value"]
                                )
                                tmp_list.append(
                                    mcid_data["activities"][0]["standard_units"]
                                )
                                tmp_list.append(
                                    mcid_data["activities"][0]["canonical_smiles"]
                                )
                                tmp_list.append(
                                    int(
                                        (
                                            float(data["molecules"][i]["similarity"])
                                            / 100.0
                                        )
                                        * 10**2
                                    )
                                    / 10**2
                                )
                                entry = Similar__Drug__Search(
                                    ChemblID=tmp_list[0],
                                    SimilarityID=tmp_list[1],
                                    AffinityType=tmp_list[2],
                                    Value=tmp_list[3],
                                    Unit=tmp_list[4],
                                    Smile=tmp_list[5],
                                    Tanimato=tmp_list[6]
                                )
                                db.session.add(entry)
                                db.session.commit()
                                sol.append(tmp_list)
                        # f = open(
                        #     "/home/sacsin/Music/pyqt-browser_application/bakwas.txt",
                        #     "a",
                        # )
                        # print(tmp_list, file=f)
                        # # print(tmp_list)
                        # f.close()
        except:
            pass

    return sol
