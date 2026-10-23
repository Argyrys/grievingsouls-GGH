# Veritas Vision — Manual Test Checklist (Arpita)

Run BEFORE demo (day: 23 Oct). Server: run.bat → http://127.0.0.1:8000/

| # | Target URL | Expected | Tier | Pass |
|---|-----------|----------|------|------|
| 1 | http://127.0.0.1:8000/api/health | {"status":"ok"} | - | ☐ |
| 2 | /mocks/ms-login-canvas.html | BLOCK >=0.90, brand Microsoft | multimodal | ☐ |
| 3 | /mocks/netflix-svg.html | BLOCK, brand Netflix | multimodal | ☐ |
| 4 | /mocks/chase-mfa.html | BLOCK >=0.95, brand Chase | multimodal | ☐ |
| 5 | /mocks/legit-demo.html | ALLOW <=0.20 | multimodal | ☐ |
| 6 | /mocks/paypal-login.html | BLOCK >=0.90 | multimodal | ☐ |
| 7 | /mocks/github-signin.html | BLOCK >=0.90 | multimodal | ☐ |
| 8 | /mocks/swiggy-login.html | BLOCK >=0.90 | multimodal | ☐ |
| 9 | https://paypa1.com | BLOCK, instant, 0 Gemini calls | lexical | ☐ |
| 10 | https://netfl1x.com | BLOCK, instant | lexical | ☐ |
| 11 | https://microsoft-login.com | BLOCK, instant | lexical | ☐ |
| 12 | https://github.com | ALLOW | multimodal | ☐ |
| 13 | Dashboard history after server restart | history persists | - | ☐ |
| 14 | Extension popup on a tab | badge PH / ?? / OK | - | ☐ |
| 15 | Unit suite: py -m unittest discover -s tests | all green | - | ☐ |

FAIL rules: any 502 timeout, wrong verdict, or crash = FAIL → report to Rajat.
Quota check before demo: GEMINI free calls remaining >= 10.
