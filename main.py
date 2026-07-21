from flask import Flask, jsonify
from requests import get
from bs4 import BeautifulSoup
from libs import data_time_validator
from datetime import datetime

# target site to test : https://www.ingeteam.com/.well-known/security.txt

app = Flask(__name__)

@app.route('/get_sec_txt/<domain>')
def get_security_txt_file(domain: str):
    score = 0
    sec_file = 'https://' + domain + '/.well-known/security.txt'
    req = get(url=sec_file)
    if req.status_code == 200:
        sendreq = req.text.lower()
        datas = dict()

        for dt in sendreq.splitlines():
            getdt = dt.lower()

            if getdt.startswith('contact:'):
                data = dt.split(':', maxsplit=1)
                if 'mailto:' in data[1].strip():
                    getmail = data[1].split(':')[1]
                else:
                    getmail = data[1]

                if getmail:
                    datas.update({'contact': getmail.strip()})
                    score += 5

            if getdt.startswith('expires:'):
                data = dt.split(':', maxsplit=1)
                date = data[1].split('t')[0].split('-')
                crt_date = date[-1] + '/' + date[1] + '/' + date[0].strip()
                time = datetime.strptime(
                    data[1].split('t')[1].split('.')[0],
                    "%H:%M:%S"
                )

                is_valid = data_time_validator(
                    data[1].split('t')[0],
                    time.strftime("%H:%M:%S")
                )

                if crt_date and time:
                    datas.update({
                        'expires': {
                            'date': crt_date,
                            'time': time.strftime("%I:%M:%S %p"),
                            'valid': 'yes' if is_valid else 'no'
                        }
                    })
                    score += 5

            if getdt.startswith('policy:'):
                data = dt.split(':', maxsplit=1)
                if data[1]:
                    datas.update({'policy': data[1].strip()})
                    score += 5

            if getdt.startswith('encryption:'):
                data = dt.split(':', maxsplit=1)
                if data[1]:
                    datas.update({'encryption': data[1].strip()})
                    score += 5

            if getdt.startswith('preferred-languages:'):
                data = dt.split(':', maxsplit=1)
                lang = data[1].strip()
                if lang:
                    datas.update({
                        'preferred-languages': 'English' if lang == 'en' else lang
                    })
                    score += 5

        datas.update({'score percentage': f'{int(score/5)}/5'})
        return datas

def check_public_program(pname: str):
    pname = (pname or "").strip()
    if not pname:
        return {"error": "Program name is required"}

    bugcrowd_url = f"https://bugcrowd.com/engagements/{pname}"
    hackerone_url = f"https://hackerone.com/{pname}"

    try:
        bugcrowd_resp = get(bugcrowd_url, timeout=10)
        hackerone_resp = get(hackerone_url, timeout=10)

        return {
            "program_name": pname,
            "bugcrowd": {
                "url": bugcrowd_url,
                "status_code": bugcrowd_resp.status_code,
                "exists": bugcrowd_resp.status_code == 200,
            },
            "hackerone": {
                "url": hackerone_url,
                "status_code": hackerone_resp.status_code,
                "exists": hackerone_resp.status_code == 200,
            },
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/check_for_pp/<pname>')
def public_program_route(pname: str):
    return jsonify(check_public_program(pname))

if __name__ == '__main__':
    app.run(debug=True)