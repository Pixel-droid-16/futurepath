# FuturePath v2 design fidelity correction

This revision corrects visible differences between the previous frontend and the group's `FuturePath Site v2.dc.html` mockup.

- Matched Geist / Geist Mono typography and the mockup's lavender/dark colour tokens.
- Changed Home to editorial text-left and prominent signal-feed card-right, replacing the unrelated hero illustration.
- Matched user audience tags, primary `Build my profile` action, three inline statistics, and pill navigation details.
- Preserved existing backend routes, scenario comparison, guided skill assessment, history, and snapshot approval workflows.
- Clearly labelled the synthetic feed and unverified resources, rather than claiming it is a live integration.

**Limits:** This is a closer adaptation of the home screen and core styling, not a pixel-for-pixel reproduction of every v2 page. Real browser visual QA remains necessary. Replit and RunPod not deployed.

## Run (Windows CMD)

From the extracted `FuturePath_v2_Fidelity_Fix` folder:

```cmd
python -m pip install -r requirements.txt
python -m uvicorn backend.app:app --reload
```

Open http://127.0.0.1:8000; stop any prior server first with Ctrl+C.

Never share API keys. Revoke the key shown earlier in your screenshot and replace it privately.
